import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)

def load_model(model_name: str = 'gemini-2.5-flash'):
    try:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        model = genai.GenerativeModel(model_name=model_name)
        logger.info("Model Loaded!")
        return model
    except Exception as e:
        logger.exception("Error occurred in load_model - Titleandtagssuggest!")
    return None

def load_prompt(post):
    prompt = f"""
You are an expert at creating engaging, and catchy titles YouTube Shorts and Tnstagram Reels. Your task is to read a Reddit post story and give a title and hashtags that grabs attention immediately.

No need to add filler text, just directly start with title and also add hashtags.

Expected format:
1. Yt short title: ...
2. Yt short hashtags: ...
3. Instagram reel title: ...
4. Instagram reel hashtags: ...
5: Common Description: ...

Post Text: {post}
"""
    logger.info("Prompt Created.")
    return prompt
    
def get_title_and_tags(post: str, model_name: str = 'gemini-2.5-flash'):
    model = load_model(model_name=model_name)
    if not model:
        logger.error("Model loading failed, cannot generate title and tags.")
        return None
    
    prompt = load_prompt(post=post)
    try:
        response = model.generate_content(prompt)
        logger.info("Title and Tags generated successfully.")
        return response.text
    except Exception:
        logger.exception("Error occurred during title and tags generation.")
        return None