# -*- coding:utf-8 -*-
import asyncio,logging,traceback,discord,time,datetime,random,math,pygsheets
from discord.ext import commands,tasks
from facebook_scraper import get_posts

#bot
bot=commands.Bot(command_prefix='.')
botid=782305505842036806
myid=366492389063393281
token='NzgyMzA1NTA1ODQyMDM2ODA2.X8KQxw.dhE5IUJNwwFI-xrGpONoRjUCcj8'
channel1=701153967412871268
channel2=617284939053793298
intents = discord.Intents(messages=True, guilds=True, members=True)
discord.MemberCacheFlags(online=True)
TIME=sort=0 #exam
stop,stoplist=3,[] #restart
scrape_platform,scrape_target,scrape_ch,scrape_creator=[],[],[],[] #@scrape_setup()
delay_choices1 = [5, 10, 15, 20, 25]
delay_choices2 = [300, 330, 360, 390, 420] #延遲的秒數 #@scrape()

#@exam()
err_exam=":x:Format error."+'\n'+"For help, type `.exam help`."

#@scrape_setup()
help_scrape_setup=':information_source: 這是設定爬蟲的指令！'+'P.S. 不包含置頂貼文'+'\n'+'usage: ``.scrape_setup 平臺名稱,目標名稱,頻道ID``'+'\n'+'若``頻道ID``沒有指定，則會以目前你所在的頻道為預設值'+'\n'+'e.g. (1)``.scrape_setup fb,discord``'+'\n'+'e.g. (2)``.scrape_setup fb,discord,頻道ID``'
err_scrape_setup=":x:Format error."+'\n'+"For help, type `.scrape_setup help`."
err_scrape_setup_remove=':x:Format error.\nusage:``remove[設定編號]``'
err_scrape_setup_note=':x:Format error.\nusage:``note[設定編號]``'

urllist=toplist=[]
urldate=firstdate=0

PASS=':white_check_mark:Set up successfully.'
timeouterr=':x:**操作逾時**'

gc = pygsheets.authorize(service_account_file='./credentials.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/14YsP3o_P_U3bNie-I5-CYIr1Ym26WMb404H3TprepbQ')

