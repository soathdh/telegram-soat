import asyncio
import logging
from datetime import datetime
import pytz
from telethon import TelegramClient

# --- SOZLAMALAR ---
API_ID = 123456  
API_HASH = 'change_this_or_keep'

# Vaqt zonasi - O'zbekiston (Toshkent)
TZ = pytz.timezone('Asia/Tashkent')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    # Siz yuklagan fayl nomi clock_session bo'lgani uchun shu nom qoladi
    client = TelegramClient('clock_session', API_ID, API_HASH)
    
    await client.start()
    logging.info("Soat skripti VPS serverda muvaffaqiyatli ishga tushdi!")
    
    last_time = ""
    
    while True:
        try:
            # Hozirgi vaqtni Toshkent vaqti bilan olish
            now = datetime.now(TZ)
            current_time = now.strftime("%H:%M")
            
            # Agar daqiqa o'zgargan bo'lsa, nikni yangilash
            if current_time != last_time:
                new_first_name = f"FEIN | {current_time}"
                
                # Profilni yangilash
                from telethon.tl.functions.account import UpdateProfileRequest
                await client(UpdateProfileRequest(first_name=new_first_name))
                
                logging.info(f"Profil yangilandi: {new_first_name}")
                last_time = current_time
                
        except Exception as e:
            logging.error(f"Xatolik yuz berdi: {e}")
            
        # Har 15 soniyada tekshirib turish
        await asyncio.sleep(15)

if __name__ == '__main__':
    asyncio.run(main())
