import os
import subprocess
import re

# --- Configuration ---
DOWNLOAD_DIR = os.path.join(os.getcwd(), "transcribed_audio") 
# Small-mlx handles "Deinococcus" and "Bacillus" much better than Base 
MODEL_ID = "mlx-community/whisper-small-mlx" 

def clean_title(title: str) -> str:
    """Removes characters unsafe for filenames."""
    safe_title = re.sub(r'[\\/:*?"<>|]+', '_', title)
    safe_title = re.sub(r'^\.|\.$', '', safe_title).strip()
    return safe_title[:100].strip()

def get_video_title(youtube_url: str) -> str | None:
    """Uses yt-dlp to fetch the video title."""
    print(f"Fetching title for: {youtube_url}")
    # Using --get-title for simplicity
    title_command = ['yt-dlp', '--skip-download', '--get-title', youtube_url]
    try:
        result = subprocess.run(title_command, capture_output=True, text=True, check=True)
        return clean_title(result.stdout.strip())
    except Exception as e:
        print(f"Error fetching title: {e}")
        return "youtube_transcript"

def clean_transcript_file(raw_path: str, final_path: str):
    """Removes timestamps, standalone 'Music' tags, and repetition loops."""
    print("--- Cleaning Transcript & Removing Hallucinations ---")
    timestamp_pattern = re.compile(r'\[\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}\.\d{3}\]')
    
    clean_segments = []
    last_line = ""

    try:
        with open(raw_path, 'r', encoding='utf-8') as raw_file:
            for line in raw_file:
                # 1. Strip timestamp
                text = timestamp_pattern.sub('', line).strip()
                
                # 2. Skip technical junk and music-only lines [cite: 1, 74]
                if not text or "Detecting language" in text or text.startswith("Args:"):
                    continue
                
                # REJECTION LOGIC:
                # Remove if the line is ONLY the word "Music"
                if re.fullmatch(r'\[?Music\]?\.?', text, re.IGNORECASE):
                    continue
                
                # Remove if it's a direct repetition (hallucination guard) 
                if text.lower() == last_line.lower():
                    continue
                
                clean_segments.append(text)
                last_line = text

        with open(final_path, 'w', encoding='utf-8') as final_file:
            final_file.write(" ".join(clean_segments))
            
    except Exception as e:
        print(f"Cleaning error: {e}")

def transcribe_youtube_url(url: str):
    """Main workflow using WAV for maximum accuracy."""
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    video_title = get_video_title(url)
    
    base_path = os.path.join(DOWNLOAD_DIR, video_title)
    audio_wav = f"{base_path}.wav" 
    raw_txt = f"{base_path}_raw.txt"
    final_txt = f"{base_path}_clean.txt"

    # 1. Download as WAV (Higher quality for the AI)
    print("--- Downloading Audio (.wav) ---")
    subprocess.run(f'yt-dlp -x --audio-format wav --audio-quality 0 "{url}" -o "{audio_wav}"', shell=True, check=True)

    # 2. Transcribe (Locking language to English reduces hallucinations) 
    print(f"--- Transcribing with {MODEL_ID} ---")
    # Using the raw path redirection to capture the output correctly
    subprocess.run(f'mlx_whisper "{audio_wav}" --model "{MODEL_ID}" --language en > "{raw_txt}"', shell=True, check=True)

    # 3. Clean
    clean_transcript_file(raw_txt, final_txt)
    
    # 4. Cleanup
    if os.path.exists(audio_wav): os.remove(audio_wav)
    if os.path.exists(raw_txt): os.remove(raw_txt)
    print(f"\nSuccess! Transcript saved to: {final_txt}")

if __name__ == "__main__":
    link = input("Enter YouTube URL: ").strip()
    if link:
        transcribe_youtube_url(link)