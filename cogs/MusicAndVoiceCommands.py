import disnake as discord
from disnake.ext import commands
from disnake import Localized
import sqlite3
from youtube_dl import YoutubeDL

import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

import random

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite MusicAndVoiceCommands] database.db загружен!")

YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'False', 'simulate': 'True',
               'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

r = sr.Recognizer()

def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text

class MusicAndVoiceCommands(commands.Cog):
    def __init__(self, bot):
        client = bot
    
    @commands.slash_command(description=Localized("Play music", key="VOICE_PLAY_DESCRIPTION"))
    async def voice_play(ctx, url: str):
        cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
        langCode = cursor.fetchone()
        langCodeStr = str(langCode)
        langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')

        await ctx.response.defer()

        vc = await ctx.author.voice.channel.connect()
        
        with YoutubeDL(YDL_OPTIONS) as ydl:
            if 'https://' in url:
                info = ydl.extract_info(url, download=False)
            else:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
        
        url = info['formats'][0]['url']
        
        vc.play(discord.FFmpegPCMAudio(executable="C:\\ffmpeg\\bin\\ffmpeg.exe", source=url, **FFMPEG_OPTIONS))

        if langCodeReal == "ru":
            await ctx.send(f"Начинаю проигрывать музыку", ephemeral=True)
        if langCodeReal == "en":
            await ctx.send(f"I'm playing music now", ephemeral=True)

    # @commands.slash_command(description=Localized("Developer testing", key="VOICE_BAD_WORD_FILTER_DESCRIPTION"))
    # async def voice_badword_filter(ctx):
    #     await ctx.response.defer()

    #     vc = await ctx.author.voice.channel.connect()
    #     await ctx.send("Я подключился к голосовому каналу. Начинаю анализировать звук", ephemeral=True)

    #     while True:
    #         content = vc.source
    #         print(vc)
    #         print(content)
    #         contentRead = content.read()
    #         with open(f'output-{random.randint(1, 2147483647)}.wav', 'w') as output:
    #             output.write(contentRead)


def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(MusicAndVoiceCommands(bot))