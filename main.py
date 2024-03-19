import discord
from discord.ext import commands
from utils import *
from genimg import *
import aiohttp
import os
import json


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')

@bot.event
async def on_guild_join(guild):
    # 새로운 텍스트 채널을 생성합니다. 채널 이름은 '봇-채널'로 설정합니다.
    channel = await guild.create_text_channel('젠-채널')

    await channel.send(
        "안녕하세요! 저는 그림을 그려주는 봇입니다.\n"
        "다음은 제가 할 수 있는 일들입니다:\n"
        "- `!gen [명령]`: 명령에 기반하여 이미지를 생성합니다.\n"
        "- 이미지를 첨부하고 이미지에 대한 설명을 작성하면 이미지를 애니스타일로 변환하여 보여줍니다.(png, jpg, jpeg)"
    )

@bot.event
async def on_message(message):
    if message.channel.name == '젠-채널' or message.channel.name == 'ai이미지생성' or message.channel.name == 'gen':
        # 봇이 보낸 메시지는 무시합니다.
        if message.author == bot.user:
            return

        # 메시지에 첨부된 파일이 있는지 확인합니다.
        if message.attachments:
            keyword = ' '.join(message.content.split()[1:])
            print(keyword)
            prompt = get_prompt(keyword)
            print(prompt)
            # 모든 첨부 파일을 순회합니다.
            for attachment in message.attachments:
                # 첨부 파일이 이미지인 경우에만 반응합니다.
                if any(attachment.filename.lower().endswith(image_ext) for image_ext in ['png', 'jpg', 'jpeg']):
                    await message.channel.send("이미지 받음")
                    # 이미지를 비동기적으로 다운로드
                    async with aiohttp.ClientSession() as session:
                        async with session.get(attachment.url) as resp:
                            if resp.status != 200:
                                await message.channel.send("이미지를 다운 실패")
                                return
                            data = await resp.read()

                            # 이미지 파일 저장 경로 설정
                            save_path = f'images/{attachment.filename}'
                            os.makedirs(os.path.dirname(save_path), exist_ok=True)

                            # 이미지 파일 서버에 저장
                            with open(save_path, 'wb') as f:
                                f.write(data)
                                await message.channel.send(f"{attachment.filename} 이미지를 저장")
                            resize_image(save_path, save_path)
                            await message.channel.send(f"{attachment.filename} 이미지를 변환 중")
                            # 이미지 파일을 이용하여 이미지 생성
                            img_path = img_to_img(save_path, prompt)
                            await message.channel.send(file=discord.File(img_path))
        await bot.process_commands(message)

                        
 
@bot.command()
async def gen(ctx, *args):
    if ctx.channel.name == '젠-채널' or ctx.channel.name == 'ai이미지생성' or ctx.channel.name == 'gen':
        keyword = ' '.join(args)
        print(keyword)
        prompt = get_prompt(keyword)
        # prompt = keyword
        print(prompt)
        msg = await ctx.send("Generating...")
        img_path = gen_img(prompt)
        await msg.delete()
        await ctx.send(file=discord.File(img_path))

@bot.command()
async def 도움(ctx):
    if ctx.channel.name == '젠-채널' or ctx.channel.name == 'ai이미지생성' or ctx.channel.name == 'gen':
        await ctx.send(
            "다음은 제가 할 수 있는 일들입니다:\n"
            "- `!gen [명령]`: 명령에 기반하여 이미지를 생성합니다.\n"
            "- 이미지를 첨부하고 이미지에 대한 설명을 작성하면 이미지를 애니스타일로 변환하여 보여줍니다.(png, jpg, jpeg)"
        )

 
bot.run('YOUR_BOT_TOKEN')