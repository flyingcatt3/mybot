# -*- coding:utf-8 -*-
import asyncio,logging,traceback,discord,time,datetime,random,math
from discord.ext import commands,tasks
from facebook_scraper import get_posts

#bot
bot=commands.Bot(command_prefix='.')
botid=782305505842036806
myid=366492389063393281
token='NzgyMzA1NTA1ODQyMDM2ODA2.X8KQxw.dhE5IUJNwwFI-xrGpONoRjUCcj8'
channel1=701153967412871268
intents = discord.Intents(messages=True, guilds=True, members=True)
discord.MemberCacheFlags(online=True)
TIME=sort=0 #exam
stop,stoplist=3,[] #forcestop
scrape_platform,scrape_target,scrape_ch,scrape_creator=[],[],[],[] #@scrape_setup()
delay_choices1 = [5, 10, 15, 20, 25]
delay_choices2 = [300, 330, 360, 390, 420] #延遲的秒數 #@scrape()

#@exam()
err_exam=":x:Format error."+'\n'+"For help, type `.exam help`."

#@scrape_setup()
help_scrape_setup=':information_source: 這是設定爬蟲的指令！'+'P.S. 不包含置頂貼文'+'\n'+'usage: ``.scrape_setup 平臺名稱,目標名稱,頻道ID``'+'\n'+'若``頻道ID``沒有指定，則會以目前你所在的頻道為預設值'+'\n'+'e.g. (1)``.scrape_setup fb,discord``'+'\n'+'e.g. (2)``.scrape_setup fb,discord,頻道ID``'
err_scrape_setup=":x:Format error."+'\n'+"For help, type `.scrape_setup help`."
err_scrape_setup_list=':x:Format error.\nusage:``list [正整數]``'

PASS=':white_check_mark:Set up successfully.'
tineouterr=':x:**操作逾時**'

def scraper(sort,target,N):
    return ([post[sort] for post in get_posts(target, pages=1,timeout=10)][N])

async def scrape():
    #函式中有用到bot.~時沒有這行會報錯
    await bot.wait_until_ready()

    #define
    
    i=j=oldurl_LEA=oldurl_gw=oldurl_qmo=0
    urllist1=['']*100
    urllist2=['']*100

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
                #await bot.get_channel(channel1).send(str(j))
            m=0
            delay1 = random.choice(delay_choices1)  #隨機選取秒數
            while m<len(scrape_platform):
                new_url1=scraper('post_url',scrape_target[m],-1)
                new_url2=scraper('post_url',scrape_target[m],0)
                if new_url1!=urllist1[m] and new_url1!=None:
                    n=-1
                    if urllist2[m]!=new_url2 and urllist1[m]!='':
                        s8=scraper('text',scrape_target[m],n)
                        s9=scraper('images',scrape_target[m],n)
                        n=0
                        if s9 == []:    S=s8+'\n'+new_url1
                        else:   S=s8+'\n'+s9+'\n'+new_url1
                        await bot.get_channel(int(scrape_ch[m])).send(S)
                    urllist1[m]=new_url1
                    urllist2[m]=new_url2
                    s8=scraper('text',scrape_target[m],n)
                    s9='\n'.join(scraper('images',scrape_target[m],n))
                    S=s8+'\n'+s9+'\n'+new_url1
                    await bot.get_channel(int(scrape_ch[m])).send(S)
                    if s9=='':  await bot.get_channel(channel1).send(':warning:如果有些圖片沒有顯示，可以點擊貼文的URL'+'\n')
                await asyncio.sleep(delay1)
                m+=1
        except Exception:
            err=':x:**[ERROR]**```\n'+traceback.format_exc()+'\n```\n'+'To debug, visit https://app.kintohub.com/app/environment/5fd51313ebd88626fb287d51/services/mybot/manage/console'
            await bot.get_channel(channel1).send(err)
            pass
        
        now=datetime.datetime.now()
        if now.hour == 16 and now.minute < 6:
            await bot.get_channel(channel1).send(f'New: {j}\nCheck: {i}')
        delay2 = random.choice(delay_choices2)  #隨機選取秒數
        await asyncio.sleep(delay2-m*delay1)

@bot.command()#ok
async def ping(ctx):
    await ctx.send(':ping_pong:  '+str(round(1000*bot.latency)))

@bot.event#ok
async def on_message(msg):
    global botid
    for x in msg.mentions:
        if int(x.id)==botid and int(msg.author.id)!=botid:
            embed = discord.Embed(title='The bot is still under development',description=f"Coded and owned by <@!{myid}>",timestamp=msg.created_at,color=discord.Color.red())
            embed.add_field(name="功能不斷增加中",value='ver 1.2.1')
            await msg.channel.send(embed=embed)
            break
        #await msg.channel.send(x)
    await bot.process_commands(msg)

