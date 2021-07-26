import discord
from discord.ext import commands
import os
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from ytb_url import *

client = commands.Bot(command_prefix = '.')


class Counter:
    def __init__(self):
        self.i = 0
        self.j = 0

    def reset(self):
        self.i = 0
        self.j = 0


c = Counter()

audio_list = ['2h-ost.mp3', '1h-ost.mp3']

urls = []


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


@client.command()
async def ping(ctx):
  await ctx.send(f'ping : {round(client.latency * 1000)} ms')


@client.command()
async def join(ctx):
  channel = client.get_channel(868526684406710352)
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice and voice.is_connected():
    await voice.move_to(channel)
  else:
    voice = await channel.connect(reconnect=True)


@client.command()
async def play_url(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('Bot is playing')


@client.command()
async def search_video(ctx, r_sep, n_v_str):
    r = r_sep.replace("-", " ")
    titles_r, urls_r = get_urls(r, int(n_v_str))
    for title in titles_r:
        await ctx.send(str(titles_r.index(title) + 1) + ": " + str(title))
    urls.extend(urls_r)


@client.command()
async def add_url(ctx, url):
    urls.append(url)
    print(f'{url} succesfully added to playlist!')


@client.command()
async def show_urls(ctx):
    print(urls)
    await ctx.send(str(urls))


@client.command()
async def show_url(ctx):
    print(urls[c.j % len(urls)])
    await ctx.send(urls[c.j % len(urls)])


@client.command()
async def next_url(ctx):
    await pause(ctx)
    c.j += 1
    await play_urls(ctx)


@client.command()
async def play_urls(ctx):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    url = urls[c.j % len(urls)]

    def next_url(urls, voice, YDL_OPTIONS, FFMPEG_OPTIONS):
        c.j += 1
        url = urls[c.j % len(urls)]
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: next_url(urls, voice, YDL_OPTIONS, FFMPEG_OPTIONS))
        voice.is_playing()
        print('Now playing : ' + url)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: next_url(urls, voice, YDL_OPTIONS, FFMPEG_OPTIONS))
        voice.is_playing()
        print('Now playing : ' + url)
        await ctx.send('Bot is playing')


async def send_message(ctx, msg):
    await ctx.send(msg)


@client.command()
async def play_files(ctx):
    guild = ctx.guild
    voice: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=guild)
    audio = discord.FFmpegPCMAudio(audio_list[0])
    audio_name = audio_list[c.i]

    channel = ctx.author.voice.channel

    #  if not voice_client.is_playing():
    #  voice_client.play(audio_source, after=None)

    def repeat(guild, voice, audio):
        voice.play(audio, after=lambda e: repeat(guild, voice, audio))
        voice.is_playing()

    def next(guild, voice, audio_list):
        c.i += 1
        audio = discord.FFmpegPCMAudio(audio_list[c.i % len(audio_list)])
        audio_name = audio_list[c.i % len(audio_list)]
        voice.play(audio, after=lambda e: next(guild, voice, audio_list))
        voice.is_playing()
        send_message(ctx, f'Playing {audio_name}')

    if channel and not voice.is_playing():
        voice.play(audio, after=lambda e: next(ctx.guild, voice, audio_list))
        voice.is_playing()
        await ctx.send(f'Playing {audio_name}')


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is resuming')


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
        urls.clear()
        await ctx.send('Stopping...')


@client.command()
async def leave(ctx):
    await ctx.message.guild.voice_client.disconnect()


@client.command()
async def show_files(ctx):
    await ctx.send(audio_list)


@client.command()
async def now_playing(ctx):
    await ctx.send(audio_list[c.i])


@client.command()
async def restart(ctx):
    await stop(ctx)
    await leave(ctx)
    c.reset()


token = os.environ['token']


client.run('ODY4Mzc1NTY4ODM0NTAyNjc2.YPuvxQ.0UUjG7WMUBlrbAuRlFQMTKnf1bk')
