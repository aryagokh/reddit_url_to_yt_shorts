
from src.narrator.whisper_transcribe import transcribe_and_save_captions
from src.titleandtags.titleandtagssuggest import get_title_and_tags
from src.narrator.gemini_narrator import generate_narration_audio
from src.videoclipper.mergevideocaption import hardcode_subtitles
from src.videoclipper.mergevideoaudio import merge_audio_to_clip
from src.videoclipper.videoclipper import extract_and_save_clip
from src.storyteller.gemini_storyteller import story_phrasing
from src.scrapper.praw_scrapper import fetch_post
from src.utils.logging_setup import setup_logger
from src.utils.voice_picker import pick_voice
from src.utils.helper import save_json
from src.utils.speed_increaser import speed_up_video
import warnings
import argparse
import random
import time
import os

warnings.filterwarnings(action='ignore')

def parse_args():
    parser = argparse.ArgumentParser(description='Generate YouTube Shorts from Reddit posts')
    
    parser.add_argument('--url', type=str, required=True, help='Reddit post URL')
    parser.add_argument('--post-number', type=str, required=True, help='Post number (for folder name)')
    parser.add_argument('--post-type', type=str, required=True, help='Post type-gender or only gender {educational, casual, motivational, emotional, storytelling, youthful}-{male, female} or only male/female')
    
    # Optional arguments
    parser.add_argument('--short-speed', type=float, default=1.25,
        help='Playback speed of the final short. '
            'Use 1.3–1.35x for funny/chaotic/revenge stories (fast pacing), '
            'and 1.25x for emotional, wholesome, or horror stories (slower pacing). '
            'Default is 1.25x.'
    )
    parser.add_argument('--words-per-caption', type=int, default=1,
        help='Number of words to show per caption update. '
            'Use 1 word for fast or funny stories (quick rhythm), '
            'and 2 words for emotional or horror stories (smoother readability). '
            'Default is 1.'
    )
    parser.add_argument('--model', type=str, default='gemini-2.5-pro', help='Story generation model (default: gemini-2.5-pro)')
    parser.add_argument('--video-category', type=str, default='gameplay', help='Video category (default: gameplay)')
    parser.add_argument('--video-base-folder', type=str, default='E:/YouTube/videos', help='Base folder for video clips (default: E:/YouTube/videos)')
    
    return parser.parse_args()


class CONFIG:
    def __init__(self, args):
        self.url = args.url
        self.story_model_name = args.model
        
        self.post_number = args.post_number
        self.post_type = args.post_type
        
        self.output_dir = f'output/post_{self.post_number}'
        self.captions_output_path = f'{self.output_dir}/raw'
        self.track_csv_path = f'posttracker/posts_done.csv'
        
        self.audio_output_path_narrator = f'{self.output_dir}/raw/gemini_story_audio.wav'
        self.video_output_path = f'{self.output_dir}/raw/clip_raw.mp4'
        self.clip_with_audio = f'{self.output_dir}/raw/clip_with_audio.mp4'
        self.final_output_path = f'{self.output_dir}/yt_short.mp4'
        self.speed_up_final_output_path = f'{self.output_dir}/yt_short_sped_up.mp4'
        self.title_and_tags_save_path = f'{self.output_dir}/title_and_tags.txt'
        
        self.video_category = args.video_category
        self.video_base_folder = args.video_base_folder

        self.short_speed = args.short_speed
        self.words_per_caption = args.words_per_caption


def main():
    start_time = time.time()
    args = parse_args()
    config = CONFIG(args)
    
    logger, RUN_LOG_DIR = setup_logger(output_dir=config.output_dir, run_name=None)
    
    try:
        logger.info("Starting main process...")
        logger.info(f"Processing URL: {config.url}")
        logger.info(f"Post number: {config.post_number}")
        
        # Fetch Reddit post
        post_title, post_content = fetch_post(url=config.url)
        logger.info("MAIN: Post fetched successfully!")
        save_json(
            {"post_title": post_title, "post_content": post_content},
            "reddit_fetch.json",
            config.output_dir,
        )

        # Generate story
        story_output = story_phrasing(
            post_title=post_title,
            post_content=post_content,
            model_name=config.story_model_name
        )
        logger.info("MAIN: Story generated successfully.")
        save_json(
            {"story_output": story_output},
            "story_output.json",
            config.output_dir,
        )

        # Generate narration audio
        voice_name = pick_voice(config.post_type)
        logger.info(f"#############MAIN: ----- Voice picked: {voice_name} ----- #############")

        narration_audio_path = generate_narration_audio(
            story_text=story_output,
            output_path=config.audio_output_path_narrator,
            voice_name=voice_name
        )
        logger.info(f"MAIN: Story narration generated successfully! Saved to {config.audio_output_path_narrator}")

        # Generate captions
        whisper_captions_path = transcribe_and_save_captions(
            audio_file_path=narration_audio_path,
            caption_output_path=config.captions_output_path,
            save_json=False,
            save_srt=True,
            words_per_caption=config.words_per_caption
        )
        logger.info(f"MAIN: Story captions generated successfully! Saved to {config.captions_output_path}")

        # Extract video clip
        clip_path = extract_and_save_clip(
            base_folder=config.video_base_folder,
            category=config.video_category,
            audio_path=narration_audio_path,
            output_path=config.video_output_path,
            max_videos_to_merge=1,
            prepare_for_vertical=True
        )
        logger.info(f"MAIN: Short clip generated successfully! Saved to {clip_path}")

        # Merge audio with video
        clip_with_audio_path = merge_audio_to_clip(
            input_audio_path=narration_audio_path,
            input_video_path=clip_path,
            output_file_path=config.clip_with_audio
        )
        logger.info(f"MAIN: Audio merged with clip successfully! Saved to {clip_with_audio_path}")

        # Add subtitles
        logger.info(f"MAIN: Adding subtitles to video...")
        final_short_output_path = hardcode_subtitles(
            video_path=clip_with_audio_path,
            srt_path=whisper_captions_path,
            output_path=config.final_output_path
        )
        logger.info(f"MAIN: Final short saved successfully! Saved to {final_short_output_path}")
        logger.info(f"✅ COMPLETE! Video ready at: {final_short_output_path}")

        # Speed Up the video
        logger.info(f"Speeding up the video: {config.short_speed}x the original speed!")
        final_spedup_short_output_path = speed_up_video(
            input_path=final_short_output_path,
            output_path=config.speed_up_final_output_path,
            speed=config.short_speed
        )
        logger.info(f"✅ Speeding up the video complete! Saved to {final_spedup_short_output_path}")

        # Get titles and tags
        logger.info(f"MAIN: Generating titles and tags for YT and IG...")
        title_and_tags = get_title_and_tags(
            post=story_output
        )
        with open(config.title_and_tags_save_path, 'w', encoding='utf-8') as file:
            file.write(title_and_tags)
        logger.info(f"MAIN: Title and Tags generated successfully! Saved to {config.title_and_tags_save_path}")

        
        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        
        logger.info("Complete pipeline run successful!!")
        logger.info(f"Time taken: {int(minutes)} minute(s) and {seconds:.2f} second(s)")
        logger.info("Finish Graceful!")
        
    except Exception as e:
        logger.exception("Error occurred in main run generation!")


if __name__ == "__main__":
    main()