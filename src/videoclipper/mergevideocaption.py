# from better_ffmpeg_progress import FfmpegProcess
# import subprocess
# import logging
# import os

# logger = logging.getLogger(__name__)

# def hardcode_subtitles(video_path, srt_path, output_path):
#     """
#     Hardcodes SRT subtitles into a video file using FFmpeg with YouTube Shorts styling.

#     Args:
#         video_path (str): Path to the input video file.
#         srt_path (str): Path to the SRT subtitle file.
#         output_path (str): Path for the output video file with hardcoded subtitles.
#     """
#     subtitle_filter = (
#         f"subtitles='{srt_path}':force_style='"
#         "FontName=Arial Black,"
#         "FontSize=18,"                 # Smaller font
#         "Bold=1,"
#         "PrimaryColour=&H0000FFFF,"    # Yellow text
#         "OutlineColour=&H00000000,"    # Black outline
#         "Outline=3,"                   
#         "Shadow=2,"                    
#         "Alignment=2,"                 # Bottom center
#         "MarginV=50"                   # 30 originally - Closer to bottom
#         "'"
#     )

#     command = [
#         'ffmpeg',
#         '-i', video_path,
#         '-vf', subtitle_filter,
#         '-c:v', 'libx264', 
#         '-preset', 'slow', #'medium', 
#         '-crf', '23',     
#         '-c:a', 'copy', 
#         output_path
#     ]

#     try:
#         process = FfmpegProcess(command)
#         process.run()
#         logger.info(f"Subtitles successfully hardcoded into: {output_path}")
        # try:
        #     os.remove('clip_with_audio.mp4_ffmpeg_log.txt')
        #     logger.info("Removed log file for progress bar - captionmerge")
        # except Exception as e:
        #     logging.warning("Failed to remove log file - captionmerge! You can safely remove it manually later!")
        # return output_path
#     except Exception as e:
#         logger.error(f"Error hardcoding subtitles: {e}")
#         return None

# if __name__ == "__main__":
#     input_video = "output/post_test/raw/clip_with_audio.mp4"
#     subtitle_file = "output/post_test/raw/captions_whisper.srt"
#     output_video = "output/post_test/raw/output_with_subtitles_aesthetic_better.mp4"

#     hardcode_subtitles(input_video, subtitle_file, output_video)

from better_ffmpeg_progress import FfmpegProcess
import subprocess
import logging
import os

logger = logging.getLogger(__name__)

