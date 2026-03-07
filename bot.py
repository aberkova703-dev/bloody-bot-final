import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import CreateChannelRequest, SetDiscussionGroupRequest, InviteToChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest
from datetime import datetime

# ========== ТВОИ ДАННЫЕ ==========
API_ID = 34806533
API_HASH = 'bf5180f8d35810360bb3fd8d3062c14c'

# 👇 ТВОЯ STRING SESSION (уже вставлена)
STRING_SESSION = '1AZWarzsBuz7a0SzTBSe3_KqobeujNLorxkjvuFKnylJSczlxxjJl9jl2A3h6LtT9ahXuJ302dy1KUi1SxdoNkckkL5c-G3RfQAdQX4zToy84cYnkA3Ufi0ui-zMNW75Ql4SQBuANxmuauf4qaDP9UFBmqDBtaPXTfKd18jGUckowAznKaEBDzYlW-3vdAB50zRlLrnQ8Dz34tzM_MaIgbOvK3SUxBboUyrqU8Poo9q45gWiqkFOxMjooN341ck7xaaOM-dnrdnyI0Fx8dEb7e9RGSVNz2tV6FFYZo5kJvpctWC_S8rvQDcO6bcxzB0JIFpEEeonCLyQuzscmYuPkznaALtvvYZE='

ADMIN_ID = 7919926262
CHANNEL_ID = -1003746444921
MAIN_GROUP = -1003713581143
BACKUP_GROUP = -1003616098909
# =================================

BOTS_TO_ADD = [
    '@linkctl_bloodny429_bot',
    '@joinhidet_bot',
    '@selfharm_linkn_bot',
    '@RequestWeb534_bot',
    '@iris_black_bot'
]

BASE_TITLE = "BLOODный чат 🩸"
current_group = MAIN_GROUP
created_groups = []

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

async def add_bots_to_group(group_id):
    added = []
    failed = []
    for bot in BOTS_TO_ADD:
        try:
            print(f"➕ Добавляю {bot}...")
            bot_entity = await client.get_entity(bot)
            await client(InviteToChannelRequest(channel=group_id, users=[bot_entity]))
            added.append(bot)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ {bot}: {e}")
            failed.append(bot)
    return added, failed

async def create_and_link_group():
    try:
        group_name = BASE_TITLE
        print(f"\n🆕 Создаю группу: {group_name}")
        
        result = await client(CreateChannelRequest(
            title=group_name,
            about=f"Создана {datetime.now().strftime('%d.%m.%Y %H:%M')}",
            megagroup=True
        ))
        
        group = result.chats[0]
        group_id = int(f"-100{group.id}") if group.id > 0 else group.id
        print(f"✅ Группа создана! ID: {group_id}")

        added, failed = await add_bots_to_group(group_id)

        try:
            invite = await client(ExportChatInviteRequest(group))
            link = invite.link
            print(f"🔗 Ссылка: {link}")
        except:
            link = "не создана"

        try:
            channel = await client.get_entity(CHANNEL_ID)
            group_entity = await client.get_entity(group_id)
            await client(SetDiscussionGroupRequest(broadcast=channel, group=group_entity))
            linked = True
            print("✅ Привязано к каналу")
        except:
            linked = False
            print("❌ Не удалось привязать к каналу")

        created_groups.append({
            'id': group_id,
            'name': group_name,
            'link': link,
            'bots': added,
            'failed': failed,
            'linked': linked
        })

        msg = (f"🩸 **НОВЫЙ ЧАТ**\n\n"
               f"ID: `{group_id}`\n"
               f"🔗 {link}\n"
               f"✅ Ботов: {len(added)}/{len(BOTS_TO_ADD)}")
        
        await client.send_message(ADMIN_ID, msg)
        return group_id
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        await client.send_message(ADMIN_ID, f"❌ Ошибка: {e}")
        return None

@client.on(events.NewMessage)
async def handler(event):
    if event.sender_id != ADMIN_ID:
        return
    
    if event.text == '/start':
        await event.reply(
            "🩸 **BLOODный юзербот**\n\n"
            "📌 **Команды:**\n"
            "/status - статистика\n"
            "/create - создать чат"
        )
    
    elif event.text == '/status':
        status = f"📊 **Статус**\n\nСоздано чатов: {len(created_groups)}"
        await event.reply(status)
    
    elif event.text == '/create':
        await event.reply("🔄 Создаю чат...")
        group_id = await create_and_link_group()
        if group_id:
            await event.reply(f"✅ Чат создан!")

async def main():
    print("=" * 50)
    print("🩸 ЗАПУСК BLOODного ЮЗЕРБОТА")
    print("=" * 50)
    
    await client.start()
    
    me = await client.get_me()
    print(f"✅ Вошёл как: {me.first_name} (@{me.username})")
    print(f"✅ ID: {me.id}")
    print("=" * 50)
    
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Юзербот остановлен")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
