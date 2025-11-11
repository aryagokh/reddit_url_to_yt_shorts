import random
import os
import logging
from pathlib import Path
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips

logger = logging.getLogger(__name__)

def get_all_videos_from_category(base_folder: str, category: str, extensions: list = None) -> list:
    """
    Get all video files from a category folder and its subfolders.
    
    Args:
        base_folder (str): Base videos folder (e.g., 'videos')
        category (str): Category name (e.g., 'gameplay', 'nature')
        extensions (list): List of valid video extensions
    
    Returns:
        list: List of paths to all video files in category
    """
    if extensions is None:
        extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    
    category_path = os.path.join(base_folder, category)
    
    if not os.path.exists(category_path):
        raise FileNotFoundError(f"Category folder not found: {category_path}")
    
    logger.info(f"Searching for videos in category: {category}")
    
    video_files = []
    
    for root, dirs, files in os.walk(category_path):
        for file in files:
            if os.path.splitext(file)[1].lower() in extensions:
                video_files.append(os.path.join(root, file))
    
    if not video_files:
        raise FileNotFoundError(f"No video files found in category: {category}")
    
    logger.info(f"Found {len(video_files)} videos in '{category}' category")
    for video in video_files:
        logger.debug(f"  - {os.path.relpath(video, base_folder)}")
    
    return video_files

def get_random_video_from_category(base_folder: str, category: str) -> str:
    """
    Select a random video from specified category.
    
    Args:
        base_folder (str): Base videos folder
        category (str): Category name
    
    Returns:
        str: Path to randomly selected video
    """
    video_files = get_all_videos_from_category(base_folder, category)
    selected_video = random.choice(video_files)
    
    relative_path = os.path.relpath(selected_video, base_folder)
    logger.info(f"Selected random video: {relative_path}")
    
    return selected_video

def get_audio_duration(audio_path: str) -> float:
    """
    Get duration of audio file in seconds.
    
    Args:
        audio_path (str): Path to audio file
    
    Returns:
        float: Duration in seconds
    """
    logger.info(f"Reading audio duration from: {os.path.basename(audio_path)}")
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    audio.close()
    logger.info(f"Audio duration: {duration:.2f}s")
    return duration

def extract_clip_from_video(video_path: str, start_time: float, duration: float) -> VideoFileClip:
    """
    Extract a clip from a video starting at specific time.
    
    Args:
        video_path (str): Path to source video
        start_time (float): Start time in seconds
        duration (float): Clip duration in seconds
    
    Returns:
        VideoFileClip: Extracted clip
    """
    video = VideoFileClip(video_path)
    video_duration = video.duration
    
    end_time = min(start_time + duration, video_duration)
    actual_duration = end_time - start_time
    
    logger.info(f"  Extracting {actual_duration:.2f}s from {os.path.basename(video_path)} ({start_time:.2f}s to {end_time:.2f}s)")
    
    clip = video.subclipped(start_time, end_time)
    return clip

def create_clip_with_merging(base_folder: str, 
                             category: str, 
                             required_duration: float,
                             max_videos: int = 3) -> VideoFileClip:
    """
    Create a clip of required duration, merging multiple random clips if needed.
    
    Args:
        base_folder (str): Base videos folder
        category (str): Category name
        required_duration (float): Total duration needed in seconds
        max_videos (int): Maximum number of videos to merge
    
    Returns:
        VideoFileClip: Composite clip of required duration
    """
    logger.info(f"Creating clip of {required_duration:.2f}s from '{category}' category")
    
    clips = []
    remaining_duration = required_duration
    video_count = 0
    
    video_files = get_all_videos_from_category(base_folder, category)
    
    while remaining_duration > 0.1 and video_count < max_videos:  # 0.1s tolerance
        video_count += 1
        
        video_path = random.choice(video_files)
        video = VideoFileClip(video_path)
        video_duration = video.duration
        
        logger.info(f"Video {video_count}: {os.path.basename(video_path)} (duration: {video_duration:.2f}s, size: {video.size[0]}x{video.size[1]})")
        
        if video_duration >= remaining_duration:
            max_start = video_duration - remaining_duration
            start_time = random.uniform(0, max_start) if max_start > 0 else 0
            
            clip = extract_clip_from_video(video_path, start_time, remaining_duration)
            clips.append(clip)
            remaining_duration = 0
            
        else:
            if video_duration > 5:  # If video is reasonably long, take random segment
                start_time = random.uniform(0, video_duration * 0.3)  # Start from first 30%
            else:
                start_time = 0
            
            clip = extract_clip_from_video(video_path, start_time, video_duration - start_time)
            clips.append(clip)
            remaining_duration -= clip.duration
        
        video.close()
    
    if remaining_duration > 0.1:
        logger.warning(f"Could not fill entire duration. Short by {remaining_duration:.2f}s")
    
    # Merge clips if multiple
    if len(clips) > 1:
        logger.info(f"Merging {len(clips)} clips together...")
        final_clip = concatenate_videoclips(clips, method="compose")
    else:
        final_clip = clips[0]
    
    logger.info(f"Final merged clip duration: {final_clip.duration:.2f}s, size: {final_clip.size[0]}x{final_clip.size[1]}")
    return final_clip

def extract_and_save_clip(base_folder: str,
                          category: str,
                          audio_path: str,
                          output_path: str,
                          max_videos_to_merge: int = 3,
                          prepare_for_vertical: bool = False) -> str:
    """
    Complete pipeline: create clip from category matching audio duration and save it.
    
    Args:
        base_folder (str): Base videos folder (e.g., 'videos')
        category (str): Category name (e.g., 'gameplay', 'nature')
        audio_path (str): Path to audio file (to determine duration)
        output_path (str): Path to save extracted clip
        max_videos_to_merge (int): Maximum number of videos to merge
        prepare_for_vertical (bool): If True, save note that this will be converted to 9:16
    
    Returns:
        str: Path to saved clip
    """
    try:
        logger.info("=" * 60)
        logger.info("STARTING CLIP EXTRACTION")
        logger.info("=" * 60)
        
        required_duration = get_audio_duration(audio_path)
        
        clip = create_clip_with_merging(
            base_folder=base_folder,
            category=category,
            required_duration=required_duration,
            max_videos=max_videos_to_merge
        )
        
        if prepare_for_vertical:
            logger.info("Note: This clip will be converted to 9:16 (1080x1920) in the composer step")
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        logger.info(f"Saving clip to: {output_path}")

        clip.write_videofile(
            output_path,
            codec='h264_nvenc', 
            audio_codec='aac',
            threads=8,
            preset='p7',
            bitrate='12000k', 
            fps=60,
            logger="bar",  
        )
        
        clip.close()
        
        logger.info("=" * 60)
        logger.info("CLIP EXTRACTION COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        
        return output_path
        
    except Exception as e:
        logger.exception("Error during clip extraction!")
        raise

# Example usage
if __name__ == "__main__":
    extract_and_save_clip(
        base_folder="E:/YouTube/videos",
        category="gameplay",
        audio_path="output/post_confess/raw/gemini_story_audio.wav",
        output_path="output/post_confess/raw/gameplay_clip.mp4",
        max_videos_to_merge=1,
        prepare_for_vertical=True
    )