# Discord Music Bot

A feature-rich Discord bot for playing music from YouTube in voice channels. Search for songs by name or use direct YouTube URLs, queue tracks, and control playback with simple commands. When multiple songs match a search, the bot prompts users to select from the top 5 YouTube results, with a 30-second timeout. Built with Python using `discord.py` and `yt-dlp`, this bot is easy to set up and customize. Includes a `requirements.txt` for dependencies and a secure `.env` for token storage. Perfect for music lovers and server admins looking to enhance their Discord experience!

## Features
- **Play Music**: Play songs from YouTube URLs or by searching song names (e.g., `.play Happy`).
- **Song Selection**: If a search query returns multiple results, the bot lists the top 5 YouTube results and prompts the user to choose one by typing a number (1-5). The selection times out after 30 seconds, defaulting to the first result.
- **Queue System**: Add songs to a queue, view the queue, or clear it.
- **Playback Controls**: Pause, resume, or stop playback and disconnect the bot from the voice channel.
- **Error Handling**: Gracefully handles errors like invalid inputs, no search results, or playback issues.

## Prerequisites
- **Python 3.8+**: Ensure Python is installed on your system.
- **Discord Bot Token**: Obtain a bot token from the [Discord Developer Portal](https://discord.com/developers/applications).
- **FFmpeg**: Required for audio playback. Install it on your system:
  - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html) and add to PATH.
  - **Linux**: `sudo apt-get install ffmpeg` (Ubuntu/Debian) or equivalent.
  - **macOS**: `brew install ffmpeg` (with Homebrew).

## Installation
1. **Clone or Download the Repository**:
   ```bash
   git clone https://github.com/Mateo-Fernandes/discord-music-bot
   cd <repository-directory>


