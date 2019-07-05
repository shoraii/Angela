import discord
from random import choice
from gtts import gTTS

async def report_no_role(ctx):
    await ctx.send("You don't have enough permissions to execute this command.")


async def report_rude(ctx):
    await ctx.send("Shut up.")


async def report_no_voice_channel(ctx):
    await ctx.send("You are not connected to any voice chat.")


async def joined_voice_channel(ctx, channel):
    await ctx.send(f"I joined {channel}!")


async def left_voice_channel(ctx, channel):
    await ctx.send(f"I left {channel}!")


async def no_channel_to_leave(ctx):
    await ctx.send("I was told to leave voice channel, but was not in one")


def generate_greetings(filename):
    greetings = [
        'Hi there!',
        "What's up, fellows!",
        "How are you doing?",
        "Hey everyone!"
    ]
    tts = gTTS(choice(greetings))
    tts.save(filename)


def generate_phrase(filename, phrase):
    tts = gTTS(phrase)
    tts.save(filename)