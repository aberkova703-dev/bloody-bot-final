import sys
import subprocess
import asyncio
from datetime import datetime

print("🚀 STARTING BOT...", flush=True)
sys.stdout.flush()

# ===== АВТОУСТАНОВКА TELEGRAM =====
def install_telethon():
    try:
        import telethon
        print("✅ Telethon уже установлен", flush=True)
        return True
    except ImportError:
        print("🔄 Устанавливаю Telethon...", flush=True)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "telethon"])
            print("✅ Telethon установлен", flush=True)
            return True
        except Exception as e:
            print(f"❌ Ошибка установки: {e}", flush=True)
            return False

# Устанавливаем перед импортом
install_telethon()
sys.stdout.flush()

# Теперь импортируем
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import CreateChannelRequest, SetDiscussionGroupRequest, InviteToChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest

# ========== ТВОИ ДАННЫЕ ==========
API_ID = 34806533
API_HASH = 'bf5180f8d35810360bb3fd8d3062c14c'
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
is_creating_group = False  # Флаг для блокировки повторного создания

print("✅ Данные загружены", flush=True)
sys.stdout.flush()

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

async def add_bots_to_group(group_id):
    added = []
    failed = []
    for bot in BOTS_TO_ADD:
        try:
            print(f"➕ Добавляю {bot}...", flush=True)
            bot_entity = await client.get_entity(bot)
            await client(InviteToChannelRequest(channel=group_id, users=[bot_entity]))
            added.append(bot)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ {bot}: {e}", flush=True)
            failed.append(bot)
    return added, failed

async def check_group_health(entity_id):
    """Проверяет, жива ли группа"""
    try:
        await client.get_entity(entity_id)
        return True
    except:
        return False

async def create_and_link_group():
    try:
        group_name = BASE_TITLE
        print(f"\n🆕 Создаю группу: {group_name}", flush=True)
        
        result = await client(CreateChannelRequest(
            title=group_name,
            about=f"Создана {datetime.now().strftime('%d.%m.%Y %H:%M')}",
            megagroup=True
        ))
        
        group = result.chats[0]
        group_id = int(f"-100{group.id}") if group.id > 0 else group.id
        print(f"✅ Группа создана! ID: {group_id}", flush=True)

        added, failed = await add_bots_to_group(group_id)

        try:
            invite = await client(ExportChatInviteRequest(group))
            link = invite.link
            print(f"🔗 Ссылка: {link}", flush=True)
        except:
            link = "не создана"

        try:
            channel = await client.get_entity(CHANNEL_ID)
            group_entity = await client.get_entity(group_id)
            await client(SetDiscussionGroupRequest(broadcast=channel, group=group_entity))
            linked = True
            print("✅ Привязано к каналу", flush=True)
        except:
            linked = False
            print("❌ Не удалось привязать к каналу", flush=True)

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
        print("✅ Уведомление админу отправлено", flush=True)
        return group_id
        
    except Exception as e:
        print(f"❌ Ошибка: {e}", flush=True)
        try:
            await client.send_message(ADMIN_ID, f"❌ Ошибка: {e}")
        except:
            pass
        return None

@client.on(events.NewMessage)
async def handler(event):
    if event.sender_id != ADMIN_ID:
        return
    
    print(f"📩 Получена команда: {event.text}", flush=True)
    
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

@client.on(events.NewMessage(chats=CHANNEL_ID))
async def channel_handler(event):
    global current_group, is_creating_group
    
    print(f"\n📢 Новый пост в канале!", flush=True)
    
    # Если группа уже создается — ничего не делаем
    if is_creating_group:
        print(f"⏳ Группа уже создается, пропускаем этот пост...", flush=True)
        return
    
    # Проверяем текущую группу
    group_exists = await check_group_health(current_group)
    
    # Если группа не существует и не создается сейчас
    if not group_exists and not is_creating_group:
        print(f"⚠️ Группа {current_group} не найдена. Создаю новую...", flush=True)
        
        # Ставим флаг, что группа создается
        is_creating_group = True
        
        try:
            new_group_id = await create_and_link_group()
            if new_group_id:
                current_group = new_group_id
                print(f"✅ Новая группа создана и назначена: {current_group}", flush=True)
            else:
                print(f"❌ Не удалось создать группу", flush=True)
        finally:
            # Снимаем флаг в любом случае
            is_creating_group = False

async def main():
    print("=" * 50, flush=True)
    print("🩸 ЗАПУСК BLOODного ЮЗЕРБОТА", flush=True)
    print("=" * 50, flush=True)
    
    await client.start()
    
    me = await client.get_me()
    print(f"✅ Вошёл как: {me.first_name} (@{me.username})", flush=True)
    print(f"✅ ID: {me.id}", flush=True)
    print("=" * 50, flush=True)
    print("👀 Слушаю канал...", flush=True)
    print("=" * 50, flush=True)
    
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Юзербот остановлен", flush=True)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}", flush=True)
