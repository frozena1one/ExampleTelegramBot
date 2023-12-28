from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN = '5871731399:AAESNUPD2ZXDUgSi4-fwtL-3R0mWYQmmKTM'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['start']))
async def start_command(message: Message) -> None:
    await message.answer(
        text='Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь'
        )

@dp.message(Command(commands=['help']))
async def help_command(message: Message) -> None:
    await message.answer(
        text='Напиши мне что-нибудь,'
        'а я в ответ пришлю тебе твоё сообщение'
    )

@dp.message()
async def send_echo(message: Message) -> None:
    await message.reply(
        text=message.text
    )


if __name__ == '__main__':
    dp.run_polling(bot=bot)