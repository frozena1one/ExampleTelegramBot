from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU


router = Router()


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.answer(
        text=LEXICON_RU['/start']
    )

@router.message(Command(commands='help'))
async def help_command(message: Message) -> None:
    await message.answer(
        text=LEXICON_RU['/help']
    )