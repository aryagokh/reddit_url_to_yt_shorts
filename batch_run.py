import csv
import subprocess
import os
import time

CSV_PATH = "daily_jobs.csv"

def get_input(prompt, default=None, required=False):
    """Take input with default fallback."""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    while True:
        val = input(prompt).strip()
        if val:
            return val
        elif default is not None:
            return default
        elif required:
            print("⚠️ This field is required!")
        else:
            return ""

def main():
    start_time = time.time()
    print("\n🎬 === DAILY REDDIT SHORT JOB COLLECTOR ===")
    print("Press 'q' anytime to finish and start run.py\n")

    # CSV header
    header = [
        "url", "post_number", "post_type", "short_speed",
        "words_per_caption", "model",
        "video_category", "video_base_folder"
    ]
    
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)

    while True:
        url = get_input("Reddit URL (or 'q' to quit): ", required=True)
        if url.lower() == "q":
            break

        post_number = get_input("Post number (e.g. test_1)", required=True)
        post_type = get_input("Post type-gender or gender (e.g. motivational-male)", required=True)
        short_speed = get_input("Short speed", "1.3")
        words_per_caption = get_input("Words per caption", "1")
        model = get_input("Model", "gemini-2.5-pro")
        video_category = get_input("Video category", "gameplay")      # particular subfolder in video_base_folder which has all the videos
        video_base_folder = get_input("Video base folder", "E:/YouTube/videos") # where all subfolders are saved

        with open(CSV_PATH, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                url, post_number, post_type, short_speed,
                words_per_caption, model,
                video_category, video_base_folder
            ])

        print(f"✅ Added: {url} ({post_number})")

    print("\n📁 All jobs saved to", CSV_PATH)
    print("🚀 Starting all jobs...\n")

    with open(CSV_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"▶️ Running job: {row['post_number']} ...")
            try:
                subprocess.run([
                    "python", "run.py",
                    "--url", row["url"],
                    "--post-number", row["post_number"],
                    "--post-type", row["post_type"],
                    "--short-speed", row["short_speed"],
                    "--words-per-caption", row["words_per_caption"],
                    "--model", row["model"],
                    "--video-category", row["video_category"],
                    "--video-base-folder", row["video_base_folder"],
                ])
            except subprocess.CalledProcessError:
                print(f"❌ Failed: {row['post_number']}")
            print("───────────────────────────────"*4)

    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)
        print(f"\n🧹 Cleaned up — deleted {CSV_PATH}")

    print("\n🎉 All queued jobs complete and CSV removed!")
    end_time = time.time()

    elapsed_time = end_time - start_time
    minutes, seconds = divmod(elapsed_time, 60)

    print("Complete batch run successful!!")
    print(f"Time taken: {int(minutes)} minute(s) and {seconds:.2f} second(s)")
    print("——————————————————————————— Completed Gracefully! ———————————————————————————")

if __name__ == "__main__":
    main()