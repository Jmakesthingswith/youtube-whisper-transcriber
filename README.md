# YouTube Whisper Transcriber

## Project Overview

This Python script automates the process of transcribing YouTube video audio. It leverages **`yt-dlp`** to efficiently download the audio stream of a specified YouTube URL, and then uses **`mlx-whisper`** (or standard OpenAI Whisper) to generate a full transcript.

This is ideal for quickly creating text versions of long-form videos, podcasts, lectures, or meetings hosted on YouTube.

---

## Features

* **YouTube Integration:** Uses `yt-dlp` to reliably fetch audio in MP3 format.
* **High-Quality Transcription:** Utilizes the powerful OpenAI Whisper model via the `mlx-whisper` library for accurate transcription.
* **Automatic Cleanup:** Removes temporary audio and raw output files after transcription is complete.
* **Portable Output:** Saves the final, cleaned transcript to a dedicated output folder.

---

## Prerequisites

You must have the following tools installed on your system:

1.  **Python 3.x:** Installed and accessible from your command line.
2.  **`yt-dlp`:** The highly flexible YouTube-DL successor for media downloading.
    ```bash
    # Installation may vary by OS. Check official yt-dlp docs.
    # On macOS/Linux (Example):
    sudo curl -L [https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp) -o /usr/local/bin/yt-dlp
    sudo chmod a+rx /usr/local/bin/yt-dlp
    ```
3.  **Required Python Libraries:**
    ```bash
    pip install mlx-whisper
    # Note: 'mlx-whisper' may have specific dependencies for certain systems (like MLX for Apple Silicon Macs). 
    # Depending on your system, if mlx is not the installed whisper model, remember to change that in the config section         referred to below "MODEL_ID ="
    # Check the whisper documentation for your environment.
    ```

---

## Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Jmakesthingswith/youtube-whisper-transcriber.git
    cd youtube-whisper-transcriber
    ```
2.  **Install Python requirements:**
    ```bash
    pip install mlx-whisper
    ```
3.  **Configuration (Portable Paths):**
    Ensure the `DOWNLOAD_DIR` path in the `Audio_to_Text_OAI_Whisper.py` file is set for portability:

    ```python
    import os
    # ... other imports
    
    # This creates a 'transcribed_audio' folder wherever the script is run.
    DOWNLOAD_DIR = os.path.join(os.getcwd(), "transcribed_audio") 
    MODEL_ID = "mlx-community/whisper-base-mlx"
    ```

---

## Usage

To run the script, execute the Python file directly from your terminal:

```bash
python Audio_to_Text_OAI_Whisper.py
```
The script will prompt you to enter the YouTube URL.

Example Output:

```bash
Enter the YouTube URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Fetching video title...
Title: Rick Astley - Never Gonna Give You Up (Official Music Video)
--- Starting Workflow for Video: 'Rick Astley - Never Gonna Give You Up (Official Music Video)' ---
Audio downloaded successfully.
--- Starting MLX-Whisper Transcription (Model: mlx-community/whisper-base-mlx) ---
Raw transcription complete.
--- Cleaning raw transcript for pure text output ---
Clean text successfully saved to: ./transcribed_audio/Rick_Astley_-_Never_Gonna_Give_You_Up_(Official_Music_Video)_clean.txt
Cleaned up temporary files from transcribed_audio.
