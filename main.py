import discord, asyncio, datetime, urllib.request
import Weather_WebCrawl as Weather_py
import COVID_19
import lol_op_gg as lol_op
import youtube_dl, os
from discord.ext import commands


# 디스코드 봇의 권한 설정 부분 (매우 중요!!)
# 디스코드 봇 생성 시 애플리케이션 파트에 들어가서 Intents 권한 True로 설정하기.
# _intents = discord.Intents(messages=True, guilds=True, members=True)

# chunk_guilds_at_startup을 True로 설정해야 guild 객체의 함수를 사용할 수 있다.
# bot = commands.Bot(command_prefix='$lut_', chunk_guilds_at_startup=True, intents=_intents)
# chunk ... 와 intents 설정시 유튜브 음악 재생이 안 되는 버그로 인해 잠시 막아 둠

bot = commands.Bot(command_prefix='$lut_')
now = datetime.datetime.now()
is_voice_connected = False

# ---------- 유튜브 뮤직 플레이어 ----------

# 음성 채널 입장
@bot.command(name='join')
async def join(ctx):
    global is_voice_connected
    if not is_voice_connected:
        voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
        await voiceChannel.connect()
        is_voice_connected = True
    else:
        await ctx.send('이미 들어와있어 미린년아;;')
    return None


# 유튜브 음악 재생
@bot.command(name='play')
async def play(ctx, url : str):
    global is_voice_connected
    if is_voice_connected:
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("지금 재생중인거 먼저 멈춘 다음에 해;; $lut_stop")
            return

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # ydl.download([url])
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
        voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        # for file in os.listdir("./"):
        #     if file.endswith(".mp3"):
        #         os.rename(file, "song.mp3")
        # voice.play(discord.FFmpegPCMAudio("song.mp3"))
    else:
        await ctx.send('먼저 음성 채널에 참가시켜주고 해줘 ... $lut_join')


# 음성 채널 나가기
@bot.command(name='leave')
async def leave(ctx):
    global is_voice_connected
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if is_voice_connected:
        if voice.is_connected():
            await voice.disconnect()
            is_voice_connected = False
    else:
        await ctx.send("들어오지도 않았어 미린년아;;")


# 유튜브 음악 일시정지
@bot.command(name='pause')
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("재생도 안 하고 있는데 뭘 일시정지 하라는거야 잡년아;;")


# 유튜브 음악 다시재생
@bot.command(name='resume')
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("일시정지 하지도 않았어;;")


# 유튜브 음악 재생 멈추기
@bot.command(name='stop')
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()


# ---------- 코로나 알림 파트 ---------


# 코로나 브리핑
@bot.command(name='한국코로나브리핑')
async def fucking_covid(ctx):
    msg = 'Loading ... '
    await ctx.send(msg)
    my_covid_19_dict = COVID_19.updated_covid_19()

    print(f'({now}) {ctx.message.author} [{ctx.message.author.id}] : {ctx.message.content}')

    if my_covid_19_dict['is_ok']:

        # # 이미지를 지정한 URL에서 다운로드하여, 'covid_19_briefing.png'로 저장
        # urllib.request.urlretrieve(my_covid_19_dict['url'], 'covid_19_briefing.png')
        #
        # # 디스코드에 올릴 파일을 지정하고, attachment에서 사용할 이름을 'covid_19.png'로 지정
        # image = discord.File('covid_19_briefing.png', filename='covid_19.png')
        #
        # # Embed 구성
        # embed = discord.Embed(title=my_covid_19_dict['text'], description='', colour=0xF15F5F)

        embed = discord.Embed(title=my_covid_19_dict['title'], description='', colour=0xF15F5F)
        embed.add_field(name='일일확진자', value=f'{int(my_covid_19_dict["donate_occur"]) + int(my_covid_19_dict["overseas_occur"])}', inline=False)
        embed.add_field(name='국내발생', value=my_covid_19_dict['donate_occur'], inline=False)
        embed.add_field(name='해외발생', value=my_covid_19_dict['overseas_occur'], inline=False)
        embed.add_field(
            name='확진환자',
            value=my_covid_19_dict['total_infected_patients'] + '\n' + my_covid_19_dict['before_total'],
            inline=False
        )
        embed.add_field(
            name='격리해제',
            value=my_covid_19_dict['quarantine_release'] + '\n' + my_covid_19_dict['before_quarantine_release'],
            inline=False
        )
        embed.add_field(
            name='치료중',
            value=my_covid_19_dict['on_cure'] + '\n' + my_covid_19_dict['before_on_cure'],
            inline=False
        )
        embed.add_field(
            name='확진환자',
            value=my_covid_19_dict['death'] + '\n' + my_covid_19_dict['before_death'],
            inline=False
        )

        await ctx.send(embed=embed)
    else:
        msg = my_covid_19_dict['text']
        await ctx.send(msg)


# ---------- 날씨 알림 파트 ----------


