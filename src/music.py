import discord
from discord.ext import commands
import youtube_dl
import time
import youtube_search
from Variables import *
import threading
import asyncio
import random
import urllib.parse
import urllib.request
import socket
import urllib.error


class Music(commands.Cog):

    """
        todo:
            v queue function
            - searching music via youtube (make it show the top 5 results),
            - skipping function,
            v stop clears queue,
            V "?op all" plays all openings shuffled
            - help command
            - manually adding commands
    """

    def __init__(self, client: commands.Bot):
        self.client = client
        self.queue = []
        self.thread = False
        self.yt_search = {}

    def check_q(self):
        return len(self.queue) > 0

    @staticmethod
    def is_connected(ctx: discord.ext.commands.context.Context):
        connected = ctx.voice_client and ctx.voice_client.is_connected()
        return True if connected else False

    @staticmethod
    async def get_audio(url):
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            print(url2)
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        return source

    async def idle_speaker(self, ctx: discord.ext.commands.context.Context):
        while self.is_playing(ctx):
            time.sleep(1)
        await self.play_queue(ctx)

    def wait_for_idle(self, ctx: discord.ext.commands.context.Context):
        self.thread = True

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.idle_speaker(ctx))
        loop.close()
        self.thread = False

    async def play_queue(self, ctx: discord.ext.commands.context.Context):
        if not self.is_playing(ctx):
            audio = await self.get_audio(self.queue.pop(0))
            ctx.voice_client.play(audio)

        if len(self.queue) > 0:
            playing_t = threading.Thread(target=self.wait_for_idle, name="Song_Listener", args=[ctx])
            playing_t.start()

    @staticmethod
    def is_yt_link(query: str):
        # True if is a link
        if ('youtube.com' or 'youtu.be') in query:
            if not query.startswith('https://'):
                query = 'https://' + query
            try:
                urllib.request.urlopen(query)
                return True
            except (ValueError, socket.gaierror, urllib.error.URLError):
                return False

    @staticmethod
    def filter_query(query: str):
        filtered_query = urllib.parse.unquote(' '.join(query.split()[1:]))
        return filtered_query

    def simplify_query(self, query):
        new_query = self.filter_query(query)
        char_i = new_query.find('&')
        if char_i != -1:
            new_query = new_query[:char_i]
        return new_query

    @commands.command(name="play", pass_ctx=True)
    async def play(self, ctx: discord.ext.commands.context.Context, url=""):
        print(f"[*] - Play query received for: {url}")
        query = ctx.message.clean_content
        url = self.simplify_query(query)
        await self.handle_connected(ctx)

        if self.is_yt_link(url):
            self.queue.append(url)
            print(self.queue, self.is_playing(ctx))

            # send a message to inform that a song has been queued or being played
            await self.send_playing(ctx)
            if not self.thread:
                await self.play_queue(ctx)
        else:
            if not self.yt_search:
                self.yt_search = youtube_search.get_first_five_yts(url)
                await self.send_yt_search(ctx)
            else:
                try:
                    url = int(url)
                    if 1 <= url <= 5:
                        await self.play(ctx, self.yt_search[url]["url"])
                        self.yt_search = {}
                    else:
                        await self.invalid_pick(ctx)
                except ValueError:
                    await self.invalid_pick(ctx)

    @commands.command(name="spotify", pass_ctx=True)
    async def spotify(self, ctx: discord.ext.commands.context.Context):
        pass

    @commands.command(name="oklesgo", pass_ctx=True)
    async def oklesgo(self, ctx: discord.ext.commands.context.Context):
        await self.play(ctx, OK)
        await ctx.send("Ok, Let's goo")

    @commands.command(name="pause", pass_ctx=True)
    async def pause(self, ctx: discord.ext.commands.context.Context):
        try:
            if self.is_playing(ctx):
                await ctx.voice_client.pause()
                await ctx.send("Ok, pausing.")
            else:
                await ctx.send("Not playing anything.")
        except TypeError:
            pass

    @commands.command(name="resume", pass_ctx=True)
    async def resume(self, ctx):
        try:
            if not self.is_playing(ctx):
                await ctx.voice_client.resume()
        except TypeError:
            pass

    @commands.command(name="disconnect", pass_ctx=True)
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(name='t1', pass_ctx=True)
    async def t1(self, ctx: discord.ext.commands.context.Context):
        await self.play(ctx, t1)

    @commands.command(name='t2', pass_ctx=True)
    async def t2(self, ctx: discord.ext.commands.context.Context):
        await self.play(ctx, t2)

    @staticmethod
    def get_shuffled_ops():
        ops_list = [str(i) for i in range(1, 25)]
        random.shuffle(ops_list)
        return ops_list

    def add_ops_to_queue(self, shuffled_list):
        for i in range(len(shuffled_list)):
            self.queue.append(OPS[shuffled_list[i]])

    @commands.command(name="op", pass_ctx=True)
    async def op(self, ctx, num):
        try:
            int(num)
            if int(num) > 24 or int(num) < 1:
                raise ValueError
            playing = await self.play(ctx, OPS[num])
            if playing:
                await ctx.send("Playing %s." % ("op %s" % num))
        except ValueError:
            if num != "all":
                await ctx.send("Bad argument %s!" % num)
            else:
                ops_shuffled = self.get_shuffled_ops()
                self.add_ops_to_queue(ops_shuffled)
                first_in_q = OPS[ops_shuffled.pop(0)]
                print(f"this is the list: {ops_shuffled}\n{first_in_q}\n\n\n")
                await self.play(ctx, first_in_q)

    def get_voice(self, ctx: discord.ext.commands.context.Context):
        return discord.utils.get(self.client.voice_clients, guild=ctx.guild)

    @commands.command(name="join", pass_ctx=True)
    async def join(self, ctx):
        voice_channel = None
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel.")
            return
        else:
            voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command(name="stop", pass_ctx=True)
    async def stop_playing(self, ctx: discord.ext.commands.context.Context):
        voice = self.get_voice(ctx)
        voice.stop()
        self.queue = []

    def is_playing(self, ctx: discord.ext.commands.context.Context):
        voice = self.get_voice(ctx)
        return voice.is_playing()

    async def handle_connected(self, ctx: discord.ext.commands.context.Context):
        if not self.is_connected(ctx):
            await self.join(ctx)

    async def send_playing(self, ctx: discord.ext.commands.context.Context):
        await ctx.send("Added to queue.") if self.is_playing(ctx) else await ctx.send("The song will be played now")

    @staticmethod
    async def invalid_pick(ctx: discord.ext.commands.context.Context):
        await ctx.send("Invalid pick.")

    async def send_yt_search(self, ctx: discord.ext.commands.context.Context):
        search_result = ''
        for i in range(1, 6):
            search_result += '%d: %s\n' % (i, self.yt_search[i]["title"])
        await ctx.send(search_result)


def setup(client):
    client.add_cog(Music(client))
