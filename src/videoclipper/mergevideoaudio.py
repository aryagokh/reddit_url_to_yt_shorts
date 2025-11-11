import subprocess
import logging

logger = logging.getLogger(__name__)

def merge_audio_to_clip(input_audio_path: str, input_video_path: str, output_file_path: str):
    try:
        command = [
        'ffmpeg',
        '-i', input_video_path,
        '-i', input_audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-map', '0:v:0',  # Map video stream from first input
        '-map', '1:a:0',  # Map audio stream from second input
        output_file_path
        ]
        subprocess.run(command, check=True)
        logger.info(f"Successfully merged {input_video_path} and {input_audio_path} into {output_file_path}")
        return output_file_path
    except Exception as e:
        logger.error("Error in merge audio to clip - mergevideoaudio")
    return None