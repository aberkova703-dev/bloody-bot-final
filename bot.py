import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

print("=== ЗАПУСК ТЕСТОВОГО БОТА ===")

# ========== ТВОИ ДАННЫЕ ==========
API_ID = 34806533
API_HASH = 'bf5180f8d35810360bb3fd8d3062c14c'
STRING_SESSION = '1AZWarzsBuz7a0SzTBSe3_KqobeujNLorxkjvuFKnylJSczlxxjJl9jl2A3h6LtT9ahXuJ302dy1KUi1SxdoNkckkL5c-G3RfQAdQX4zToy84cYnkA3Ufi0ui-zMNW75Ql4SQBuANxmuauf4qaDP9UFBmqDBtaPXTfKd18jGUckowAznKaEBDzYlW-3vdAB50zRlLrnQ8Dz34tzM_MaIgbOvK3SUxBboUyrqU8Poo9q45gWiqkFOxMjooN341ck7xaaOM-dnrdnyI0Fx8dEb7e9RGSVNz2tV6FFYZo5kJvpctWC_S8rvQDcO6bcxzB0JIFpEEeonCLyQuzscmYuPkznaALtvvYZE='

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

async def main():
    print("✅ Попытка подключения...")
    await client.start()
    me = await client.get_me()
    print(f"✅ УСПЕХ! Вошёл как: {me.first_name} (ID: {me.id})")
    print("✅ Бот готов и ждёт сообщений")
    await client.run_until_disconnected()

if __name__ == "__main__":
    print("🟢 Запуск main()")
    asyncio.run(main())
