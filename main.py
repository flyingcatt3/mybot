import discord, asyncio
from discord.ext import commands,tasks
from facebook_scraper import get_posts

def scraper(sort,target):
    return ([post[sort] for post in get_posts(target, pages=1)][-1])
bot=commands.Bot(command_prefix='/')
async def scrape():
    await bot.wait_until_ready()
    channel=bot.get_channel(701153967412871268)
    oldurl_LEA=oldurl_gw=0
    while True:
        #s13=text,s24=url
        newurl_LEA=scraper('post_url','LearningEnglishAmericanWay')
        if newurl_LEA!=oldurl_LEA:
            s1=scraper('text','LearningEnglishAmericanWay')
            oldurl_LEA=s2=newurl_LEA
        else:
            s1=s2=0

        newurl_gw=scraper('post_url','gainwind')
        if newurl_gw!=oldurl_gw:
            s3=scraper('text','gainwind')
            oldurl_gw=s4=newurl_gw
        else:
            s3=s4=0
        
        if s1!=s2 or s3!=s4:
            s=s1+'\n'+s2+'\n'+"------"+'\n'+s3+'\n'+s4
            await channel.send(s)
            await channel.send('debug')
        elif s1!=s2:
            s=s1+'\n'+s2
            await channel.send(s)
            await channel.send('debug')
        elif s3!=s4:
            s=s3+'\n'+s4
            await channel.send(s)
            await channel.send('debug')
        asyncio.sleep(300)
bot.loop.create_task(scrape())       
bot.run("NzgyMzA1NTA1ODQyMDM2ODA2.X8KQxw.zLwqJ4OjksO5NcEEIOBYYGbl5_4")

