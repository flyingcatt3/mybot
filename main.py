import asyncio,logging,traceback,discord,time,random,math
from discord.ext import commands
from facebook_scraper import get_posts

def scraper(sort,target,N):
    return ([post[sort] for post in get_posts(target, pages=1,timeout=10)][N])
#define
bot=commands.Bot(command_prefix='π')
token='NzgyMzA1NTA1ODQyMDM2ODA2.X8KQxw.dhE5IUJNwwFI-xrGpONoRjUCcj8'
channel1=701153967412871268
intents = discord.Intents(messages=True, guilds=True, members=True)
discord.MemberCacheFlags(online=True)
async def scrape():
    await bot.wait_until_ready()

    #define
    
    i=j=oldurl_LEA=oldurl_gw=oldurl_qmo=0
    err=':x:**[ERROR]**\n'+traceback.format_exc()+'\n'+'To debug, visit https://app.kintohub.com/app/environment/5fd51313ebd88626fb287d51/services/mybot/manage/console'

    while 1:
        try:
            newurl_LEA=scraper('post_url','LearningEnglishAmericanWay',-1)
    
            #s135=text,s246=url,s7=images
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
                    await bot.get_channel(channel1).send(s+'\n')
                if s5!='0':
                    await bot.get_channel(channel1).send(s5+'\n')
                    if s7!='0':
                        await bot.get_channel(channel1).send(s7+'\n')
                        await bot.get_channel(channel1).send(s6+'\n')
                        await bot.get_channel(channel1).send(':warning:如果有些圖片沒有顯示，可以點擊貼文的URL'+'\n')
                await bot.get_channel(channel1).send(str(j))       
        except:
            await bot.get_channel(channel1).send(err)
        await asyncio.sleep(300)
        
@bot.command()
async def ping(ctx):
    await ctx.send(':pingpong:  '+str(100*bot.latency))
@bot.command()
async def gi(ctx):
    guild = ctx.guild
    embed = discord.Embed(title='The bot is still under development',description="Coded by @flyingcatt3#2016",timestamp=ctx.message.created_at,color=discord.Color.red())
    embed.add_field(name="Server Owner:",value=guild.owner)
    embed.add_field(name="功能不斷增加中",value=guild.name)
    await ctx.send(embed=embed)
@bot.command()
async def gsat(ctx,sort,date):
    gsattime=0
    def now():
        return int(str(time.localtime().tm_year)+str(time.localtime().tm_mon)+str(time.localtime().tm_date))
    if sort == 'set':
        if date.isdigit() and len(date)==8:
            if date >= now():
                await ctx.send(':white_check_mark:Set up Succeedfully.')
                gsattime=date
            elif date == now():
                await ctx.send(':x:The date you specified is today.')
        elif date == 'help':
            await ctx.send('e.g. πgsat set 20221106')
        
        else:
            await ctx.send(":x:Format error."+"'\n'"+"For help, type `πgsat set help`")
    elif sort == None:
        if gsattime==0:
            await ctx.send(":x:The time of gsat is not set up yet."+"'\n'"+"To set up, type `πgsat set TIME`")
        else:
            remaining=gsattime-date
            if remaining==1:
                await ctx.send("Time remaining: **1 day**")
            elif remaining<=0:
                await ctx.send("Already happened.")
            else:
                await ctx.send(f"Time remaining: **{remaining} days**")
@bot.command()
async def starburst(ctx):
    await ctx.send('https://hbl917070.cf/img/murl/SgsU3cr.jpg')
    if random.randint(1, 10):
        await ctx.send('原來你沒收到封測的邀請嗎？')
@bot.command()
async def ot(ctx):
    end=time.time()
    await ctx.send(':hourglass:Operated for '+str(round((end-start)/3600),1)+' h:hourglass_flowing_sand:')
#Error Handler
@gsat.error()
async def error(ctx,error):
    if isinstance(error,commands.errors.MissingRequiredArgument):
        await ctx.send(":x:Please provide the time of GSAT.")
start = time.time()
bot.loop.create_task(scrape())
logging.basicConfig(level=logging.INFO)
bot.run(token)
