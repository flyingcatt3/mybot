# -*- coding:utf-8 -*-
import asyncio,logging,discord,datetime,random,os,keep_alive,itertools
from discord.ext import commands,tasks

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

get_or_create_eventloop()

#bot
bot=commands.Bot(command_prefix='.')
botid=782305505842036806
myid=366492389063393281
channel1=701153967412871268
channel2=617284939053793298
intents = discord.Intents(messages=True, guilds=True, members=True)
discord.MemberCacheFlags(online=True)
TIME=sort=0 #exam
PASS=':white_check_mark:Set up successfully.\n'

#@exam()
err_exam=":x:Format error."+'\n'+"For help, type `.exam help`."

@bot.event#ok
async def on_message(msg):
    global botid
    for x in msg.mentions:
        if int(x.id)==botid and int(msg.author.id)!=botid:
            embed = discord.Embed(title='The bot is still under development',description=f"Coded and owned by <@!{myid}>",timestamp=msg.created_at,color=discord.Color.red())
            embed.add_field(name="功能不斷增加中",value='Ver. 20211112')
            await msg.channel.send(embed=embed)
            break
        #await msg.channel.send(x)
    await bot.process_commands(msg)

@bot.command()#ok
async def exam(ctx,arg):
    global TIME,sort,err_exam
    if arg == 'help':
        await ctx.send('e.g. `.exam 公測,20221106`')
    elif arg == 'reset':
        await ctx.send(':white_check_mark:Reset successfully.')
        TIME=0
    elif arg.find(',')!=-1:
        if arg.find(',')==arg.rfind(','):
            arg=arg.split(',')
            if arg[-1].isdigit() and len(arg[-1])==8 and arg[0]!='':
                now = datetime.datetime.now()
                if now.hour >= 16:
                    NOW=int(str(now.year)+str(now.month)+str(now.day+1))
                else:
                    NOW=int(str(now.year)+str(now.month)+str(now.day))
                if int(arg[-1]) > NOW:
                    TIME=int(arg[-1])
                    sort=arg[0]
                    await ctx.send(PASS)
                elif int(arg[-1]) == NOW:
                    await ctx.send(':x:The date you specified is today.')
                else:
                    await ctx.send(':x:The date you specified is the past.')
            else:
                await ctx.send(err_exam)
        else:
            await ctx.send(err_exam)
    else:
        await ctx.send(err_exam)

@bot.command()#ok
async def starburst(ctx):
    await ctx.send('https://hbl917070.cf/img/murl/SgsU3cr.jpg')
    if random.randint(1, 10)==1:
        await ctx.send('原來你沒收到封測的邀請嗎？')

@bot.command()#ok
async def hulan(ctx,arg):
    await ctx.send(f'**{arg}**一進dc，所有聊天的人便開始對著他嘲諷，有的叫道，\n「**{arg}**，你的噁男身份組又添上新的了！」\n他不回答，對其他人說，「我不是甲。」便排出我不是噁男幾個字。\n他們又故意的高聲嚷道，「吼 你又好想狠狠的跳起來了！」\n**{arg}**睜大眼睛說，「你怎麼這樣憑空污人清白……」「什麼清白?我前天親眼見你噁人，還裝。」**{arg}**便漲紅了臉，額上的青筋條條綻出，爭辯道，「搭訕的事不能算……人際交流！……欣賞人的事，能算噁麼？」\n接連便是難懂的話，什麼「要是我是妹子」，什麼「我也很喜歡蘿莉」之類，引得眾人都鬨笑起來：群組內充滿了快活的空氣。')

@bot.command()
async def agt(ctx,arg):
    p=random.randint(0,120)
    a=f"{arg} 有 **{p}%** 的可能去考分科測驗"
    b=f"騙人的吧<:1_pepo:778999019682791474>...{arg} 只有 **{p}%** 的可能去考分科測驗"
    
    link=['https://pse.is/3se6k2','https://i.imgur.com/qdIqIID.png','https://pse.is/3srfgz']
    
    if p>100:
        await ctx.send('https://i.imgur.com/UUDVTBS.png')
    elif p>=50:
        await ctx.send(a)
        await ctx.send(random.choice(link))
    elif p<=20:
        await ctx.send(b)
    else:
        await ctx.send(a)

@bot.command()#這是最短，最單純，最美麗的function
async def getchannelid(ctx):
    await ctx.send(ctx.channel.id)

@bot.command()
async def now(ctx):
    await ctx.send(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %p"))

status = itertools.cycle(['with Python','lazzicat'])

@bot.event
async def on_ready():
  change_status.start()
  print("Your bot is ready")

@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Game(next(status)))

#Error Handler
@exam.error#ok
async def examerr(ctx,err):
    global TIME,sort
    if isinstance(err,commands.errors.MissingRequiredArgument):
        if TIME==0:
            await ctx.send(":x:There's no timer."+'\n'+"To set up, type `.exam help`")
        else:
            now = datetime.datetime.now()
            if now.hour >= 16:
                remaining=(datetime.datetime.strptime(str(TIME), "%Y%m%d")-now).days-1
            else:
                remaining=(datetime.datetime.strptime(str(TIME), "%Y%m%d")-now).days
            #remaining=TIME-now
            if remaining==1:
                await ctx.send(f"Time remaining of **{sort}**: **1 day**")
            elif remaining<=0: await ctx.send("Already happened.")
            else:
                await ctx.send(f"Time remaining of **{sort}**: **{remaining} days**")

@hulan.error#ok
async def hulanerr(ctx,err):
    if isinstance(err,commands.errors.MissingRequiredArgument):
        await bot.wait_until_ready()
        await ctx.send(':x:既然你不指定參數，那我要...')
        await asyncio.sleep(2)
        await hulan(ctx,bot.get_user(ctx.author.id).mention)

@agt.error#ok
async def agterr(ctx,err):
    if isinstance(err,commands.errors.MissingRequiredArgument):
        await bot.wait_until_ready()
        await agt(ctx,ctx.author.mention)

logging.basicConfig(level=logging.INFO)
keep_alive.keep_alive()
bot.run(os.environ['token'])