# 날씨 브리핑
@bot.command(name='날씨')
async def my_weather(ctx):
    msg = '어디? 60초 안에 ㄱㄱ'
    await ctx.send(msg)

    print(f'({now}) {ctx.message.author} [{ctx.message.author.id}] : {ctx.message.content}')

    def check(react_msg):
        # 메시지가 비어있지 않고 동일한 채널에서 메시지를 보냈으며 메시지 작성자가 동일할 때
        return react_msg != "" and react_msg.channel == ctx.channel and react_msg.author == ctx.message.author

    try:
        location = await bot.wait_for('message', timeout=60.0, check=check)
        Finallocation = location.content + '날씨'

        # 지역 검색 실패 시
        if Finallocation is None:
            msg = 'Error! 지역 검색 오류 발생, 다시 물어볼거면 "$lut_날씨"를 통해 물어봐 잡년아 ㅋ'
            await ctx.send(msg)
        else:
            pass
    except asyncio.TimeoutError:
        await ctx.send(':middle_finger: 시간 지남 ㅅㄱ')
    else:
        my_dict = Weather_py.Crawling_Weather(Finallocation)
        embed = discord.Embed(title=(my_dict['지역'] + ' 날씨'), description='', colour=0xF15F5F)
        embed.add_field(name='현재 온도', value=my_dict['현재온도'], inline=False)
        embed.add_field(name='체감 온도', value=my_dict['체감온도'], inline=False)
        embed.add_field(name='오전 온도', value=my_dict['오전온도'], inline=False)
        embed.add_field(name='오후 온도', value=my_dict['오후온도'], inline=False)
        embed.add_field(name='현재 상태', value=my_dict['현재상태'], inline=False)
        embed.add_field(name='현재 자외선 지수', value=my_dict['현재자외선지수'], inline=False)
        embed.add_field(name='현재 미세먼지 농도', value=my_dict['현재미세먼지농도'], inline=False)
        embed.add_field(name='현재 초미세먼지 농도', value=my_dict['현재초미세먼지농도'], inline=False)
        embed.add_field(name='현재 오존 지수', value=my_dict['현재오존지수'], inline=False)
        embed.add_field(name='내일 오전 온도', value=my_dict['내일오전온도'], inline=False)
        embed.add_field(name='내일 오전 상태', value=my_dict['내일오전상태'], inline=False)
        embed.add_field(name='내일 오후 온도', value=my_dict['내일오후온도'], inline=False)
        embed.add_field(name='내일 오후 상태', value=my_dict['내일오후상태'], inline=False)

        await ctx.send('아잇! 어 prr 12번', embed=embed)

        print(f'({now}) {location.author} [{location.author.id}] : {location.content}')


# ---------- 롤 정보 스크래핑 ----------

# 롤 모스트 챔프 전적 (op.gg)
@bot.command(name='모스트검색')
async def most_champ(ctx):
    msg = '소환사 이름 입력 ㄱㄱ'
    await ctx.send(msg)

    print(f'({now}) {ctx.message.author} [{ctx.message.author.id}] : {ctx.message.content}')

    def check(react_msg):
        # 메시지가 비어있지 않고 동일한 채널에서 메시지를 보냈으며 메시지 작성자가 동일할 때
        return react_msg != "" and react_msg.channel == ctx.channel and react_msg.author == ctx.message.author

    try:
        name = await bot.wait_for('message', timeout=60.0, check=check)

        # 소환사 검색 실패 시
        if name is None:
            msg = 'Error! 소환사 검색 오류, 다시 물어볼거면 "$lut_모스트검색"를 통해 물어봐 잡년아 ㅋ'
            await ctx.send(msg)
        else:
            pass
    except asyncio.TimeoutError:
        await ctx.send(':middle_finger: 시간 지남 ㅅㄱ')
    else:
        most_list = lol_op.crapping_op_gg(name.content)

        if not most_list:
            await ctx.send('해당 소환사의 모스트 챔피언 정보 불어오기 실패')
        else:
            embed = discord.Embed(title='', description='', colour=0xF15F5F)
            embed.set_author(
                name=f"{most_list['user-info']['user-name']}  ({most_list['user-info']['level']})",
                icon_url='https:' + most_list['user-info']['profile-icon']
            )
            embed.set_thumbnail(url='https:' + most_list['user-info']['solo-rank'])
            await ctx.send(embed=embed)

            for champ in most_list['champ-list']:
                del embed
                embed = discord.Embed(title='', description='', colour=0xF15F5F)
                temp_name = ''
                for txt in champ['name']:
                    temp_name = temp_name + ' ' + txt
                embed.set_author(
                    name=f"{temp_name}",
                    icon_url='https:' + champ['face']
                )
                embed.set_thumbnail(url='https:' + champ['face'])
                embed.add_field(name='분당 CS', value=f"{champ['CSpMin'][1]}{champ['CSpMin'][2]}", inline=True)
                embed.add_field(name='평점', value=f"{champ['grade']}", inline=True)
                embed.add_field(name='K/D/A', value=f"{champ['kill']} / {champ['death']} / {champ['assist']}", inline=True)
                embed.add_field(name='게임 횟수', value=f"{champ['game_count']}", inline=True)
                embed.add_field(name='승률', value=f"{champ['winning_ratio'][0]}", inline=True)

                await ctx.send(embed=embed)
            msg='불러오기 종료'
            await ctx.send(msg)

        print(f'({now}) {name.author} [{name.author.id}] : {name.content}')


@bot.command()
async def null_txt(ctx):
    pass


# 디스코드 봇이 작동시작 했을 때
@bot.event
async def on_ready():
    print('client ID : ' + str(bot.user.id))
    print('discord.py version : ' + str(discord.__version__) + '\n')
    print('... 공부기계-001 ON\n')
    # 상태 메시지 설정
    # 종류는 3가지 : Game, Streaming, CustomActivity
    game = discord.Game('테스트 중')
    # 계정 상태를 변경한다.
    # online, idle, offline, etc
    await bot.change_presence(status=discord.Status.idle, activity=game)
    return None


# 프로그램이 실행되면 제일 처음으로 실행되는 구간
if __name__ == "__main__":
    # TOKEN 값을
    token = 'ODAxODAwMjA4MTc0Mjg0ODQw.YAl8og.wKxO7_XS2GISkaNf24TJHweFc5M'
    bot.run(token)