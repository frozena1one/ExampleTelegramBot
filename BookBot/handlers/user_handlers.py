from copy import deepcopy

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from database.database import user_dict_template, users_db
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from keyboards.bookmarks import create_bookmarks_keyboard, create_edit_bookmarks_keyboard
from keyboards.pagination import create_pagination_keyboard
from lexicon.lexicon import LEXICON
from services.file_handling import book


router = Router()


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.answer(text=LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)


@router.message(Command(commands='help'))
async def help_command(message: Message) -> None:
    await message.answer(text=LEXICON[message.text])


@router.message(Command(commands='beginning'))
async def begging_command(message: Message) -> None:
    users_db[message.from_user.id]['page'] = 1
    text = book[users_db[message.from_user.id]['page']]

    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            "backward",
            f"{users_db[message.from_user.id]['page']}/{len(book)}",
            "forward"
        )
    )


@router.message(Command(commands='continue'))
async def continue_command(message: Message) -> None:
    text = book[users_db[message.from_user.id]['page']]

    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(
            "backward",
            f"{users_db[message.from_user.id]['page']}/{len(book)}",
            "forward"
        )
    )


@router.message(Command(commands='bookmarks'))
async def bookmarks_command(message: Message) -> None:
    if users_db[message.from_user.id]['bookmarks']:
        await message.answer(
            text=LEXICON[message.text],
            reply_markup=create_bookmarks_keyboard(
                *users_db[message.from_user.id]['bookmarks']
            )
        )
    else:
        await message.answer(text=LEXICON['no_bookmarks'])


@router.callback_query(F.data == 'forward')
async def forward_button_press(callback_query: CallbackQuery) -> None:
    if users_db[callback_query.from_user.id]['page'] < len(book):
        users_db[callback_query.from_user.id]['page'] += 1
        text = book[users_db[callback_query.from_user.id]['page']]
        await callback_query.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                "backward",
                f"{users_db[callback_query.from_user.id]['page']}/{len(book)}",
                "forward"
            )
        )

    await callback_query.answer()


@router.callback_query(F.data == 'backward')
async def forward_button_press(callback_query: CallbackQuery) -> None:
    if users_db[callback_query.from_user.id]['page'] > 1:
        users_db[callback_query.from_user.id]['page'] -= 1
        text = book[users_db[callback_query.from_user.id]['page']]
        await callback_query.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                "backward",
                f"{users_db[callback_query.from_user.id]['page']}/{len(book)}",
                "forward"
            )
        )

    await callback_query.answer()


@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def page_button_press(callback_query: CallbackQuery):
    users_db[callback_query.from_user.id]['bookmarks'].add(
        users_db[callback_query.from_user.id]['page']
    )

    await callback_query.answer('Страница добавлена в закладки!')


@router.callback_query(IsDigitCallbackData())
async def bookmark_button_press(callback_query: CallbackQuery) -> None:
    text = book[users_db[callback_query.from_user.id]['page']]
    users_db[callback_query.from_user.id]['page'] = int(callback_query.data)

    await callback_query.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(
            "backward",
            f"{users_db[callback_query.from_user.id]['page']}/{len(book)}",
            "forward"
        )
    )

    await callback_query.answer()


@router.callback_query(F.data == 'edit_bookmarks')
async def edit_bookmarks_button_press(callback_query: CallbackQuery) -> None:
    await callback_query.message.edit_text(
        text=LEXICON[callback_query.data],
        reply_markup=create_edit_bookmarks_keyboard(
            *users_db[callback_query.from_user.id]['bookmarks']
        )
    )

    await callback_query.answer()


@router.callback_query(F.data == 'cancel')
async def cancel_button_press(callback_query: CallbackQuery) -> None:
    await callback_query.message.edit_text(text=LEXICON['cancel_text'])
    await callback_query.answer()


@router.callback_query(IsDelBookmarkCallbackData())
async def delete_bookmarks_button_press(callback_query: CallbackQuery) -> None:
    users_db[callback_query.from_user.id]['bookmarks'].remove(
        int(callback_query.data[:-3])
    )

    if users_db[callback_query.from_user.id]['bookmarks']:
        await callback_query.message.edit_text(
            text=LEXICON['/bookmarks'],
            reply_markup=create_edit_bookmarks_keyboard(
                *users_db[callback_query.from_user.id]["bookmarks"]
            )
        )
    else:
        await callback_query.message.edit_text(text=LEXICON['no_bookmarks'])

    await callback_query.answer()
