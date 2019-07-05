import discord
from gtts import gTTS
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
from botsettings import *
from utility import *
from feedback import *

bot = commands.Bot(command_prefix='Angela, ', description='Your attentive assistant.')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def bravo(ctx):
    if not has_role(ctx, USER_ROLE_NAME):
        return await report_no_role(ctx)
    await ctx.send('Thanks!')


@bot.command()
async def helpx(ctx):
    if not has_role(ctx, USER_ROLE_NAME):
        return await report_no_role(ctx)
    embed = discord.Embed(title="**Angela** bot list of commands:", color=0xFFFDCD)

    embed.add_field(name="helpx", value="Returns this list", inline=False)
    embed.add_field(name="play <YT video/playlist link>", value="Plays or puts in queue a YouTube video", inline=False)
    embed.add_field(name="s <ID>", value="Old soundboard", inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def shutdown(ctx):
    if not has_role(ctx, MOD_ROLE_NAME):
        return await report_no_role(ctx)
    await bot.logout()


@bot.command()
async def clear(ctx):
    if not has_role(ctx, MOD_ROLE_NAME):
        return await report_no_role(ctx)
    channel = ctx.message.channel
    async for message in channel.history(limit=200):
        await message.delete()


@bot.command()
async def join(ctx):
    if not has_role(ctx, USER_ROLE_NAME):
        return await report_no_role(ctx)
    voice_status = ctx.message.author.voice
    channel = voice_status.channel
    if channel is not None:
        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await voice.disconnect()

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await joined_voice_channel(ctx, channel)

        fname = GREETINGS_FILENAME
        generate_greetings(fname)
        voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=fname))
    else:
        await report_no_voice_channel()


@bot.command()
async def leave(ctx):
    if not has_role(ctx, USER_ROLE_NAME):
        return await report_no_role(ctx)
    voice_status = ctx.message.author.voice
    channel = voice_status.channel
    if channel is not None:
        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
            await left_voice_channel(ctx, channel)
        else:
            await no_channel_to_leave(ctx)
    else:
        await report_no_voice_channel()


@bot.command()
async def say(ctx, what):
    if not has_role(ctx, USER_ROLE_NAME):
        return await report_no_role(ctx)
    if len(what) > 90:
        return await report_rude(ctx)
    voice_status = ctx.message.author.voice
    channel = voice_status.channel
    if channel is not None:
        voice = get(bot.voice_clients, guild=ctx.guild)
        fname = GREETINGS_FILENAME
        generate_phrase(fname, what)
        voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=fname))
    else:
        await report_no_voice_channel()


@bot.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing failed pause")


@bot.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")


@bot.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")


@bot.command(pass_context=True, aliases=['p', 'pla'])
async def yt(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3") and file != GREETINGS_FILENAME:
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.05

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")


@bot.command()
async def vol(ctx, new_v: float):
    if not has_role(ctx, USER_ROLE_NAME):
        return await report_no_role(ctx)
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.source.volume = new_v


bot.run(TOKEN)