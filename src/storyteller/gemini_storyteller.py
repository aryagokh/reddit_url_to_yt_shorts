import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)

def load_model(model_name: str = 'gemini-2.5-pro'):
    try:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        model = genai.GenerativeModel(model_name=model_name)
        logger.info("Model Loaded!")
        return model
    except Exception as e:
        logger.exception("Error occurred in load_model - Gemini storyteller!")
    return None

def load_prompt(post_title, post_content):
    prompt = f"""
You are a YouTube Shorts scriptwriter who specializes in viral Reddit story content. 
Your scripts consistently achieve 80%+ average view duration.

CONVERT THIS REDDIT POST INTO A 55-60 SECOND SCRIPT:

Title: {post_title}
Content: {post_content}

---

VIRAL FORMULA (MANDATORY):

[0-3 SEC] HOOK - Use ONE of these proven patterns:
→ Shocking revelation: "I just found out my wife has been..."
→ Impossible situation: "My boss told me to choose between..."
→ Pattern break: "Everyone thinks I'm crazy, but I'm not the one who..."
→ Forbidden truth: "Nobody talks about what really happens when..."

[3-15 SEC] CONTEXT TEASE
→ Give JUST enough setup to understand the stakes
→ Drop a breadcrumb that promises a crazy payoff
→ Keep them wondering "wait, WHAT happens next?"

[15-45 SEC] STORY ARC
→ Build tension with mini-reveals every 5-7 seconds
→ Use conversational, natural pacing (like texting a friend)
→ Include one "wait, it gets worse..." moment
→ Make the narrator relatable, not a victim or hero — just REAL

[45-60 SEC] PAYOFF
→ Deliver on the hook's promise (twist, justice, irony, or emotional gut-punch)
→ End with a line that makes viewers want to comment/share
→ NO moral lessons, NO "looking back now..." — just land it and stop

---

STYLE RULES:
✓ Write like someone telling their story at 2AM to a close friend
✓ Use short sentences. Vary rhythm. Create momentum.
✓ Embed emotion in word choice, not [tone cues] — show, don't label
✓ Cut ALL filler: "So basically..." "I guess..." "To be honest..."
✓ Make every sentence earn its place or delete it

AVOID:
✗ Explaining the obvious
✗ Slow, dramatic builds (this isn't a movie trailer)
✗ Over-narrating emotions ("I felt so angry" → just show the anger)
✗ Moral summaries or life lessons at the end

---

OUTPUT FORMAT:
Just the script. No labels, no tone markers, no scene directions.
First line = hook. Last line = payoff. Everything between = momentum.

Example of rhythm:
"My husband accused me of cheating. With his brother. At his brother's wedding. While I was in the hospital. Giving birth. To his son."

Now write the script.
"""
    logger.info("Prompt created.")
    return prompt
    
def story_phrasing(post_title: str, post_content: str, model_name: str = 'gemini-2.5-flash'):
    model = load_model(model_name=model_name)
    if not model:
        logger.error("Model loading failed, cannot generate story.")
        return None
    
    prompt = load_prompt(post_title=post_title, post_content=post_content)
    try:
        response = model.generate_content(prompt)
        logger.info("Story generated successfully.")
        return response.text
    except Exception:
        logger.exception("Error occurred during story generation.")
        return None