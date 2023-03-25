import re

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
# /watch?v=G75KfgmTXSs
YT_URL_FORMAT = r"watch\?v=(\S{11})"
YT_TITLE_RANGE = r"{}(.*)/watch\?v={}"
YT_TITLE_TEXT_RANGE = r'"text":"(.*)"}],"accessibility"'
YT_SEARCH = "https://www.youtube.com/results?search_query={}"
YT_URL = "https://www.youtube.com/watch?v={}"
