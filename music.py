import discord
from discord.ext import commands
import youtube_dl
import time
from Variables import *


class Music(commands.Cog):

    # todo: Add queue function, skipping function

    def __init__(self, client: commands.Bot):
        self.client = client
        self.queue = []

    def check_q(self):
        return len(self.queue) > 0

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

    @staticmethod
    def is_connected(ctx: discord.ext.commands.context.Context):
        connected = ctx.voice_client and ctx.voice_client.is_connected()
        print(f"Connected to voice channel: {ctx.voice_client and ctx.voice_client.is_connected()}")
        return True if connected else False

    @commands.command(name="disconnect", pass_ctx=True)
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(name='t1', pass_ctx=True)
    async def t1(self, ctx: discord.ext.commands.context.Context):
        await self.play(ctx, t1)

    @commands.command(name='t2', pass_ctx=True)
    async def t2(self, ctx: discord.ext.commands.context.Context):
        await self.play(ctx, t2)

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
                # todo: play all openings shuffled
                pass

    def get_voice(self, ctx: discord.ext.commands.context.Context):
        return discord.utils.get(self.client.voice_clients, guild=ctx.guild)

    @commands.command(name="stop", pass_ctx=True)
    async def stop_playing(self, ctx: discord.ext.commands.context.Context):
        voice = self.get_voice(ctx)
        voice.stop()

    def is_playing(self, ctx: discord.ext.commands.context.Context):
        voice = self.get_voice(ctx)
        return voice.is_playing()

    def add_to_queue(self, url):
        self.queue.append(url)

    async def handle_connected(self, ctx: discord.ext.commands.context.Context):
        if not self.is_connected(ctx):
            await ctx.send("Joining channel.")
            await self.join(ctx)

    async def handle_queue(self, ctx: discord.ext.commands.context.Context, url):
        await ctx.send("Added song to the queue.")
        self.add_to_queue(url)

    @staticmethod
    async def get_audio(url):
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            print(url2)
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        return source

    async def get_first_in_q(self, ctx: discord.ext.commands.context.Context):
        if self.check_q():
            source = await self.get_audio(self.queue.pop(0))
            return source

    async def play_q(self, ctx: discord.ext.commands.context.Context):
        while len(self.queue) > 0:
            if self.is_playing(ctx):
                time.sleep(1)
            else:
                await self.stop_playing(ctx)
                time.sleep(3)
                ctx.voice_client.play(await self.get_first_in_q(ctx))

    @commands.command(name="play", pass_ctx=True)
    async def play(self, ctx: discord.ext.commands.context.Context, url="", queue=False):
        """
        every song I command playing enters a queue and the command actually plays the next song in queue,
        no matter if the queue is empty or not.
        in the end I will add the next condition

        `if len(self.queue) > 0:
            await self.play(ctx, self.queue.pop(0), queued=True)`

        which will recurse the function until the queue is empty.
        now all I need is to make the bot wait for the current song to finish playing and while it waits it needs to
        be able to receive commands too.
        """
        await self.handle_connected(ctx)
        if self.is_playing(ctx):
            await self.handle_queue(ctx, url)
            await self.play_q(ctx)
            return False
        else:
            vc = ctx.voice_client
            source = await self.get_audio(url)
            if self.is_playing(ctx):
                time.sleep(1)
                await self.play(ctx, url)
            else:
                vc.play(source)
            return True

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
                await ctx.send("Ok, resuming.")
            else:
                await ctx.send("Nothing is paused.")
        except TypeError:
            pass


def setup(client):
    client.add_cog(Music(client))
