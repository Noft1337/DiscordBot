import discord
from discord.ext import commands
import youtube_dl

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

    def __init__(self, client):
        self.client = client
        self.queue = []

    @commands.command(name="join", pass_ctx=True)
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel.")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @staticmethod
    def is_connected(ctx):
        return ctx.voice_client is not None

    @commands.command(name="disconnect", pass_ctx=True)
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command(name="op", pass_ctx=True)
    async def op(self, ctx, num):
        try:
            int(num)
            await ctx.send("Playing %s." % ("op %s" % num))
            await self.play(ctx, OPS[num])
        except ValueError:
            if num != "all":
                await ctx.send("Bad argument %s!" % num)
            else:
                pass

    @commands.command(name="play", pass_ctx=True)
    async def play(self, ctx, url=""):
        if not self.is_connected(ctx):
            await ctx.send("Joining channel.")
            await self.join(ctx)
        else:
            ctx.voice_client.stop()
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        ydl_options = {'format': 'bestaudio'}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **ffmpeg_options)
            vc.play(source)

    @commands.command(name="pause", pass_ctx=True)
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("Ok, pausing.")

    @commands.command(name="resume", pass_ctx=True)
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send("Ok, resuming.")


def setup(client):
    client.add_cog(Music(client))
