import os
import subprocess
import re

# --- Configuration ---
DOWNLOAD_DIR = os.path.join(os.getcwd(), "transcribed_audio") 
# Small is the "sweet spot" for speed vs. scientific accuracy (e.g., Bacillus subtilis)
MODEL_ID = "mlx-community/whisper-small-mlx" 

def clean_title(title: str) -> str:
    """Removes characters unsafe for filenames and shortens the title."""
    safe_title = re.sub(r'[\\/:*?"<>|]+', '_', title)
    safe_title = re.sub(r'^\.|\.$', '', safe_title).strip()
    return safe_title[:100].strip()

def get_video_title(youtube_url: str) -> str | None:
    """Uses yt-dlp to fetch the video title."""
    print(f"Targeting: {youtube_url}")
    title_command = ['yt-dlp', '--skip-download', '--get-title', youtube_url]
    try:
        result = subprocess.run(title_command, capture_output=True, text=True, check=True)
        return clean_title(result.stdout.strip())
    except Exception as e:
        print(f"Error fetching title: {e}")
        return "youtube_transcript"

def process_transcript(raw_path: str, final_path: str):
    """Filters out timestamps, repetitive hallucinations, and music tags."""
    print("--- Refining Transcript & Removing Loops ---")
    timestamp_pattern = re.compile(r'\[\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}\.\d{3}\]')
    
    unique_lines = []
    last_line = ""

    try:
        with open(raw_path, 'r', encoding='utf-8') as f:
            for line in f:
                # 1. Remove timestamps and junk
                text = timestamp_pattern.sub('', line).strip()
                
                # 2. Skip technical headers and music tags
                if not text or any(x in text for x in ["Args:", "Detecting language", "Music"]):
                    continue
                
                # 3. Hallucination Guard: Skip if line is a near-duplicate of the last
                # This stops the "star-spirited" and "beautiful space" loops
                if text.lower() == last_line.lower():
                    continue
                
                unique_lines.append(text)
                last_line = text

        with open(final_path, 'w', encoding='utf-8') as f:
            f.write(" ".join(unique_lines))
        print(f"Final text saved: {final_path}")
    except Exception as e:
        print(f"Processing error: {e}")

def run_workflow(url: str):
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    title = get_video_title(url)
    
    base_path = os.path.join(DOWNLOAD_DIR, title)
    audio_wav = f"{base_path}.wav"  # WAV is native for Whisper
    raw_txt = f"{base_path}_raw.txt"
    clean_txt = f"{base_path}_clean.txt"

    # Step 1: Download Audio (WAV 16kHz Mono is optimal for AI)
    print("--- Downloading High-Quality Audio ---")
    dl_cmd = f'yt-dlp -x --audio-format wav --audio-quality 0 "{url}" -o "{audio_wav}"'
    subprocess.run(dl_cmd, shell=True, check=True)

    # Step 2: Transcribe via MLX
    print(f"--- Transcribing with {MODEL_ID} ---")
    # Added --language en to prevent the model from guessing wrong during silence
    tx_cmd = f'mlx_whisper "{audio_wav}" --model "{MODEL_ID}" --language en > "{raw_txt}"'
    subprocess.run(tx_cmd, shell=True, check=True)

    # Step 3: Clean and Cleanup
    process_transcript(raw_txt, clean_txt)
    
    # Cleanup temporary files
    for f in [audio_wav, raw_txt]:
        if os.path.exists(f): os.remove(f)
    print("Workflow Complete.")

if __name__ == "__main__":
    link = input("Enter YouTube URL: ").strip()
    if link: run_workflow(link)