def hardcode_subtitles(video_path, srt_path, output_path, style="viral_yellow"):
    """
    Hardcodes SRT subtitles into a video file using FFmpeg with multiple style presets.

    Args:
        video_path (str): Path to the input video file.
        srt_path (str): Path to the SRT subtitle file.
        output_path (str): Path for the output video file with hardcoded subtitles.
        style (str): Caption style preset. Options:
            - "viral_yellow" (default): Bold yellow with heavy black outline
            - "tiktok_white": White text with black background box
            - "mrbeast": All caps, thick outline, explosive style
            - "alex_hormozi": Bold white, minimal, clean
            - "subway_surfers": Colorful bouncy style
    """
    
    styles = {
        "viral_yellow": (
            f"subtitles='{srt_path}':force_style='"
            "FontName=Impact,"              # More impactful than Arial Black
            "FontSize=20,"                  # Bigger = better retention
            "Bold=1,"
            "PrimaryColour=&H00FFFF,"       # Pure yellow (BGR format)
            "OutlineColour=&H000000,"       # Black outline
            "BackColour=&H80000000,"        # Semi-transparent black background
            "Outline=4,"                    # Thicker outline for readability
            "Shadow=0,"                     # No shadow (cleaner look)
            "Alignment=2,"                  # Bottom center
            "MarginV=120"                   # Centered in lower third (OPTIMAL)
            "'"
        ),

#         "viral_yellow": (
#             f"subtitles='{srt_path}':force_style='"
#             "FontName=Impact,"              # More impactful than Arial Black
#             "FontSize=22,"                  # Bigger = better retention
#             "Bold=1,"
#             "PrimaryColour=&H00FFFF,"       # Pure yellow (BGR format)
#             "OutlineColour=&H000000,"       # Black outline
#             "BackColour=&H80000000,"        # Semi-transparent black background
#             "Outline=4,"                    # Thicker outline for readability
#             "Shadow=0,"                     # No shadow (cleaner look)
#             "Alignment=2,"                  # Bottom center
#             "MarginV==120" #80                    # Higher margin (more space from bottom)
#             "'"
#         ),    #slightly below
        
        "tiktok_white": (
            f"subtitles='{srt_path}':force_style='"
            "FontName=Arial Black,"
            "FontSize=20,"
            "Bold=1,"
            "PrimaryColour=&HFFFFFF,"       # White text
            "OutlineColour=&H000000,"       # Black outline
            "BackColour=&HDD000000,"        # Dark background box (higher opacity)
            "BorderStyle=4,"                # Box background style
            "Outline=2,"
            "Shadow=0,"
            "Alignment=2,"
            "MarginV=90"
            "'"
        ),
        
        "mrbeast": (
            f"subtitles='{srt_path}':force_style='"
            "FontName=Impact,"
            "FontSize=26,"                  # HUGE
            "Bold=1,"
            "PrimaryColour=&H00FFFF,"       # Yellow
            "OutlineColour=&H000000,"
            "BackColour=&H00000000,"
            "Outline=6,"                    # THICC outline
            "Shadow=3,"                     # Drop shadow for depth
            "Alignment=2,"
            "MarginV=100,"
            "ScaleX=110,"                   # Slightly stretched horizontally
            "ScaleY=110"
            "'"
        ),
        
        "alex_hormozi": (
            f"subtitles='{srt_path}':force_style='"
            "FontName=Arial,"               # Clean, professional
            "FontSize=24,"
            "Bold=1,"
            "PrimaryColour=&HFFFFFF,"       # White
            "OutlineColour=&H000000,"
            "Outline=3,"
            "Shadow=0,"
            "Alignment=2,"
            "MarginV=120"                   # Center-bottom area
            "'"
        ),
        
        "subway_surfers": (
            f"subtitles='{srt_path}':force_style='"
            "FontName=Comic Sans MS,"       # Playful font
            "FontSize=24,"
            "Bold=1,"
            "PrimaryColour=&H00FF00,"       # Bright cyan/green
            "OutlineColour=&HFF00FF,"       # Magenta outline (colorful!)
            "BackColour=&H80000000,"
            "Outline=5,"
            "Shadow=2,"
            "Alignment=2,"
            "MarginV=70"
            "'"
        ),
        
        "minimalist": (
            f"subtitles='{srt_path}':force_style='"
            "FontName=Helvetica,"
            "FontSize=20,"
            "Bold=1,"
            "PrimaryColour=&HFFFFFF,"       # White
            "OutlineColour=&H000000,"
            "Outline=2,"
            "Shadow=0,"
            "Alignment=2,"
            "MarginV=100"
            "'"
        )
    }
    
    if style not in styles:
        logger.warning(f"Style '{style}' not found. Using 'viral_yellow' as default.")
        style = "viral_yellow"
    
    subtitle_filter = styles[style]

    command = [
        'ffmpeg',
        '-i', video_path,
        '-vf', subtitle_filter,
        '-c:v', 'libx264', 
        '-preset', 'slow',        # Balance between speed and quality
        '-crf', '23',               # Good quality
        '-c:a', 'copy',             # Keep original audio
        '-y',                       # Overwrite output file
        output_path
    ]

    try:
        logger.info(f"Applying '{style}' caption style...")
        process = FfmpegProcess(command)
        process.run()
        logger.info(f"Subtitles successfully hardcoded into: {output_path}")
        
        try:
            os.remove('clip_with_audio.mp4_ffmpeg_log.txt')
            logger.info("Removed log file for progress bar - captionmerge")
        except Exception as e:
            logging.warning("Failed to remove log file - captionmerge! You can safely remove it manually later!")
        
        return output_path
    except Exception as e:
        logger.error(f"Error hardcoding subtitles: {e}")
        return None


if __name__ == "__main__":
    input_video = "output/post_test/raw/clip_with_audio.mp4"
    subtitle_file = "output/post_test/raw/captions_whisper.srt"
    
    # Try different styles - test which performs best!
    
    # Style 1: Classic viral yellow (RECOMMENDED for most content)
    output_1 = "output/post_test/raw/output_viral_yellow.mp4"
    hardcode_subtitles(input_video, subtitle_file, output_1, style="viral_yellow")
    
    # # Style 2: TikTok-style white box
    # output_2 = "output/post_test/raw/output_tiktok.mp4"
    # hardcode_subtitles(input_video, subtitle_file, output_2, style="tiktok_white")
    
    # # Style 3: MrBeast explosive style
    # output_3 = "output/post_test/raw/output_mrbeast.mp4"
    # hardcode_subtitles(input_video, subtitle_file, output_3, style="mrbeast")
    
    # # Style 4: Alex Hormozi clean minimal
    # output_4 = "output/post_test/raw/output_hormozi.mp4"
    # hardcode_subtitles(input_video, subtitle_file, output_4, style="alex_hormozi")

    # # Style 4: Alex Hormozi clean minimal
    # output_4 = "output/post_test/raw/output_subway.mp4"
    # hardcode_subtitles(input_video, subtitle_file, output_4, style="subway_surfers")

    # # Style 4: Alex Hormozi clean minimal
    # output_4 = "output/post_test/raw/output_minimal.mp4"
    # hardcode_subtitles(input_video, subtitle_file, output_4, style="minimalist")
