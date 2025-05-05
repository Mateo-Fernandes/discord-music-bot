

# Discord Music Bot

A feature-rich Discord bot locally based for playing music from YouTube in voice channels. Search for songs by name or use direct YouTube URLs, queue tracks, and control playback with simple commands. When multiple songs match a search, the bot prompts users to select from the top 5 YouTube results, with a 30-second timeout. Built with Python using `discord.py` and `yt-dlp`, this bot is easy to set up and customize. Includes a `requirements.txt` for dependencies and a secure `.env` for token storage. Perfect for music lovers and server admins looking to enhance their Discord experience! 

---

## Features

- **Play Music:** Play songs from YouTube URLs or by searching song names (e.g., `.play Happy`).
- **Song Selection:** If a search query returns multiple results, the bot lists the top 5 YouTube results and prompts the user to choose one by typing a number (1-5). The selection times out after 30 seconds, defaulting to the first result.
- **Queue System:** Add songs to a queue, view the queue, or clear it.
- **Playback Controls:** Pause, resume, or stop playback and disconnect the bot from the voice channel.
- **Error Handling:** Gracefully handles errors like invalid inputs, no search results, or playback issues.

---

## Prerequisites

- **Python 3.8+**: Ensure Python is installed on your system.
- **Discord Bot Token**: Obtain a bot token from the [Discord Developer Portal](https://discord.com/developers/applications).
- **FFmpeg**: Required for audio playback.
  - **Windows:** Download from the FFmpeg website and add to PATH.
  - **Linux:** `sudo apt-get install ffmpeg` (Ubuntu/Debian) or equivalent.
  - **macOS:** `brew install ffmpeg` (with Homebrew).

---

## Installation

### 1. Clone or Download the Repository

```bash
git clone https://github.com/Mateo-Fernandes/discord-music-bot
cd 
```

**Alternatively:** Download `main.py`, `harmony.py`, `requirements.txt`, and create a `.env` file.

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project directory with your Discord bot token:

```
discord_token=your_bot_token_here
```

> **Warning:** Do not share your `.env` file or commit it to a public repository, as it contains sensitive information (your bot token).

### 4. Invite the Bot to Your Server

1. In the Discord Developer Portal, go to your bot's application, select "OAuth2" > "URL Generator."
2. Choose the `bot` scope and grant permissions: Send Messages, Read Messages/View Channels, Connect, Speak.
3. Copy the generated URL, open it in a browser, and invite the bot to your server.

---

## Usage

### Run the Bot

```bash
python main.py
```

The bot loads the token from `.env` using `python-dotenv` and connects to Discord, logging `{bot_name} is now jamming` in the console.

### Join a Voice Channel

Ensure you are in a voice channel before using music commands. The bot will join your voice channel when you run the `.play` command.

### Use Commands

Commands are prefixed with `.` (e.g., `.play`). See the [Commands](#commands) section for details.

---

## Commands

| Command           | Description                                                                                          | Example                                         |
|-------------------|------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| `.play `    | Plays a song from a YouTube URL or searches for a song by name. If multiple results are found, prompts for selection (30-second timeout). | `.play Happy``.play https://youtu.be/ZbZSe6N_BXs` |
| `.queue `   | Adds a song (URL or name) to the queue.                                                              | `.queue Happy`                                  |
| `.show_queue`     | Displays the current queue.                                                                          | `.show_queue`                                   |
| `.clear_queue`    | Clears the queue.                                                                                    | `.clear_queue`                                  |
| `.pause`          | Pauses the currently playing song.                                                                   | `.pause`                                        |
| `.resume`         | Resumes the paused song.                                                                             | `.resume`                                       |
| `.stop`           | Stops playback and disconnects the bot from the voice channel.                                       | `.stop`                                         |

---

## Song Selection Example

When you run `.play Happy`:

If multiple results are found, the bot sends a message like:

> Multiple songs found for 'Happy'. Please select one by typing the number (1-5):  
> 1. Pharrell Williams - Happy (Official Music Video) (Pharrell Williams)  
> 2. Happy - Despicable Me 2 (Minions)  
> 3. Happy (Live Performance) (Some Artist)  
> 4. Happy (Cover) (Cover Artist)  
> 5. Happy (Remix) (DJ Remix)

Type a number (e.g., `1`) to select a song. If no response is received within 30 seconds or the input is invalid, the bot plays the first result.

---

## Project Structure

- `main.py`: Entry point that imports and runs the bot from `harmony.py`.
- `harmony.py`: Core bot implementation, including commands and music playback logic.
- `requirements.txt`: Lists Python dependencies (`discord.py`, `yt-dlp`, `PyNaCl`, `python-dotenv`).
- `.env`: Stores the Discord bot token, loaded at the start of the bot using `python-dotenv`. **Do not include in version control.**

---

## Notes

- **Top 5 Results:** The song selection feature uses the first five YouTube search results, ranked by YouTube's algorithm (based on relevance, popularity, etc.), not strictly by view count.
- **Token Security:** The `.env` file is loaded at the beginning of `harmony.py` using `load_dotenv()` to securely access the bot token.
- **Dependencies:** Ensure FFmpeg is installed and accessible in your system's PATH for audio playback. Python dependencies are listed in `requirements.txt`.
- **Permissions:** The bot requires permissions to send/read messages, connect to voice channels, and speak.
- **Timeout:** The song selection prompt times out after 30 seconds, defaulting to the first result.

---

## Troubleshooting

- **Bot Not Responding:** Check the console for errors, ensure the token in `.env` is correct, and verify the bot has the necessary permissions.
- **No Audio:** Ensure FFmpeg is installed and in your system's PATH.
- **No Search Results:** Verify your internet connection and ensure the search query is valid.
- **Dependency Issues:** Ensure all packages in `requirements.txt` are installed (`pip install -r requirements.txt`).
- **Errors:** Check the console for error messages. Common issues include missing dependencies or incorrect bot permissions.

---

Enjoy your enhanced Discord music experience!  
**Happy jamming!** 🎶


