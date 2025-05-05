# Import required libraries
import discord  # Discord API wrapper for interacting with Discord
from discord.ext import commands  # Commands framework for Discord bot
import os  # For accessing environment variables
import asyncio  # For handling asynchronous operations
import yt_dlp  # For downloading and extracting YouTube audio streams
from dotenv import load_dotenv  # For loading environment variables from .env file
import urllib.parse, urllib.request, re  # For constructing and parsing YouTube search URLs

def run_bot():
    # Load environment variables from .env file (e.g., Discord bot token)
    load_dotenv()
    TOKEN = os.getenv('discord_token')  # Retrieve Discord bot token from .env

    # Set up bot intents (permissions and capabilities)
    intents = discord.Intents.default()
    intents.message_content = True  # Enable reading message content
    client = commands.Bot(command_prefix=".", intents=intents)  # Initialize bot with '.' prefix

    # Initialize dictionaries to store queues and voice clients for each guild
    queues = {}  # Stores song queues per guild (server)
    voice_clients = {}  # Stores voice client connections per guild

    # Define YouTube URLs for searching and playing videos
    youtube_base_url = 'https://www.youtube.com/'
    youtube_results_url = youtube_base_url + 'results?'  # URL for search results
    youtube_watch_url = youtube_base_url + 'watch?v='  # URL for specific videos

    # Configure yt-dlp options for extracting audio
    yt_dl_options = {"format": "bestaudio/best"}  # Select best audio quality
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)  # Initialize yt-dlp with options

    # Configure FFmpeg options for audio playback
    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',  # Handle stream reconnection
        'options': '-vn -filter:a "volume=0.25"'  # Disable video, set volume to 25%
    }

    @client.event
    async def on_ready():
        # Event triggered when the bot is fully connected to Discord
        print(f'{client.user} is now jamming')  # Log bot's username to console

    async def play_next(ctx):
        """
        Plays the next song in the queue for the guild.
        Args:
            ctx: Command context (contains guild, channel, etc.)
        """
        if queues[ctx.guild.id] != []:  # Check if queue is not empty
            link = queues[ctx.guild.id].pop(0)  # Remove and get the next song
            await play(ctx, link=link)  # Play the next song

    async def prompt_song_selection(ctx, search_results, query):
        """
        Prompts the user to select a song from multiple YouTube search results.
        Args:
            ctx: Command context
            search_results: List of YouTube video IDs from search
            query: Original search query (song name)
        Returns:
            Selected video ID or first result if selection fails
        """
        # Create a message listing up to 5 search results
        message = f"Multiple songs found for '{query}'. Please select one by typing the number (1-5):\n"
        for i, video_id in enumerate(search_results[:5], 1):  # Limit to top 5 results
            # Fetch video metadata (title, uploader) using yt-dlp
            info = await asyncio.get_event_loop().run_in_executor(
                None, lambda: ytdl.extract_info(f"{youtube_watch_url}{video_id}", download=False)
            )
            message += f"{i}. {info['title']} ({info['uploader']})\n"  # Add title and uploader to message

        # Send the selection prompt to the Discord channel
        selection_msg = await ctx.send(message)

        def check(m):
            # Check if the response is from the command author, in the same channel, and a valid number (1-5)
            return m.author == ctx.author and m.channel == ctx.channel and m.content in ['1', '2', '3', '4', '5']

        try:
            # Wait for user response (timeout after 30 seconds)
            response = await client.wait_for('message', check=check, timeout=30.0)
            selected_index = int(response.content) - 1  # Convert response to index (0-based)
            return search_results[selected_index]  # Return selected video ID
        except asyncio.TimeoutError:
            # If user doesn't respond in time, default to first result
            await selection_msg.edit(content="Selection timed out. Playing first result.")
            return search_results[0]
        except ValueError:
            # If user enters invalid input, default to first result
            await selection_msg.edit(content="Invalid selection. Playing first result.")
            return search_results[0]

    @client.command(name="play")
    async def play(ctx, *, link):
        """
        Plays a song from a YouTube URL or searches for a song by name.
        Args:
            ctx: Command context
            link: YouTube URL or song name to search
        """
        try:
            # Initialize queue for guild if it doesn't exist
            if ctx.guild.id not in queues:
                queues[ctx.guild.id] = []

            # Connect to voice channel if not already connected
            if not ctx.voice_client:
                voice_client = await ctx.author.voice.channel.connect()  # Join user's voice channel
                voice_clients[voice_client.guild.id] = voice_client  # Store voice client
            else:
                voice_client = ctx.voice_client  # Use existing voice client

            # If input is not a YouTube URL, treat it as a search query
            if youtube_base_url not in link:
                # Construct YouTube search URL
                query_string = urllib.parse.urlencode({'search_query': link})
                content = urllib.request.urlopen(youtube_results_url + query_string)
                # Extract video IDs from search results using regex
                search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())

                # Handle case where no results are found
                if not search_results:
                    await ctx.send("No results found.")
                    return

                # If multiple results, prompt user to select one
                if len(search_results) > 1:
                    selected_video_id = await prompt_song_selection(ctx, search_results, link)
                    link = youtube_watch_url + selected_video_id  # Construct URL for selected video
                else:
                    link = youtube_watch_url + search_results[0]  # Use first result if only one

            # Extract audio stream URL using yt-dlp
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))
            song = data['url']  # Get direct audio stream URL
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)  # Create audio player

            def after_playing(err):
                # Callback function to play next song after current one finishes
                fut = asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop)
                try:
                    fut.result()
                except:
                    pass

            # Play the audio and notify user
            voice_clients[ctx.guild.id].play(player, after=after_playing)
            await ctx.send(f"Now playing: {data['title']}")

        except Exception as e:
            # Log and notify user of any errors
            print(e)
            await ctx.send("An error occurred while trying to play the song.")

    @client.command(name="queue")
    async def queue(ctx, *, url=None):
        """
        Adds a song to the queue.
        Args:
            ctx: Command context
            url: YouTube URL or song name to queue
        """
        if url is None:
            await ctx.send("Please provide a song name or link.")
            return

        # Initialize queue for guild if it doesn't exist
        if ctx.guild.id not in queues:
            queues[ctx.guild.id] = []
        queues[ctx.guild.id].append(url)  # Add song to queue
        await ctx.send("Added to queue!")

    @client.command(name="show_queue")
    async def show_queue(ctx):
        """
        Displays the current song queue.
        Args:
            ctx: Command context
        """
        # Check if queue exists and is not empty
        if ctx.guild.id not in queues or not queues[ctx.guild.id]:
            await ctx.send("The queue is currently empty.")
            return

        # Build and send queue list
        queue_list = queues[ctx.guild.id]
        response = "**Current Queue:**\n"
        for i, song in enumerate(queue_list, 1):
            response += f"{i}. {song}\n"
        await ctx.send(response)

    @client.command(name="clear_queue")
    async def clear_queue(ctx):
        """
        Clears the song queue.
        Args:
            ctx: Command context
        """
        if ctx.guild.id in queues:
            queues[ctx.guild.id].clear()  # Clear the queue
            await ctx.send("Queue cleared!")
        else:
            await ctx.send("There is no queue to clear.")

    @client.command(name="pause")
    async def pause(ctx):
        """
        Pauses the currently playing song.
        Args:
            ctx: Command context
        """
        try:
            voice_clients[ctx.guild.id].pause()  # Pause playback
            await ctx.send("Playback paused.")
        except Exception as e:
            print(e)
            await ctx.send("An error occurred while pausing.")

    @client.command(name="resume")
    async def resume(ctx):
        """
        Resumes the paused song.
        Args:
            ctx: Command context
        """
        try:
            voice_clients[ctx.guild.id].resume()  # Resume playback
            await ctx.send("Playback resumed.")
        except Exception as e:
            print(e)
            await ctx.send("An error occurred while resuming.")

    @client.command(name="stop")
    async def stop(ctx):
        """
        Stops playback and disconnects the bot from the voice channel.
        Args:
            ctx: Command context
        """
        try:
            voice_clients[ctx.guild.id].stop()  # Stop playback
            await voice_clients[ctx.guild.id].disconnect()  # Disconnect from voice channel
            del voice_clients[ctx.guild.id]  # Remove voice client from dictionary
            await ctx.send("Stopped and disconnected.")
        except Exception as e:
            print(e)
            await ctx.send("An error occurred while stopping.")

    # Start the bot with the provided token
    client.run(TOKEN)

# Run the bot
run_bot()