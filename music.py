import discord
from discord.ext import commands
import youtube_dl
import time

FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
YDL_OPTIONS = {'format': 'bestaudio'}

OK = "https://www.youtube.com/watch?v=GD9QURJd6qA&ab_channel=SvenBalthazard"

t1 = u'https://www.youtube.com/watch?v=rfT6IhY_eUM&ab_channel=SLOplayz'
t2 = u'https://www.youtube.com/watch?v=MU_ZhdCy9-8&ab_channel=AnimeKURO'

OPS = {
    "1": u"https://www.youtube.com/watch?v=HRaoYuRKBaA",
    "2": u"https://www.youtube.com/watch?v=54dp8ucsGG8",
    "3": u"https://www.youtube.com/watch?v=x1_sHTEEmik",
    "4": u"https://www.youtube.com/watch?v=AYhIPAs8JTU",
    "5": u"https://www.youtube.com/watch?v=RO_VGv4GT9k",
    "6": u"https://www.youtube.com/watch?v=Tyr7Ymbtl2Y",
    "7": u"https://www.youtube.com/watch?v=U-1rNzn1w6o",
    "8": u"https://www.youtube.com/watch?v=rXINBAWxJ94",
    "9": u"https://www.youtube.com/watch?v=o7sZWSVH37g",
    "10": u"https://www.youtube.com/watch?v=CFM_zypYFHM",
    "11": u"https://www.youtube.com/watch?v=LzC0HSOOauI",
    "12": u"https://www.youtube.com/watch?v=eS0hCgXMnT4",
    "13": u"https://www.youtube.com/watch?v=hJgJTTIbMDI",
    "14": u"https://www.youtube.com/watch?v=z7QgUzPHkBA",
    "15": u"https://www.youtube.com/watch?v=fCQufN8Wsgc",
    "16": u"https://www.youtube.com/watch?v=cZsj0dTTmy8",
    "17": u"https://www.youtube.com/watch?v=1apeGd4cinU",
    "18": u"https://www.youtube.com/watch?v=jJHDDYd6PrM",
    "19": u"https://www.youtube.com/watch?v=fsWF5Ek_RiI",
    "20": u"https://www.youtube.com/watch?v=yJXUuu2lF7s",
    "21": u"https://www.youtube.com/watch?v=t7xHamn5inQ",
    "22": u"https://www.youtube.com/watch?v=PwVT67T5Xt4",
    "23": u"https://www.youtube.com/watch?v=hBi9wavp2w4",
    "24": u"https://www.youtube.com/watch?v=MSXr7O0hu-c"

}


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
        await voice.stop()

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
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        return source

    async def get_first_in_q(self, ctx: discord.ext.commands.context.Context):
        if self.check_q():
            source = await self.get_audio(self.queue.pop(0))
            ctx.voice_client.play(source)

    async def play_q(self, ctx: discord.ext.commands.context.Context):
        while len(self.queue) > 0:
            if self.is_playing(ctx):
                time.sleep(1)
            else:
                time.sleep(3)
                print("playing the queue")
                self.stop_playing(ctx)
                ctx.voice_client.play(await self.get_first_in_q(ctx))

    @commands.command(name="play", pass_ctx=True)
    async def play(self, ctx: discord.ext.commands.context.Context, url=""):
        await self.handle_connected(ctx)
        if self.is_playing(ctx):
            await self.handle_queue(ctx, url)
            await self.play_q(ctx)
            return False
        else:
            vc = ctx.voice_client
            source = await self.get_audio(url)
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
