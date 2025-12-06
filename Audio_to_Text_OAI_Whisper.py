import os
import subprocess
import shutil
import re

# --- Configuration ---
# 1. Path to the audio download directory. 
#    This will create a folder named 'transcribed_audio' in the directory where the script is run.
DOWNLOAD_DIR = os.path.join(os.getcwd(), "transcribed_audio") 
# 2. Your target model name
MODEL_ID = "mlx-community/whisper-base-mlx"


def clean_title(title: str) -> str:
    """Removes characters unsafe for filenames and shortens the title."""
    # Remove characters that are illegal or problematic in filenames
    safe_title = re.sub(r'[\\/:*?"<>|]+', '_', title)
    # Remove leading/trailing periods or spaces
    safe_title = re.sub(r'^\.|\.$', '', safe_title).strip()
    # Limit the length to prevent excessively long file names
    return safe_title[:100].strip()


def get_video_title(youtube_url: str) -> str | None:
    """Uses yt-dlp to fetch the video title without downloading the video."""
    print("Fetching video title...")
    
    # Command uses --print "%(title)s" and --skip-download
    title_command = [
        'yt-dlp', 
        '--skip-download', 
        '--print', 
        '%(title)s', 
        youtube_url
    ]
    
    try:
        # Capture the output, which should be just the title
        result = subprocess.run(
            title_command, 
            capture_output=True, 
            text=True, 
            check=True
        )
        # The title is the first line of standard output
        raw_title = result.stdout.strip().split('\n')[0]
        return clean_title(raw_title)
        
    except subprocess.CalledProcessError as e:
        print(f"Error fetching title with yt-dlp: {e.stderr.strip()}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while fetching title: {e}")
        return None


def clean_transcript_file(raw_path: str, final_path: str):
    """Reads the raw transcript and removes all timestamp markers."""
    print("--- Cleaning raw transcript for pure text output ---")
    
    # Regex pattern to identify and remove the timestamp marker: [00:00.000 --> 00:00.000]
    timestamp_pattern = re.compile(r'\[\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}\.\d{3}\]')
    
    clean_text = ""
    try:
        with open(raw_path, 'r', encoding='utf-8') as raw_file:
            for line in raw_file:
                # 1. Remove the timestamp marker from the line
                cleaned_line = timestamp_pattern.sub('', line).strip()

                # Filter out specific unwanted lines
                if cleaned_line.startswith("Args:") or "Detecting language" in cleaned_line or "Detected language:" in cleaned_line:
                    continue
                
                # 2. Rejoin segments with a space for continuous reading
                if cleaned_line:
                    clean_text += cleaned_line + " "

        # Write the final, clean text to the new file
        with open(final_path, 'w', encoding='utf-8') as final_file:
            final_file.write(clean_text.strip())
            
        print(f"Clean text successfully saved to: {final_path}")
        
    except Exception as e:
        print(f"Error during cleaning: {e}")


def transcribe_youtube_url(youtube_url: str):
    """Downloads audio, transcribes it, and saves the pure text using video title for names."""
    
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    # 1. Get the video title
    video_title = get_video_title(youtube_url)
    if not video_title:
        print("Cannot proceed without a valid video title.")
        return

    # 2. Define dynamic file paths
    base_file_path = os.path.join(DOWNLOAD_DIR, video_title)
    output_audio_path = f"{base_file_path}.mp3"
    raw_output_path = f"{base_file_path}_raw.txt" # Raw file (with timestamps)
    final_output_path = f"{base_file_path}_clean.txt" # Final file (pure text)
    
    print(f"--- Starting Workflow for Video: '{video_title}' ---")
    
    # 3. Command to download and extract audio
    download_command = (
        f'yt-dlp -x --audio-format mp3 "{youtube_url}" -o "{base_file_path}.%(ext)s"'
    )
    
    try:
        subprocess.run(download_command, shell=True, check=True)
        print("Audio downloaded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during audio download/extraction: {e.stderr.strip()}")
        return

    # 4. Command to Transcribe using MLX-Whisper/Whisper 
    print(f"--- Starting MLX-Whisper Transcription (Model: {MODEL_ID}) ---")
    
    # Output is redirected to the temporary RAW file
    transcribe_command = (
        f'mlx_whisper "{output_audio_path}" --model "{MODEL_ID}" > "{raw_output_path}"'
    )
    
    try:
        subprocess.run(transcribe_command, shell=True, check=True)
        print("Raw transcription complete.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error during Whisper transcription: {e.stderr.strip()}")
        return

    # 5. Clean and Finalize Output
    clean_transcript_file(raw_output_path, final_output_path)

    # 6. Clean up temporary files
    try:
        os.remove(output_audio_path)
        os.remove(raw_output_path) 
        print(f"\nCleaned up temporary files from {DOWNLOAD_DIR}.")
    except Exception as e:
        print(f"Warning: Could not remove temporary files. {e}")


if __name__ == "__main__":
    video_link = input("Please enter the YouTube URL: ").strip()
    if video_link:
        transcribe_youtube_url(video_link)
    else:
        print("No URL provided. Exiting.")   