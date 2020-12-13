import asyncio,logging,re
from discord.ext import commands
from facebook_scraper import get_posts

def scraper(sort,target,N):
    return ([post[sort] for post in get_posts(target, pages=1)][N])
bot=commands.Bot(command_prefix='/')
async def scrape():
    
    #define
    i=j=oldurl_LEA=oldurl_gw=oldurl_qmo=0

    await bot.wait_until_ready()
    while 1:
        #s135=text,s246=url,s7=images
        newurl_LEA=scraper('post_url','LearningEnglishAmericanWay',-1)
        if newurl_LEA!=oldurl_LEA:
            s1=scraper('text','LearningEnglishAmericanWay',-1)
            oldurl_LEA=s2=newurl_LEA
        else:
            s1=s2='0'

        newurl_gw=scraper('post_url','gainwind',-1)
        if newurl_gw!=oldurl_gw:
            s3=scraper('text','gainwind',-1)
            oldurl_gw=s4=newurl_gw
        else:
            s3=s4='0'

        newurl_qmo=scraper('post_url','qmoleenglish',0)
        if newurl_qmo!=oldurl_qmo:
            s5=("".join('\n'.join(scraper('text','qmoleenglish',0)).split('#')[0])).replace('\n\n','$').replace('\n','').replace('$','\n')
            s7='\n'.join(scraper('images','qmoleenglish',0))
            oldurl_qmo=s6=newurl_qmo
        else:
            s5=s6=s7='0'

        i+=1

        if s1!=s2 and s3!=s4:
            s=s1+'\n'+s2+'\n'+"------"+'\n'+s3+'\n'+s4
        elif s1!=s2:
            s=s1+'\n'+s2
        elif s3!=s4:
            s=s3+'\n'+s4
        else:
            s=0
        if s!=0 or s5!='0':
            j+=1
            logging.info(j)
            if s!=0:
                await bot.get_channel(701153967412871268).send(s+'\n')
            if s5!=0:
                await bot.get_channel(701153967412871268).send(s5+'\n'+s6+'\n')
                if s7!=0:
                    await bot.get_channel(701153967412871268).send(s7+'\n')
                    await bot.get_channel(701153967412871268).send(':warning:如果有些圖片沒有顯示，可以點擊貼文的URL'+'\n')
            await bot.get_channel(701153967412871268).send(str(j))
        await asyncio.sleep(300)
logging.basicConfig(level=logging.INFO)
bot.loop.create_task(scrape())
bot.run("NzgyMzA1NTA1ODQyMDM2ODA2.X8KQxw.zLwqJ4OjksO5NcEEIOBYYGbl5_4")
