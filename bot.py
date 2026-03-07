import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Данные для входа
api_id = 34806533
api_hash = 'bf5180f8d35810360bb3fd8d3062c14c'
session_str = '1AZWarzsBuz7a0SzTBSe3_KqobeujNLorxkjvuFKnylJSczlxxjJl9jl2A3h6LtT9ahXuJ302dy1KUi1SxdoNkckkL5c-G3RfQAdQX4zToy84cYnkA3Ufi0ui-zMNW75Ql4SQBuANxmuauf4qaDP9UFBmqDBtaPXTfKd18jGUckowAznKaEBDzYlW-3vdAB50zRlLrnQ8Dz34tzM_MaIgbOvK3SUxBboUyrqU8Poo9q45gWiqkFOxMjooN341ck7xaaOM-dnrdnyI0Fx8dEb7e9RGSVNz2tV6FFYZo5kJvpctWC_S8rvQDcO6bcxzB0JIFpEEeonCLyQuzscmYuPkznaALtvvYZE='

client = TelegramClient(StringSession(session_str), api_id, api_hash)

async def main():
    print("🚀 Запуск...")
    await client.start()
    me = await client.get_me()
    print(f"✅ Успех! Вошел как: {me.first_name}")
    await client.run_until_disconnected()

@client.on(events.NewMessage)
async def handler(event):
    if event.text == '/start':
        await event.reply('🩸 BLOODny бот работает!')

if __name__ == '__main__':
    asyncio.run(main())
