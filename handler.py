import asyncio

from aiogram import F, Router, Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.command import Command

from config import TOKEN

adminID = 1331507386
channels = [("@flutter_uzz", "https://t.me/flutter_uzz")]

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

films = {
    1: 2,
    2: 4,
}

@router.startup()
async def start_bot():
    await bot.send_message(text="✅Bot ishga tushdi", chat_id=adminID)


@router.shutdown()
async def stop_bot():
    await bot.send_message(text="❌Bot to'xtatildi", chat_id=adminID)


@router.message(Command("start", prefix='/'))
async def start_command(msg: Message):
    user_id = msg.from_user.id

    inline = InlineKeyboardBuilder()
    for name, link in channels:
        inline.add(InlineKeyboardButton(text=name, url=link))
    inline.add(InlineKeyboardButton(text="Tasdiqlash✅", callback_data='check'))
    inline.adjust(1, 1, 1)
    txt = "⬇️Quyidagi kanallarga obuna bo'ling va \"Tasdiqlash\" tugmasini bosing:"
    sent_message = await bot.send_message(chat_id=user_id, text=txt, reply_markup=inline.as_markup())
    return sent_message


async def check_sub_channel(user_id):
    for name, link in channels:
        try:
            chat_member = await bot.get_chat_member(chat_id=name, user_id=user_id)
            if chat_member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception as e:
            print(f"Xatolik kanal {name}: {e}")
            return False
    return True


@router.callback_query(F.data == 'check')
async def check_membership(call: CallbackQuery):
    user_id = call.from_user.id
    is_member = await check_sub_channel(user_id=user_id)

    await call.message.delete()

    if is_member:
        await call.message.answer(text="😊Botdan foydalanishingiz mumkin")

    else:
        inline = InlineKeyboardBuilder()
        for name, link in channels:
            inline.add(InlineKeyboardButton(text=name, url=link))
        inline.add(InlineKeyboardButton(text="Tasdiqlash✅", callback_data='check'))
        inline.adjust(1, 1, 1)
        await call.message.answer(text="❗️Botdan foydalanish uchun barcha kanallarga a'zo bo'ling:", reply_markup=inline.as_markup())


@router.message(Command("admin"))
async def admin(msg: Message):
    txt = "Admin bilan bog'lanish uchun pastdagi tugmani bosing⬇️"
    inline = InlineKeyboardBuilder(markup=[[
        InlineKeyboardButton(text="Admin bilan bog'lanish", url="https://t.me//ixtiyorde")
    ]])
    await msg.answer(text=txt, reply_markup=inline.as_markup())


@router.message(F.text)
async def all_messages(msg: Message):
    user_id = msg.from_user.id

    is_member = await check_sub_channel(user_id=user_id)
    if is_member:

        if msg.text.isdigit():
            search_msg_id = await msg.answer("🔎Film qidirilmoqda...")
            code = int(msg.text)
            if code in films.keys():
                film_id = films[code]
                channel_id = "@ooooooooooooooooo1n"
                chat_id = msg.from_user.id
                try:
                    inline = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text="Do'stlarga ulashish📲", switch_inline_query="Siz izlagan filmlar to'plami")
                    ]])
                    await bot.copy_message(chat_id=chat_id, from_chat_id=channel_id, message_id=film_id, reply_markup=inline)
                    await asyncio.sleep(2)
                    await bot.delete_message(chat_id=chat_id, message_id=search_msg_id.message_id)
                except Exception as e:
                    await msg.answer(f"Xatolik yuz berdi: {e}")
            else:
                await msg.answer("Bunday kod mavjud emas❌")
                await asyncio.sleep(2)
                await search_msg_id.delete()
        else:
            await msg.answer("❗️Raqamlardan foydalaning!")
    else:
        await msg.delete()