@bot.command()#ok
async def exam(ctx,arg):
    global TIME,sort,err_exam
    if arg == 'help':
        await ctx.send('e.g. ``.exam 公測,20221106``')
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



@tasks.loop(seconds=60)
async def countdown():
    global TIME,sort
    now=datetime.datetime.now()
    if now.hour == 16 and now.minute <= 1 and TIME!=0:
        #remaining=TIME-now
        remaining=(datetime.datetime.strptime(str(TIME), "%Y%m%d")-now).days-1
        await bot.wait_until_ready()
        await bot.get_channel(614352743791984643).send(f":warning:Time remaining of **{sort}**: **{remaining} days**")

@bot.command()#ok
async def forcestop(ctx):
    global stop,stoplist
    if int(ctx.author.id) == myid:
        await ctx.send("Stopped.")
        await bot.logout()
    elif stop > 1 and not ctx.author in stoplist:
        await bot.wait_until_ready()
        stop-=1
        tmp=stop
        stoplist.append(ctx.author)
        await ctx.send(f"還需要其他 **{stop}** 人執行此指令始可強制停止{bot.get_user(782305505842036806).mention}")
        await asyncio.sleep(30)
        if tmp==stop:
            await ctx.send(tineouterr)
            stop=3
            stoplist=[]
    elif ctx.author in stoplist: await ctx.send(f'{ctx.author}, 此為無效操作')
    else:
        await ctx.send("Stopped.")
        await bot.logout()

@bot.command()
async def scrape_setup(ctx,arg):
    global scrape_platform,scrape_target,scrape_ch,err_scrape_setup,err_scrape_setup_list,help_scrape_setup
    if arg == 'help':
        await ctx.send(help_scrape_setup)
    elif arg.startswith('list'):
        if arg[-1].isdigit():
            if int(arg[-1])-1 > len(scrape_platform):
                arg[-1]=len(scrape_platform)+1
            if int(arg[-1]) > 0 and scrape_platform != []:
                N=int(arg[-1])-1
                a='[平臺]         '+scrape_platform[N]+'\n'
                b='[目標]         '+scrape_target[N]+'\n'
                c='[頻道ID]     '+scrape_ch[N]+'\n'
                d='[創建者]     '+scrape_creator[N]
                await ctx.send(':information_source: **爬蟲組態列表**'+'\n'+a+b+c+d+'\n:information_source:若要刪除此組態，請輸入:x:')
                i=0
                async def check(m):
                    if int(ctx.author.id) == myid: return 1
                    i+=1
                    if i==1:    await ctx.send('還需要 1 人回覆:x:')
                    return i==2 and m.content == ':x:' and m.channel == ctx.channel
                try:
                    await bot.wait_for('message', timeout=60.0, check=check)
                    scrape_platform.remove(scrape_platform[N])
                    scrape_target.remove(scrape_target[N])
                    scrape_ch.remove(scrape_ch[N])
                    scrape_creator.remove(scrape_creator[N])
                    await ctx.send(':white_check_mark:Remove successfully.')
                except asyncio.TimeoutError:
                    if i!=0:    await ctx.send(tineouterr)
            elif scrape_platform == []: await ctx.send(':warning:目前沒有任何組態')
            else: await ctx.send(err_scrape_setup_list)
        else: await ctx.send(err_scrape_setup_list)
    elif len(scrape_platform)>100:  await ctx.send(':x:')
    elif arg.find(',')!=-1:
        comma2_isnotexist= arg.find(',') == arg.rfind(',')
        arg=arg.split(',')
        if arg[0].lower() in ['fb','facebook']:
            if arg[1] == '':
                await ctx.send(err_scrape_setup)
            else:
                if not arg[1] in scrape_target:
                    try:
                        tmp=-1
                        if comma2_isnotexist or arg[-1] == '':
                            if int(ctx.channel.id) != channel1:
                                await ctx.send(':mag:Checking...')
                                scraper('time',arg[1],0)
                                if int(ctx.author.id) != myid:
                                    await ctx.send(f'目標為  https://www.facebook.com/{arg[1]}/\n:warning:需要其他 2 人回覆:thumbsup:始可設定成功')
                                    async def check(m):
                                        i=0
                                        i+=1
                                        if i==1:    await ctx.send('還需要 1 人回覆:thumbsup:')
                                        return i==2 and m.content == ':thumbsup:' and m.channel == ctx.channel
                                    try:    await bot.wait_for('message', timeout=60.0, check=check)
                                    except asyncio.TimeoutError:    await ctx.send(tineouterr)
                                scrape_platform.append('Facebook')
                                scrape_target.append(arg[1])
                                scrape_ch.append(str(ctx.channel.id))
                                scrape_creator.append(str(ctx.author))
                                await ctx.send(PASS+'\n'+f':information_source:將於稍後於{ctx.channel.mention}傳送 https://www.facebook.com/{arg[1]}/ 上的貼文，並每 **6~10 分鐘** 檢查更新')
                                tmp=0
                            else:
                                await ctx.send(':x:此頻道不能被指定，因為其在例外中')
                        elif int(arg[-1]) != channel1:
                            for x in ctx.guild.channels:
                                tmp=str(x.id).find(arg[-1])
                                if tmp==-1:
                                    await ctx.send(':mag:Checking...')
                                    scraper('time',arg[1],0)
                                    if int(ctx.author.id) != myid:
                                        await ctx.send(f'目標為  https://www.facebook.com/{arg[1]}/\n:warning:需要其他 2 人回覆:thumbsup:始可設定成功')
                                        async def check(m):
                                            i=0
                                            i+=1
                                            if i==1:    await ctx.send('還需要 1 人回覆:thumbsup:')
                                            return i==2 and m.content == ':thumbsup:' and m.channel == ctx.channel
                                        try:    await bot.wait_for('message', timeout=60.0, check=check)
                                        except asyncio.TimeoutError:    await ctx.send(tineouterr)
                                    scrape_platform.append('Facebook')
                                    scrape_target.append(arg[1])
                                    scrape_ch.append(arg[-1])
                                    scrape_creator.append(str(ctx.author))
                                    tmp=0
                                    await ctx.send(PASS+'\n'+f':information_source:將於稍後於{x.mention}傳送 https://www.facebook.com/{arg[1]}/ 上的貼文，並每 **6~10 分鐘**檢查更新')
                                    break
                        if str(arg[-1]) == str(channel1):    await ctx.send(':x:此頻道不能被指定，因為其在例外中')
                        elif tmp==-1:   await ctx.send(':x:被指定的頻道不存在，或是機器人沒有查看該頻道的權限')
                    except Exception:
                        #await ctx.send(traceback.format_exc())
                        await ctx.send(':x:目標名稱不存在於 Facebook 上')
                        pass
                else:
                    await ctx.send(':x:被指定的目標不能重複設定')
        elif arg[0].lower() in ['twitter','ig','instagram']:
            await ctx.send(':x:被指定的平臺尚未支援，目前只支援 Facebook')
        elif arg[0] == '':  await ctx.send(err_scrape_setup)
        else:   await ctx.send(':x:被指定的平臺不存在')
    else: await ctx.send(err_scrape_setup)

