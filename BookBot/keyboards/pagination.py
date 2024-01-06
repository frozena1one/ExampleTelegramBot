from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()

    keyboard_builder.row(*[InlineKeyboardButton(
        text=LEXICON[button] if button in LEXICON else button,
        callback_data=button) for button in buttons]
        )

    return keyboard_builder.as_markup()