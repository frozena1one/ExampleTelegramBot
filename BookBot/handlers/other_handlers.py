from aiogram import Router
from aiogram.types import Message


router = Router()


@router.message()
async def send_echo(message: Message) -> None:
    await message.answer(text=f'Это эхо!\n{message.text}')