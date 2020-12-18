import asyncio,logging,traceback,discord,time,datetime,random,math
from discord.ext import commands,tasks
from facebook_scraper import get_posts

#setup
bot=commands.Bot(command_prefix='.')
token='NzgyMzA1NTA1ODQyMDM2ODA2.X8KQxw.dhE5IUJNwwFI-xrGpONoRjUCcj8'
channel1=701153967412871268
intents = discord.Intents(messages=True, guilds=True, members=True)
discord.MemberCacheFlags(online=True)
TIME=sort=0 #exam

def scraper(sort,target,N):
    return ([post[sort] for post in get_posts(target, pages=1,timeout=10)][N])

async def scrape():
    #函式中有用到bot.~時沒有這行會報錯
    await bot.wait_until_ready()

    #define
    i=j=oldurl_LEA=oldurl_gw=oldurl_qmo=0

    while 1:
        try:
            newurl_LEA=scraper('post_url','LearningEnglishAmericanWay',-1)
        
            #s135=text,s246=url,s7=images
            if newurl_LEA!=oldurl_LEA and newurl_LEA!=None:
                s1=scraper('text','LearningEnglishAmericanWay',-1)
                oldurl_LEA=s2=newurl_LEA
            else:
                s1=s2='0'

            newurl_gw=scraper('post_url','gainwind',-1)
            if newurl_gw!=oldurl_gw and newurl_gw!=None:
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
                if s!=0:
                    await bot.get_channel(channel1).send(s+'\n')
                if s5!='0':
                    await bot.get_channel(channel1).send(s5+'\n')
                    if s7!='0':
                        await bot.get_channel(channel1).send(s7+'\n')
                        await bot.get_channel(channel1).send(s6+'\n')
                        await bot.get_channel(channel1).send(':warning:如果有些圖片沒有顯示，可以點擊貼文的URL'+'\n')
                await bot.get_channel(channel1).send(str(j))

        except Exception:
            err=':x:**[ERROR]**```\n'+traceback.format_exc()+'\n```\n'+'To debug, visit https://app.kintohub.com/app/environment/5fd51313ebd88626fb287d51/services/mybot/manage/console'
            await bot.get_channel(channel1).send(err)
            pass
        
        now=datetime.datetime.now()
        if now.hour == 16 and now.minute < 6:
            await bot.get_channel(channel1).send(f'New: {j}\nCheck: {i}')
        await asyncio.sleep(300)

@bot.command()#ok
async def ping(ctx):
    await ctx.send(':ping_pong:  '+str(round(1000*bot.latency)))
@bot.command()#ok
async def gi(ctx):
    #guild = ctx.guild
    embed = discord.Embed(title='The bot is still under development',description="Coded by @flyingcatt3#2016",timestamp=ctx.message.created_at,color=discord.Color.red())
    embed.add_field(name="功能不斷增加中",value='ver 1.2')
    await ctx.send(embed=embed)
@bot.command()
async def exam(ctx,date):
    global TIME,sort
    err=":x:Format error."+"'\n'"+"For help, type `.exam help`"
    if date == 'help':
        await ctx.send('e.g. ``.exam 公測-20221106``')
    elif date == 'reset':
        await ctx.send(':white_check_mark:Reset successfully.')
        TIME=0
    elif date.find('-')!=-1:
        if date.find('-')==date.rfind('-'):
            date=date.split('-')
            if date[-1].isdigit() and len(date[-1])==8 and date[0]!='':
                now = datetime.datetime.now()
                if now.hour >= 16:
                    NOW=int(str(now.year)+str(now.month)+str(now.day+1))
                else:
                    NOW=int(str(now.year)+str(now.month)+str(now.day))
                if int(date[-1]) > NOW:
                    TIME=int(date[-1])
                    sort=date[0]
                    await ctx.send(':white_check_mark:Set up successfully.')
                elif int(date[-1]) == NOW:
                    await ctx.send(':x:The date you specified is today.')
                else:
                    await ctx.send(':x:The date you specified is the past.')
            else:
                await ctx.send(err)
        else:
            await ctx.send(err)
    else:
        await ctx.send(err)
@bot.command()#ok
async def starburst(ctx):
    await ctx.send('https://hbl917070.cf/img/murl/SgsU3cr.jpg')
    if random.randint(1, 10)==1:
        await ctx.send('原來你沒收到封測的邀請嗎？')
#Error Handler
@exam.error
async def examerr(ctx,err):
    global TIME,sort
    if isinstance(err,commands.errors.MissingRequiredArgument):
        if TIME==0:
            await ctx.send(":x:The time of exam is not set up yet."+'\n'+"To set up, type `.exam help`")
        else:
            now = datetime.datetime.now()
            if now.hour >= 16:
                remaining=(datetime.datetime.strptime(str(TIME), "%Y%m%d")-now).days-1
            else:
                remaining=(datetime.datetime.strptime(str(TIME), "%Y%m%d")-now).days
            #remaining=TIME-now
            if remaining==1:
                await ctx.send(f"Time remaining of the **{sort}**: **1 day**")
            elif remaining<=0:
                await ctx.send("Already happened.")
            else:
                await ctx.send(f"Time remaining of the **{sort}**: **{remaining} days**")

@tasks.loop(seconds=60)
async def countdown():
    global TIME,sort
    now=datetime.datetime.now()
    if now.hour == 16 and now.minute <= 1 and TIME!=0:
        #remaining=TIME-now
        remaining=(datetime.datetime.strptime(str(TIME), "%Y%m%d")-now).days-1
        await bot.wait_until_ready()
        await bot.get_channel(614352743791984643).send(f":warning:Time remaining of the **{sort}**: **{remaining} days**")
bot.loop.create_task(scrape())
logging.basicConfig(level=logging.WARNING)
bot.run(token)