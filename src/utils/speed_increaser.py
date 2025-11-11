from better_ffmpeg_progress import FfmpegProcess
from pathlib import Path
import subprocess
import logging
import sys

logger = logging.getLogger(__name__)

def speed_up_video(input_path: str, output_path: str, speed: float = 1.35):
    """
    Speed up a video without quality loss using ffmpeg.
    
    Args:
        input_path: Path to input video file
        output_path: Path to output video file
        speed: Speed multiplier (e.g., 1.25 = 25% faster, 1.5 = 50% faster)
    
    Note:
        - Video pts is divided by speed (setpts=PTS/{speed})
        - Audio tempo is multiplied by speed (atempo={speed})
        - For speed > 2.0, atempo filter needs to be chained
    """

    logger.info("Trying to speed up the video to 1.35")
    
    if not Path(input_path).exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if speed <= 0:
        raise ValueError("Speed must be greater than 0")
    
    video_speed = 1 / speed  
    
    # atempo filter only supports 0.5 to 2.0 range
    # For higher speeds, chain multiple atempo filters
    audio_filters = []
    remaining_speed = speed
    
    while remaining_speed > 2.0:
        audio_filters.append("atempo=2.0")
        remaining_speed /= 2.0
    
    while remaining_speed < 0.5:
        audio_filters.append("atempo=0.5")
        remaining_speed /= 0.5
    
    audio_filters.append(f"atempo={remaining_speed}")
    audio_filter_str = ",".join(audio_filters)
    
    # Build ffmpeg command
    # -i: input file
    # -filter:v: video filter (setpts adjusts timestamps)
    # -filter:a: audio filter (atempo adjusts speed without pitch change)
    # -c:v libx264: use H.264 codec
    # -preset slow: better compression (slower encoding but better quality)
    # -crf 18: high quality (0-51 scale, 18 is visually lossless)
    # -c:a aac: audio codec
    # -b:a 192k: audio bitrate
    command = [
        "ffmpeg",
        "-i", input_path,
        "-filter:v", f"setpts={video_speed}*PTS",
        "-filter:a", audio_filter_str,
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",  # Enable fast start for web playback
        "-y",  # Overwrite output file if exists
        output_path
    ]
    
    logger.info(f"Processing: {input_path}")
    logger.info(f"Speed: {speed}x")
    logger.info(f"Output: {output_path}")
    
    process = FfmpegProcess(command)
    process.run()
    
    logger.info(f"✓ Video processing complete! Output saved to: {output_path}")

    try:
        import os
        os.remove('yt_short.mp4_ffmpeg_log.txt')
        logger.info("Removed log file for progress bar - speedincreaser")
    except Exception as e:
        logging.warning("Failed to remove log file - speedincreaser! You can safely remove it manually later!")
    return output_path


if __name__ == "__main__":
    input_path = 'output\post_upload_52\yt_short.mp4'
    output_path = 'output\post_upload_52\yt_short_spedup_35.mp4'
    speed = 1.35
    
    try:
        speed_up_video(input_path, output_path, speed)
    except Exception as e:
        print(f"\n❌ Error: {e}")