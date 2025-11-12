# Reddit URL to Shorts Generator

This is an end-to-end, automated AI factory that turns any Reddit post into a viral, captioned YouTube Short in under 5 minutes.

**No manual editing. No green screens. Just one command.**

---

## ✨ Features

- **AI Storyteller**: Uses Gemini to read a messy Reddit post and rewrite it as a 60-second, high-retention "viral" script.
- **AI Voice Actor**: Generates realistic, high-quality audio narration for the script using Gemini TTS.
- **AI Transcriber**: Uses Whisper to create perfectly timestamped, word-by-word `.srt` caption files.
- **Smart Video Clipper**: Automatically finds background gameplay footage and cuts it to the exact length of the audio narration.
- **Automated "Builder"**: Uses FFmpeg to merge the audio, video, and burn the captions directly onto the final short.
- **Retention Knobs**: Includes built-in "retention hacks" like speeding up the final video and controlling caption pacing.
- **Factory Manager Mode**: Includes a batch runner script to queue up 10, 20, or 100 jobs and let them run overnight.

---

## 🏭 How It Works: The "AI Factory"

This project runs like an assembly line, controlled by one Factory Controller script (`run.py`):

1. **Treasure Hunter** (`praw_scrapper`): Fetches the Reddit post (title + story).
2. **Storyteller** (`gemini_storyteller`): Rewrites the story into a script.
3. **Voice Actor** (`gemini_narrator`): Records the script to a `.wav` file.
4. **Transcriber** (`whisper_transcribe`): Listens to the `.wav` and creates the `.srt` caption file.
5. **Master Clipper** (`videoclipper`): Cuts a silent gameplay clip to the exact audio length.
6. **FFmpeg Builder** (`mergevideo...`): Merges the audio, video, and burns the captions to create the final `yt_short.mp4`.
7. **Marketing AI** (`titleandtagssuggest`): Writes your YouTube title and tags for you.

---

## 🚀 Getting Started: Installation & Setup

Follow these steps to get your own AI Factory running.

### 📦 1. "Pull" the Code

First, clone this repository to your local machine:

```bash
git clone https://github.com/aryagokh/reddit_url_to_yt_shorts.git
cd reddit_url_to_yt_shorts
```

### 🔄 1.5. Setup your environment

You can go ahead and setup your python virtual env using your preferences but I prefer using Anaconda. Create your virtual env and keep it activated before you proceed to next steps.

- **MiniConda Installation and Activation Guide**: [miniconda-guide](https://docs.anaconda.com/miniconda/)
- **Virtual env using python** (less preferred by me): [venv-guide](https://docs.python.org/3/library/venv.html)

### 📚 2. Install the "Tools" (Dependencies)

* This project uses several Python libraries. Install them all with pip:

```bash
pip install -r requirements.txt
```

* Also, you should have FFMpeg installed in your system.
Windows installation guide: [YouTube Video](https://youtu.be/JR36oH35Fgg?si=7oHn5TZsi6Qe_7_a)
MacOs (via Homebrew): `brew install ffmpeg`
Linux:
```
sudo apt update
sudo apt install ffmpeg
```

Then verify installation: `ffmpeg -version`

### 🔑 3. Set Your "Keys" (API & Environment)

This factory needs keys to open the doors for the AI "workers."

Create a file named `.env` in the main project folder and add your secret keys:

```env
# Gemini API Key (for Storyteller & Narrator)
GEMINI_API_KEY="your_google_ai_studio_api_key"

# PRAW API Keys (for the Reddit Treasure Hunter)
r_client_id="your_reddit_client_id"
r_client_secret="your_reddit_client_secret"
r_user_agent="YourAppNameV1.0 by /u/your_reddit_username"
```

**Where to get your keys:**
- **Reddit API**: [Watch this Video](https://www.youtube.com/watch?v=gIZJQmX-55U)
- **Gemini API**: [Google AI Studio](https://aistudio.google.com/apikey)


### 🎞️ 4. Stock the "Warehouse" (Background Videos)
The Master Clipper needs a folder of videos to cut from.

Create a base folder, for example:

```
E:/YouTube/videos
```
Inside it, create category subfolders such as:
```
gameplay/
nature/
satisfying/
Fill these folders with .mp4 background clips.
```
By default, the script looks for clips in ```E:/YouTube/videos```,
but you can change this path with the ```--video-base-folder``` argument.


## ⚙️ USAGE: Running Your "AI Factory"

You can run the factory in two modes:

### 🧩 Method 1: The "Single Job" (Good for testing)

Use ```run.py``` for a single, specific Reddit post.
This acts as the Factory Controller.

You must provide:<br>

* The Reddit post URL
* A unique post number
* A post type (like "emotional-female", "funny", etc.)

Example:
```
python run.py --url "https://www.reddit.com/r/..." 
              --post-number "101" 
              --post-type "emotional-female"
```

This will create a new folder:
```
output/post_101/
```

Inside it, you’ll find:

* yt_short_sped_up.mp4 → your final short video
* all intermediate assets (audio, captions, etc.)

If you have video files in different directory, you can run it like this:
Say you have your video subfolders in `C:\Videos`
```
python run.py --url "https://www.reddit.com/r/..." 
              --post-number "101" 
              --post-type "emotional-female"
              --video-base-folder "C:\Videos"
              --video-category "gameplay"
```

## 🧠 Method 2: Factory Manager Mode (Batch Processing)

Once you’re confident with single runs, unleash the Factory Manager Mode to process multiple Reddit posts overnight.

Example:
```
python batch_run.py
```
You can enter all the details as it asks during runtime and schedule it for as many URLs as you want.
(Watch you API Key Limits)


## 💬 Contributing

Pull requests are welcome!
If you have feature ideas, open an issue or submit a PR — help make the AI Factory even smarter.
