# youtube-whisper-transcriber
This Python script automates the process of transcribing YouTube video audio. It leverages yt-dlp to efficiently download the audio stream of a specified YouTube URL, and then uses mlx-whisper (or standard OpenAI Whisper) to generate a full transcript.

Features

YouTube Integration: Uses yt-dlp to reliably fetch audio in MP3 format.

High-Quality Transcription: Utilizes the powerful OpenAI Whisper model via the mlx-whisper library for accurate transcription.

Automatic Cleanup: Removes temporary audio and raw output files after transcription is complete.

Portable Output: Saves the final, cleaned transcript to a dedicated output folder.

Prerequisites:
You must have the following tools installed on your system:
Python 3.x: Installed and accessible from your command line.
yt-dlp: The highly flexible YouTube-DL successor for media downloading.

# Installation may vary by OS. Check official yt-dlp docs.
# On macOS/Linux:
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp

Required Python Libraries:
pip install mlx-whisper # For the transcription model
# You may also need other dependencies, depending on your system

Installation and Setup:
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME

Install Python requirements:
pip install mlx-whisper

(Optional) Configuration: Open the script Audio_to_Text_OAI_Whisper.py and review the configuration section near the top.
# --- Configuration ---
# 1. Path to the audio download directory. 
#    This will create a folder named 'transcribed_audio' in the directory where the script is run.
DOWNLOAD_DIR = os.path.join(os.getcwd(), "transcribed_audio") 
# 2. Your target model name (e.g., "mlx-community/whisper-base-mlx", or "mlx-community/whisper-large-v3-mlx")
MODEL_ID = "mlx-community/whisper-base-mlx"

Usage:
To run the script, execute the Python file directly from your terminal. When prompted, paste the full URL of the YouTube video you wish to transcribe.
python Audio_to_Text_OAI_Whisper.py

The script will guide you through the process:

It will ask for the YouTube URL.
It will fetch the video title.
It will download the audio.
It will run the transcription using the configured Whisper model.
It will save the final, cleaned transcript as a .txt file in the transcribed_audio folder.
It will delete the temporary audio and raw output files.

Example Output:
Enter the YouTube URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Fetching video title...
Title: Rick Astley - Never Gonna Give You Up (Official Music Video)
--- Starting Audio Download (yt-dlp) ---
... Download progress ...
Audio downloaded successfully.
--- Starting MLX-Whisper Transcription (Model: mlx-community/whisper-base-mlx) ---
Raw transcription complete.
Cleaned and saved final transcript to: ./transcribed_audio/Rick_Astley_-_Never_Gonna_Give_You_Up_(Official_Music_Video)_clean.txt
Cleaned up temporary files from ./transcribed_audio.

Contributing:
Contributions are welcome! If you have suggestions for new features, bug fixes, or improvements, please feel free to open an issue or submit a pull request.

License:
This project is licensed under the MIT License.

