import praw
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

def define_client():
    try:
        reddit = praw.Reddit(
            client_id=os.getenv('r_client_id'),
            client_secret=os.getenv('r_client_secret'),
            user_agent=os.getenv('r_user_agent')
        )
        logger.info("Reddit client defined successfully.")
        return reddit
    except Exception as e:
        logger.exception(f"Error occurred while defining Reddit client.\nError message: {e}")
    return None


def fetch_post(url: str):
    try:
        reddit = define_client()
        if not reddit:
            logger.error("Reddit client is None. Aborting fetch_post.")
            return None, None
        
        submission = reddit.submission(url=url)
        if not submission.title or not submission.selftext:
            logger.error("Submission title or text is empty.")
            return None, None
        logger.info(f"Post fetched successfully from URL: {url}")
        return submission.title, submission.selftext
    
    except Exception as e:
        logger.exception("Error occurred in fetch_post.")
    return None, None

if __name__ == '__main__':
    import time

    start_time = time.time()
    post_title, post_content = fetch_post(
        url='https://www.reddit.com/r/tifu/comments/1ocxo8k/tifu_by_telling_my_gym_crush_i_love_you/'
    )
    print("\n\n\n\n\n")
    print(f"Post title{post_title}")
    print(f"Post Content:\n{post_content}")
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.6f} seconds")