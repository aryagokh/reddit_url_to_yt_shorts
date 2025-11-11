import logging
import os
import mimetypes
import struct
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

def save_binary_file(file_name: str, data: bytes):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, "wb") as f:
        f.write(data)
    logger.info(f"File saved to: {file_name}")

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    # (copy your existing convert_to_wav function here)
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        chunk_size,
        b"WAVE",
        b"fmt ",
        16,
        1,
        num_channels,
        sample_rate,
        byte_rate,
        block_align,
        bits_per_sample,
        b"data",
        data_size
    )
    return header + audio_data

def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    bits_per_sample = 16
    rate = 24000

    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate_str = param.split("=", 1)[1]
                rate = int(rate_str)
            except (ValueError, IndexError):
                pass
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass

    return {"bits_per_sample": bits_per_sample, "rate": rate}

def generate_narration_audio(story_text: str, output_path: str, model: str = "gemini-2.5-flash-preview-tts", voice_name: str = "Zephyr"):
    """
    Generate narration audio from story text and save to output_path.

    Args:
        story_text (str): The text to convert to speech.
        output_path (str): The full file path (including filename) to save audio.
        api_key (str): Your GEMINI_API_KEY.
    """
    logger.info("Initializing TTS generation...")
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

    model = model
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=story_text)],
        )
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice_name)
            )
        ),
    )

    file_index = 0
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue

        inline_data = chunk.candidates[0].content.parts[0].inline_data
        if inline_data and inline_data.data:
            logger.info("Received audio chunk, saving to file...")
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            if file_extension is None:
                file_extension = ".wav"
                audio_data = convert_to_wav(inline_data.data, inline_data.mime_type)
            else:
                audio_data = inline_data.data

            if file_index == 0:
                if not output_path.endswith(file_extension):
                    output_path += file_extension
                save_binary_file(output_path, audio_data)
                file_index += 1
        else:
            logger.debug(f"Chunk text: {chunk.text}")

    logger.info("TTS generation complete.")
    return output_path
