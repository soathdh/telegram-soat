import sys
import os

# Python 3.13+ uchun imghdr muammosini majburlab hal qilish
try:
    import imghdr
except ImportError:
    import types
    imghdr = types.ModuleType('imghdr')
    imghdr.what = lambda filename, h=None: None
    sys.modules['imghdr'] = imghdr

import asyncio
import logging
from datetime import datetime
import pytz
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest

# --- SIZNING SOZLAMALARINGIZ (TAYYORLANDI) ---
API_ID = 33618869
API_HASH = '21f53d0ff713f14f3b8ef7606f9123eb'

# Vaqt zonasi - O'zbekiston (Tashkent)
TZ = pytz.timezone('Asia/Tashkent')

# Loglarni sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def main():
    session_name = 'clock_session'
    
    # Railway SQLite faylini o'qishda xato bermasligi uchun eski xotirani tozalash
    if os.path.exists(f"{session_name}.session-journal"):
        try:
            os.remove(f"{session_name}.session-journal")
        except Exception:
            pass

    # Telegram Client ulanishi
    client = TelegramClient(session_name, API_ID, API_HASH)
    
    logging.info("Telegram Client ishga tushirilmoqda...")
    await client.connect()
    
    if not await client.is_user_authorized():
        logging.error("Xatolik: Sessiya fayli mos kelmadi yoki tasdiqlanmagan!")
        return
        
    logging.info("Sessiya muvaffaqiyatli ulandi!")

    last_time = ""

    while True:
        try:
            # Toshkent vaqti bo'yicha soat va minutni olish
            current_time = datetime.now(TZ).strftime("%H:%M")
            
            # Har minutda vaqt o'zgarganda nikni yangilash
            if current_time != last_time:
                # Format: FEIN | 23:45
                yangi_ism = f"FEIN | {current_time}"
                
                # Nikni yangilash buyrug'i
                await client(UpdateProfileRequest(first_name=yangi_ism))
                logging.info(f"Profil ismi yangilandi: {yangi_ism}")
                
                last_time = current_time
                
        except Exception as e:
            logging.error(f"Ismni yangilashda xatolik yuz berdi: {e}")
            
        # Har 30 soniyada vaqtni tekshirish
        await asyncio.sleep(30)

if __name__ == '__main__':
    asyncio.run(main())