@bot.command()#ok
async def hulan(ctx,arg):
    await ctx.send(f'**{arg}**一進dc，所有聊天的人便開始對著他嘲諷，有的叫道，\n「**{arg}**，你的噁男身份組又添上新的了！」\n他不回答，對其他人說，「我不是甲。」便排出我不是噁男幾個字。\n他們又故意的高聲嚷道，「吼 你又好想狠狠的跳起來了！」\n**{arg}**睜大眼睛說，「你怎麼這樣憑空污人清白……」「什麼清白?我前天親眼見你噁人，還裝。」**{arg}**便漲紅了臉，額上的青筋條條綻出，爭辯道，「搭訕的事不能算……人際交流！……欣賞人的事，能算噁麼？」\n接連便是難懂的話，什麼「要是我是妹子」，什麼「我也很喜歡蘿莉」之類，引得眾人都鬨笑起來：群組內充滿了快活的空氣。')

@bot.command()#這是最短，最單純，最美麗的function
async def getchannelid(ctx):
    await ctx.send(ctx.channel.id)

#Error Handler
@exam.error#ok
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
            elif remaining<=0: await ctx.send("Already happened.")
            else:
                await ctx.send(f"Time remaining of the **{sort}**: **{remaining} days**")

@hulan.error#ok
async def hulanerr(ctx,err):
    if isinstance(err,commands.errors.MissingRequiredArgument):
        await bot.wait_until_ready()
        await ctx.send(':x:既然你不指定參數，那我要...')
        await asyncio.sleep(2)
        await hulan(ctx,bot.get_user(ctx.author.id).mention)

@scrape_setup.error#ok
async def scrape_setuperr(ctx,err):
    if isinstance(err,commands.errors.MissingRequiredArgument):
        await ctx.send(help_scrape_setup)

bot.loop.create_task(scrape())
logging.basicConfig(level=logging.INFO)
bot.run(token)