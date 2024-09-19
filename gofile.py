import os
import discord
from discord.ext import commands
import requests

# Intentsを有効にする
intents = discord.Intents.default()
intents.message_content = True  # メッセージの内容にアクセスするために必要

# Botオブジェクトを作成
bot = commands.Bot(command_prefix='!', intents=intents)

# ファイルサイズをMB単位で取得する関数
def get_file_size_in_mb(file_path: str) -> float:
    """
    指定されたファイルのサイズをMB単位で取得します。

    :param file_path: サイズを取得するファイルのパス
    :return: ファイルサイズ（MB単位）、ファイルが存在しない場合は-1
    """
    try:
        # ファイルサイズをバイト単位で取得
        file_size_bytes = os.path.getsize(file_path)
        # バイト単位からMB単位に変換（1MB = 1024 * 1024バイト）
        file_size_mb = file_size_bytes / (1024 * 1024)
        return file_size_mb
    except FileNotFoundError:
        return -1

# GoFileにファイルをアップロードしてダウンロードリンクを取得する関数
def upload_file_to_gofile(file_path: str) -> str:
    url = "https://store1.gofile.io/contents/uploadfile"
    
    # ファイルをアップロードするためのリクエスト
    with open(file_path, 'rb') as file:
        response = requests.post(url, files={'file': file})
    
    # レスポンスの処理
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'ok':
            return data['data']['downloadPage']
        else:
            return "Error: " + data['message']
    else:
        return "Failed to upload file: " + str(response.status_code)

# Discordのチャットメッセージからファイルパスを取得し、サイズを計測するコマンド
@bot.command()
async def filesize(ctx, *, file_path: str):
    # ファイルサイズを計測
    file_size_mb = get_file_size_in_mb(file_path)
    
    if file_size_mb != -1:
        if file_size_mb > 10:
            # アップロード中メッセージを先に送信
            uploading_message = await ctx.send(f"ファイルサイズは {file_size_mb:.2f} MB です。10MBを超えているため、GoFileにアップロード中です...")
            
            # GoFileにファイルをアップロード
            download_link = upload_file_to_gofile(file_path)
            
            # アップロード完了メッセージを送信
            await uploading_message.edit(content=f"アップロードが完了しました。ダウンロードリンク: {download_link}")
        else:
            await ctx.send(f"ファイルサイズは {file_size_mb:.2f} MB です。10MB以下なので、直接Discordに添付できます。")
    else:
        await ctx.send("ファイルが見つかりません。")

# Botを実行
bot.run('')  # YOUR_BOT_TOKEN を実際のトークンに置き換えてください
