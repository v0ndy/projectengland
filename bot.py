import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BOT_TOKEN = "8186015763:AAFcPWMoCIDM6ySUzxebkeLa2yTb95OPxqw"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

mood_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=str(i)) for i in range(1, 6)]],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("🤖 MoodTracker Bot\n\n/mood - rate your day\n/test - depression check")

@dp.message(Command("mood"))
async def mood_cmd(message: types.Message):
    await message.answer("How are you feeling?\n1=Bad 😞  5=Excellent 😊", reply_markup=mood_kb)

@dp.message(lambda msg: msg.text in ["1","2","3","4","5"])
async def handle_mood(message: types.Message):
    mood = int(message.text)
    if mood <= 2:
        reply = "Sorry you had a tough day. Be kind to yourself."
    elif mood == 3:
        reply = "Neutral day is okay. Tomorrow can be better."
    else:
        reply = "Glad you had a good day! Remember this feeling."
    await message.answer(reply, reply_markup=types.ReplyKeyboardRemove())

@dp.message(Command("test"))
async def test_cmd(message: types.Message):
    await message.answer("Send two numbers 0-3 (example: 1 2)")

@dp.message()
async def chat(message: types.Message):
    await message.answer("I'm a simple bot. Try /mood or /test")

async def main():
    print("🤖 Bot is running on Render!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
