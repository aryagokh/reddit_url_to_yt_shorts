import whisper
import logging
import json
import torch

logger = logging.getLogger(__name__)

def log_gpu_usage():
    """Log current GPU memory usage."""
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            allocated = torch.cuda.memory_allocated(i) / 1024**3
            reserved = torch.cuda.memory_reserved(i) / 1024**3
            total = torch.cuda.get_device_properties(i).total_memory / 1024**3
            logger.info(
                f"GPU {i} ({torch.cuda.get_device_name(i)}): "
                f"{allocated:.2f}GB/{total:.2f}GB allocated, "
                f"{reserved:.2f}GB reserved"
            )
    else:
        logger.info("Running on CPU (CUDA not available)")

def load_model():
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading Whisper model on {device.upper()}...")
        
        model = whisper.load_model("medium", device=device)
        logger.info("Transcription model (WHISPER) loaded successfully")
        log_gpu_usage()
        
        return model
    except Exception as e:
        logger.error(f"Error loading transcription model: {e}")
        return None

def transcribe(audio_file_path: str, caption_output_path: str):
    model = load_model()
    if model is None:
        raise RuntimeError("Failed to load transcription model")
    
    logger.info(f"Starting transcription for: {audio_file_path}")
    log_gpu_usage()
    
    # Enable word-level timestamps
    result = model.transcribe(
        audio=audio_file_path, 
        task="transcribe", 
        verbose=True,
        word_timestamps=True  # THIS IS KEY!
    )
    
    logger.info("Transcription completed successfully!")
    log_gpu_usage()
    
    return result

def chunk_words(words, chunk_size=3):
    """
    Split words into chunks of specified size.
    
    Args:
        words: List of word dictionaries with 'word', 'start', 'end'
        chunk_size: Number of words per chunk (default: 3)
    
    Returns:
        List of chunks, each containing words and timing info
    """
    chunks = []
    for i in range(0, len(words), chunk_size):
        word_group = words[i:i + chunk_size]
        if word_group:
            chunks.append({
                'text': ' '.join([w['word'].strip() for w in word_group]),
                'start': word_group[0]['start'],
                'end': word_group[-1]['end']
            })
    return chunks

def transcribe_and_save_captions(audio_file_path: str, caption_output_path: str, 
                                 save_json: bool=False, save_srt: bool=True,
                                 words_per_caption: int=3):
    """
    Transcribe audio and save captions with customizable words per line.
    
    Args:
        audio_file_path: Path to audio file
        caption_output_path: Directory to save captions
        save_json: Whether to save full JSON output
        save_srt: Whether to save SRT file
        words_per_caption: Number of words per caption line (default: 3)
    """
    result = transcribe(audio_file_path=audio_file_path, caption_output_path=caption_output_path)
    
    if save_json:
        json_path = f"{caption_output_path}/captions_whisper.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        logger.info(f"Saved transcriptions in JSON: {json_path}")

    if save_srt:
        srt_path = f"{caption_output_path}/captions_whisper.srt"
        
        def fmt(t):
            """Format time for SRT (HH:MM:SS,mmm)"""
            h, t = divmod(t, 3600)
            m, s = divmod(t, 60)
            return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace('.', ',')
        
        with open(srt_path, "w", encoding="utf-8") as f:
            caption_index = 1
            
            for segment in result["segments"]:
                # Check if word-level timestamps are available
                if "words" in segment and segment["words"]:
                    # Split words into chunks
                    chunks = chunk_words(segment["words"], chunk_size=words_per_caption)
                    
                    for chunk in chunks:
                        f.write(f"{caption_index}\n")
                        f.write(f"{fmt(chunk['start'])} --> {fmt(chunk['end'])}\n")
                        f.write(f"{chunk['text']}\n\n")
                        caption_index += 1
                else:
                    # Fallback: split by words if word timestamps not available
                    words = segment["text"].strip().split()
                    duration = segment["end"] - segment["start"]
                    time_per_word = duration / len(words) if words else 0
                    
                    for i in range(0, len(words), words_per_caption):
                        word_group = words[i:i + words_per_caption]
                        start_time = segment["start"] + (i * time_per_word)
                        end_time = segment["start"] + ((i + len(word_group)) * time_per_word)
                        
                        f.write(f"{caption_index}\n")
                        f.write(f"{fmt(start_time)} --> {fmt(end_time)}\n")
                        f.write(f"{' '.join(word_group)}\n\n")
                        caption_index += 1
        
        logger.info(f"Saved {words_per_caption}-word captions in SRT: {srt_path}")
        return srt_path