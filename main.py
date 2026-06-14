
import sys

# Python 3.13+ uchun imghdr muammosini hal qilish (Railway xatolik bermasligi uchun)
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

# --- SOZLAMALAR ---
# Bu yerga o'zingizning API_ID va API_HASH qiymatlaringizni yozing
API_ID = 33618869  
API_HASH = '21f53d0ff713f14f3b8ef7606f9123eb'

# Vaqt zonasi - O'zbekiston (Toshkent)
TZ = pytz.timezone('Asia/Toshkent')

# Loglarni sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def main():
    # Sessiya fayli orqali ulanish
    client = TelegramClient('clock_session', API_ID, API_HASH)
    
    logging.info("Telegram Client ishga tushirilmoqda...")
    await client.start()
    logging.info("Sessiya muvaffaqiyatli ulandi!")

    last_time = ""

    while True:
        try:
            # Toshkent vaqti bo'yicha soat va minutni olish
            current_time = datetime.now(TZ).strftime("%H:%M")
            
            # Har minutda vaqt o'zgarganda nikni yangilash
            if current_time != last_time:
                # Aynan siz xohlagan format: FEIN | 23:45
                yangi_ism = f"FEIN | {current_time}"
                
                # Telegramda profil ismini o'zgartirish buyrug'i
                await client(UpdateProfileRequest(first_name=yangi_ism))
                logging.info(f"Profil ismi yangilandi: {yangi_ism}")
                
                last_time = current_time
                
        except Exception as e:
            logging.error(f"Ismni yangilashda xatolik: {e}")
            
        # Vaqtni har 30 soniyada tekshirib turish
        await asyncio.sleep(30)

if __name__ == '__main__':
    asyncio.run(main())
