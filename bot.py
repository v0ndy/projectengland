import asyncio
import aiohttp
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.session.aiohttp import AiohttpSession

# ===== ТВОИ КЛЮЧИ =====
BOT_TOKEN = "8186015763:AAFcPWMoCIDM6ySUzxebkeLa2yTb95OPxqw"
QWEN_API_KEY = "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"
QWEN_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

# ===== ОБХОД БЛОКИРОВКИ =====
# Вариант 1: Если у тебя есть VPN (прокси)
# Раскомментируй строку ниже и укажи свой прокси
# session = AiohttpSession(proxy="http://127.0.0.1:10808")

# Вариант 2: Без прокси (просто попробуй)
session = AiohttpSession()

bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()

mood_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=str(i)) for i in range(1, 6)]],
    resize_keyboard=True
)

async def ask_qwen(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "qwen-turbo",
        "input": {"messages": [{"role": "user", "content": prompt}]}
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(QWEN_API_URL, headers=headers, json=payload, timeout=15) as resp:
                data = await resp.json()
                return data["output"]["text"]
    except Exception as e:
        return f"I'm here for you. (Note: {str(e)[:50]})"

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🤖 *AI MoodTracker Bot*\n\nI use Qwen AI.\n\n/mood - rate your day\n/test - quick check\nOr just text me!",
        parse_mode="Markdown"
    )

@dp.message(Command("mood"))
async def mood_cmd(message: types.Message):
    await message.answer("Rate your mood 1-5:", reply_markup=mood_kb)

@dp.message(lambda msg: msg.text in ["1","2","3","4","5"])
async def handle_mood(message: types.Message):
    mood = int(message.text)
    prompt = f"User mood {mood}/5. Respond supportively in 1 sentence."
    reply = await ask_qwen(prompt)
    await message.answer(reply, reply_markup=types.ReplyKeyboardRemove())

@dp.message(Command("test"))
async def test_cmd(message: types.Message):
    await message.answer("Send two numbers 0-3 (e.g., '1 2') for PHQ-2 test.")

@dp.message()
async def chat(message: types.Message):
    await message.answer("🧠 Thinking...")
    reply = await ask_qwen(message.text)
    await message.answer(reply)

async def main():
    print("🤖 Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())