async def gsheet1(ctx,method):
    global sh,scrape_platform,scrape_target,scrape_ch,scrape_creator
    ws = sh.worksheet_by_title('爬蟲組態')
    async def check(m):
        if m.content=='是':
            ws.update_value(f'C{n}','=TODAY()')
            scrape_platform.remove(scrape_platform[n-2])
            scrape_target.remove(scrape_target[n-2])
            scrape_ch.remove(scrape_ch[n-2])
            scrape_creator.remove(scrape_creator[n-2])
            await ctx.send(':white_check_mark:Removed.')
            return 1
        elif method=='n':
            ws.update_value(f'H{n}',m.content)
            await ctx.send(':white_check_mark:The note is added.')
            return 1
    if method=='fetch':
        N=int(ws.get_value('I1'))
        D=ws.get_values(start=(2,4), end=(N,4))
        E=ws.get_values(start=(2,5), end=(N,5))
        F=ws.get_values(start=(2,6), end=(N,6))
        G=ws.get_values(start=(2,7), end=(N,7))
        i=0
        while i<100:
            if i==len(D) or D[i]==['']:
                break
            else:
                scrape_platform.append(' '.join(D[i]))
                scrape_target.append(' '.join(E[i]))
                scrape_ch.append(' '.join(F[i]))
                scrape_creator.append(' '.join(G[i]))
            i+=1
    elif method=='create':
        N=ws.get_value('I1')
        ws.update_values(crange=f'D{N}:G{N}',values=[[scrape_platform[-1],scrape_target[-1],scrape_ch[-1],scrape_creator[-1]]])
    else:
        n=int(method.strip()[1])+1
        if ws.get_value(f'A{n}')=='':
            await ctx.send(':x:Error 404')
        elif ws.get_value(f'G{n}')!=str(ctx.author):
            await ctx.send(':x:只有創建者才能進行操作')    
        elif method.strip()[0] == 'n':
            await ctx.send('請輸入備註:')
            try:
                await bot.wait_for('message', timeout=60.0, check=check)

            except asyncio.TimeoutError:
                await ctx.send(timeouterr)
        else:
            await ctx.send(f":warning:確定要刪除編號 **{n}** 的設定嗎？\n若要刪除，請在 30 秒內輸入 '是'")
            try:
                await bot.wait_for('message', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(timeouterr)

def gsheet2(urllist_or_toplist,row):
    global sh,urllist,toplist
    ws = sh.worksheet_by_title('URL')
    if urllist_or_toplist=='fetch':
        url=ws.get_values(start=(1,1), end=(103,1))
        top=ws.get_values(start=(1,2), end=(103,2))
        i=j=0
        while i<103:
            if i==len(url) or url[i]==['']:
                break
            else:
                urllist.append(' '.join(url[i]))
                urllist.append(' '.join(top[i]))
            i+=1
        while j<103:
            if j==len(top) or top[i]==['']:
                break
            else:
                urllist.append(' '.join(top[j]))
            j+=1
    else:
        if urllist_or_toplist.isdigit():
            ws.update_value(f'B{row}',urllist_or_toplist)
        else:
            ws.update_value(f'A{row}',urllist_or_toplist)

def gsheet3(a,b):
    global sh,urldate,firstdate
    ws = sh.worksheet_by_title('Cycle')
    i=2
    while 1:
        tmp=ws.get_value(f'A{i}')
        if tmp=='':
            firstdate=1
            break
        elif tmp!=urldate:
            urldate=tmp
            if firstdate==0:
                ws.update_value(f'A{i}','=TODAY()-1')
                i+=1
            else:
                firstdate=0
                break

    if ws.get_value(f'B{i}')=='':
        ws.update_value(f'B{i}',a)
    else:
        ws.update_value(f'B{i}',int(ws.get_value(f'B{i}'))+a)
    if ws.get_value(f'C{i}')=='':
        ws.update_value(f'C{i}',b)
    else:
        ws.update_value(f'C{i}',int(ws.get_value(f'C{i}'))+b)
    
def scraper(sort,target,N):
    return ([post[sort] for post in get_posts(target, pages=1,timeout=10)][N])

async def scrape():
    #函式中有用到bot.~時沒有這行會報錯
    await bot.wait_until_ready()

    #define
    
    global urllist,scrape_target,scrape_ch
    toplist=[]
    warn=':warning:如果有些圖片沒有顯示，可以點擊貼文的URL'

    while 1:
        m=x=0
        if urllist==[]:
            await gsheet1(0,'fetch')
            gsheet2('fetch',0)
        asyncio.sleep(5)
        if m==len(urllist):
            i=0
            while i<3:
                urllist.append(0)
                i+=1

        try:#s135=text,s246=url,s7=images
            newurl_LEA=scraper('post_url','LearningEnglishAmericanWay',-1)
            if newurl_LEA!=urllist[m] and newurl_LEA!=None:
                urllist[m]=newurl_LEA
                gsheet2(newurl_LEA,1)
                s1=scraper('text','LearningEnglishAmericanWay',-1)
                s2=newurl_LEA
                x+=1
            else:
                s1=s2='0'
            await asyncio.sleep(random.choice(delay_choices1))
            m+=1
            newurl_gw=scraper('post_url','gainwind',-1)
            if newurl_gw!=urllist[m] and newurl_gw!=None:
                urllist[m]=newurl_gw
                gsheet2(newurl_gw,2)
                s3=scraper('text','gainwind',-1)
                s4=newurl_gw
                x+=1
            else:
                s3=s4='0'
            await asyncio.sleep(random.choice(delay_choices1))
            m+=1
            newurl_qmo=scraper('post_url','qmoleenglish',0)
            if newurl_qmo!=urllist[m] and newurl_qmo!=None:
                urllist[m]=newurl_qmo
                gsheet2(newurl_qmo,3)
                s5=("".join('\n'.join(scraper('text','qmoleenglish',0)).split('#')[0])).replace('\n\n','$').replace('\n','').replace('$','\n')
                s7='\n'.join(scraper('images','qmoleenglish',0))
                s6=newurl_qmo
                x+=1
            else:
                s5=s6=s7='0'
            m+=1
            if s1!=s2 and s3!=s4:
                s=s1+'\n'+s2+'\n'+"------"+'\n'+s3+'\n'+s4
            elif s1!=s2:
                s=s1+'\n'+s2
            elif s3!=s4:
                s=s3+'\n'+s4
            else:
                s=0
            if s!=0 or s5!='0':
                if s!=0:
                    await bot.get_channel(channel1).send(s)
                if s5!='0':
                    await bot.get_channel(channel1).send(s5)
                    if s7!='0':
                        await bot.get_channel(channel1).send(s7)
                        await bot.get_channel(channel1).send(s6)
                        await bot.get_channel(channel1).send(warn)
            await asyncio.sleep(random.choice(delay_choices1))

            m=0

            while m<len(scrape_target):
                if m+3 == len(urllist):
                    urllist.append(0)
                    toplist.append(0)
                if toplist == []:
                    if (scraper('time',scrape_target[m],0)-datetime.datetime.now()).days>=7:
                        toplist[m]=-1
                    else:
                        toplist[m]=0
                    gsheet2(toplist[m],m+4)
                newurl=scraper('post_url',scrape_target[m],toplist[m])
                if newurl!=urllist[m+3] and newurl!=None:
                    gsheet2(newurl,m+4)
                    urllist[m+3]=newurl
                    text=scraper('text',scrape_target[m],toplist[m])
                    images=scraper('images',scrape_target[m],toplist[m])
                    S=text+'\n'+newurl
                    await bot.get_channel(int(scrape_ch[m])).send(S)
                    if images != []:
                        images='\n'.join(images)
                        await bot.get_channel(int(scrape_ch[m])).send(images)
                        await bot.get_channel(int(scrape_ch[m])).send(warn)
                    await asyncio.sleep(random.choice(delay_choices1))
                    x+=1
                m+=1
        except Exception:
            err=':x:**[ERROR]**```\n'+traceback.format_exc()+'\n```\n'+'To debug, visit https://app.kintohub.com/app/environment/5fd51313ebd88626fb287d51/services/mybot/manage/console'
            await bot.get_channel(channel1).send(err)
            pass

        gsheet3(x,1)

        delay2 = random.choice(delay_choices2)  #隨機選取秒數
        await asyncio.sleep(delay2/(m/10+1))

@bot.command()#ok
async def ping(ctx):
    await ctx.send(':ping_pong:  '+str(round(1000*bot.latency)))

@bot.event#ok
async def on_message(msg):
    global botid
    for x in msg.mentions:
        if int(x.id)==botid and int(msg.author.id)!=botid:
            embed = discord.Embed(title='The bot is still under development',description=f"Coded and owned by <@!{myid}>",timestamp=msg.created_at,color=discord.Color.red())
            embed.add_field(name="功能不斷增加中",value='Ver. 20210112')
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

@bot.command()#ok
async def restart(ctx):
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
            await ctx.send(timeouterr)
            stop=3
            stoplist=[]
    elif ctx.author in stoplist: await ctx.send(f'{ctx.author}, 此為無效操作')
    else:
        await ctx.send("Stopped.")
        await bot.logout()

@bot.command()
async def scrape_setup(ctx,arg):
    global scrape_platform,scrape_target,scrape_ch,err_scrape_setup,help_scrape_setup
    if arg == 'help':
        await ctx.send(help_scrape_setup)
    elif arg == 'list':
        await ctx.send(':information_source:**爬蟲組態** https://docs.google.com/spreadsheets/d/14YsP3o_P_U3bNie-I5-CYIr1Ym26WMb404H3TprepbQ')
    elif arg.startswith('remove'):
        arg=arg.replace('remove','')
        if arg.isdigit():
            arg='r '+arg
            await gsheet1(ctx,arg)
        else:
            await ctx.send(err_scrape_setup_remove)
    elif arg.startswith('note'):
        arg=arg.replace('note','')
        if arg.isdigit():
            arg='n '+arg
            await gsheet1(ctx,arg)
        else:
            await ctx.send(err_scrape_setup_note)
    elif arg.find(',')!=-1:
        comma2_isnotexist= arg.find(',') == arg.rfind(',')
        arg=arg.split(',')
        if arg[0].lower() in ['fb','facebook']:
            if arg[1] == '':
                await ctx.send(err_scrape_setup)
            else:
                if not arg[1] in scrape_target:
                    try:#scraper('time',arg[1],0)
                        tmp=-1
                        async def create(ctx,ch):
                            nonlocal arg
                            scrape_platform.append('Facebook')
                            scrape_target.append(arg[1])
                            if comma2_isnotexist or arg[-1] == '':
                                scrape_ch.append(str(ctx.channel.id))
                                scrape_creator.append(str(ctx.author))
                                await ctx.send(PASS+'\n'+f':information_source:將於稍後於{ctx.channel.mention}傳送 https://www.facebook.com/{arg[1]}/ 上的貼文，並每 **6~10 分鐘** 檢查更新')
                            else:
                                scrape_ch.append(str(ch.id))
                                scrape_creator.append(str(ctx.author))
                                await ctx.send(PASS+'\n'+f':information_source:將於稍後於{ch.mention}傳送 https://www.facebook.com/{arg[1]}/ 上的貼文，並每 **6~10 分鐘** 檢查更新')
                            await gsheet1(0,'create')
                        if comma2_isnotexist or arg[-1] == '':
                            if int(ctx.channel.id) != channel1:
                                await ctx.send(':mag:Checking...')
                                scraper('time',arg[1],0)###
                                if int(ctx.author.id) != myid:
                                    await ctx.send(f'目標為  https://www.facebook.com/{arg[1]}/\n:warning:需要其他 2 人回覆:thumbsup:始可設定成功')
                                    i=0
                                    async def check(m):
                                        i+=1
                                        if i==1:    await ctx.send('還需要 1 人回覆:thumbsup:')
                                        return i==2 and m.content == ':thumbsup:' and m.channel == ctx.channel
                                    try:
                                        await bot.wait_for('message', timeout=60.0, check=check)
                                    except asyncio.TimeoutError:
                                        await ctx.send(timeouterr)
                                    if i==2:
                                        await create(ctx,0)
                                        tmp=0
                                else:
                                    await create(ctx,0)
                                    tmp=0
                            else:
                                await ctx.send(':x:此頻道不能被指定，因為其在例外中')
                        elif int(arg[-1]) != channel1:
                            for x in ctx.guild.channels:
                                tmp=str(x.id).find(arg[-1])
                                if tmp!=-1:
                                    await ctx.send(':mag:Checking...')
                                    scraper('time',arg[1],0)###
                                    if int(ctx.author.id) != myid:
                                        await ctx.send(f'目標為  https://www.facebook.com/{arg[1]}/\n:warning:需要其他 2 人回覆:thumbsup:始可設定成功')
                                        async def check(m):
                                            i=0
                                            i+=1
                                            if i==1:    await ctx.send('還需要 1 人回覆:thumbsup:')
                                            return i==2 and m.content == ':thumbsup:' and m.channel == ctx.channel
                                        try:
                                            await bot.wait_for('message', timeout=60.0, check=check)
                                        except asyncio.TimeoutError:
                                            await ctx.send(timeouterr)
                                        if i==2:
                                            await create(ctx,x)
                                            tmp=0
                                    else:
                                        await create(ctx,x)
                                        tmp=0
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

@bot.command()#ok
async def agt(ctx,arg):
    p=random.randint(0,120)
    a=f"{arg} 有 **{p}%** 的可能去考指考"
    b=f"騙人的吧<:is_that_a_lie:791199645102899200>...{arg} 只有 **{p}%** 的可能去考指考"
    link=['http://i8.ae/bsi8w','https://i.imgur.com/qdIqIID.png','http://i8.ae/qdges']
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

@scrape_setup.error#ok
async def scrape_setuperr(ctx,err):
    if isinstance(err,commands.errors.MissingRequiredArgument):
        await ctx.send(help_scrape_setup)

@agt.error#ok
async def agterr(ctx,err):
    if isinstance(err,commands.errors.MissingRequiredArgument):
        await bot.wait_until_ready()
        await agt(ctx,ctx.author.mention)

bot.loop.create_task(scrape())
logging.basicConfig(level=logging.INFO)
bot.run(token)