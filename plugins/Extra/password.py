# Don't Remove Credit @movie_file_20
# Subscribe YouTube Channel For Amazing Bot @movie_file_20
# Ask Doubt on telegram @KingVJ01

import random, os
from pyrogram import Client, filters, enums 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command(["genpassword", 'genpw']))
async def password(bot, update):
    message = await update.reply_text(text="`Processing...`")
    password = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+".lower()
    if len(update.command) > 1:
        qw = update.text.split(" ", 1)[1]
    else:
        ST = ["5", "7", "6", "9", "10", "12", "14", "8", "13"] 
        qw = random.choice(ST)
    limit = int(qw)
    random_value = "".join(random.sample(password, limit))
    txt = f"<b>Limit:</b> {str(limit)} \n<b>Password: <code>{random_value}</code>"
    btn = InlineKeyboardMarkup([[InlineKeyboardButton('JISSHU_BOTS', url='https://t.me/JISSHU_BOTS')]])
    await message.edit_text(text=txt, reply_markup=btn, parse_mode=enums.ParseMode.HTML)
