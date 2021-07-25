import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

client = commands.Bot(command_prefix = '.')

audio_list = ['2h-ost.mp3', '1h-ost.mp3']
i = 0

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


async def send_message(ctx, msg):
    await ctx.send(msg)

@client.command()
async def play_files(ctx):
    guild = ctx.guild
    voice: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=guild)
    audio = discord.FFmpegPCMAudio(audio_list[0])
    audio_name = audio_list[i]

    channel = ctx.author.voice.channel

    #if not voice_client.is_playing():
    #  voice_client.play(audio_source, after=None)

    def repeat(guild, voice, audio):
        voice.play(audio, after=lambda e: repeat(guild, voice, audio))
        voice.is_playing()

    def next(guild, voice, audio_list, i):
        i += 1
        audio = discord.FFmpegPCMAudio(audio_list[i % len(audio_list)])
        audio_name = audio_list[i % len(audio_list)]
        voice.play(audio, after=lambda e: next(guild, voice, audio_list, i))
        voice.is_playing()
        send_message(ctx, f'Playing {audio_name}')


    if channel and not voice.is_playing():
        voice.play(audio, after=lambda e: next(ctx.guild, voice, audio_list, i))
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
        await ctx.send('Stopping...')


@client.command()
async def leave(ctx):
    await ctx.message.guild.voice_client.disconnect()


@client.command()
async def show_files(ctx):
    await ctx.send(audio_list)


@client.command()
async def now_playing(ctx):
    await ctx.send(audio_list[i])


#token = os.environ['token']

token = 'ODY4Mzc1NTY4ODM0NTAyNjc2.YPuvxQ.s9IffCEjxPl03QpHHCv-PABzF1I'

#keep_alive()
client.run(token)







