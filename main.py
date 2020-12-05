import discord, asyncio
from discord.ext import commands,tasks
from facebook_scraper import get_posts

def scraper(sort,target):
    return ([post[sort] for post in get_posts(target, pages=1)][-1])
bot=commands.Bot(command_prefix='/')
@tasks.loop()
async def send():
    await bot.wait_until_ready()
    channel=bot.get_channel(701153967412871268)
    oldtime_LEA=oldtime_gw=0
    while True:
        newtime_LEA=scraper('time','LearningEnglishAmericanWay')
        if newtime_LEA!=oldtime_LEA:
            s1=scraper('text','LearningEnglishAmericanWay')
            s2=scraper('post_url','LearningEnglishAmericanWay')
            oldtime_LEA=newtime_LEA
        else:
            s1=s2=0

        newtime_gw=scraper('time','gainwind')
        if newtime_gw!=oldtime_gw:
            s3=scraper('text','gainwind')
            s4=scraper('post_url','gainwind')
            oldtime_gw=newtime_gw
        else:
            s3=s4=0
        
        if s1!=s2 or s3!=s4:
            s=s1+'\n'+s2+'\n'+"------"+'\n'+s3+'\n'+s4
            await channel.send(s)
        elif s1!=s2:
            s=s1+'\n'+s2
            await channel.send(s)
        elif s3!=s4:
            s=s3+'\n'+s4
            await channel.send(s)
        await asyncio.sleep(1200)
bot.run("NzgyMzA1NTA1ODQyMDM2ODA2.X8KQxw.zLwqJ4OjksO5NcEEIOBYYGbl5_4")
send.start()
