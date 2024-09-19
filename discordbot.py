# インストールした discord.py を読み込む
import discord
intents = discord.Intents.default()
intents.voice_states = True  # ボイスステートの変更を検知するために必要

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'MTI3NzkyNDkyNjI4ODA0MDAxOQ.GPtg_a.yeRrGeibacSQb7CecS08ZEERM4g-7mO574hQ90'

# 接続に必要なオブジェクトを生成
intents = discord.Intents.default()  # デフォルトのIntentsを使用
intents.message_content = True  # メッセージの内容を取得する場合
client = discord.Client(intents=intents)

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_voice_state_update(member, before, after):
    # 参加
    if before.channel is None and after.channel is not None:
        await after.channel.send(f'{member.display_name} がボイスチャンネルに参加しました！')

    # 退出
    elif before.channel is not None and after.channel is None:
        await before.channel.send(f'{member.display_name} がボイスチャンネルを退出しました！')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
