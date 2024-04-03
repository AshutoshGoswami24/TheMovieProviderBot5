import asyncio 
from info import *
from imdb import Cinemagoer
from pymongo.errors import DuplicateKeyError
from pyrogram.errors import UserNotParticipant
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

dbclient = AsyncIOMotorClient(DATABASE_URI)
db = dbclient["Bisal-Chats"]
grp_col  = db["GROUPS"]
user_col = db["USERS"]
dlt_col  = db["Auto-Delete"]

ia = Cinemagoer()

async def add_group(group_id, group_name, user_name, user_id, channels, f_sub, verified):
    data = {"_id": group_id, "name":group_name, 
            "user_id":user_id, "user_name":user_name,
            "channels":channels, "f_sub":f_sub, "verified":verified}
    try:
       await grp_col.insert_one(data)
    except DuplicateKeyError:
       pass

async def get_group(id):
    data = {'_id':id}
    group = await grp_col.find_one(data)
    return dict(group)

async def update_group(id, new_data):
    data = {"_id":id}
    new_value = {"$set": new_data}
    await grp_col.update_one(data, new_value)

async def delete_group(id):
    data = {"_id":id}
    await grp_col.delete_one(data)

async def get_groups():
    count  = await grp_col.count_documents({})
    cursor = grp_col.find({})
    list   = await cursor.to_list(length=int(count))
    return count, list

async def add_user(id, name):
    data = {"_id":id, "name":name}
    try:
       await user_col.insert_one(data)
    except DuplicateKeyError:
       pass

async def get_users():
    count  = await user_col.count_documents({})
    cursor = user_col.find({})
    list   = await cursor.to_list(length=int(count))
    return count, list

async def save_dlt_message(message, time):
    data = {"chat_id": message.chat.id,
            "message_id": message.id,
            "time": time}
    await dlt_col.insert_one(data)
   
async def get_all_dlt_data(time):
    data     = {"time":{"$lte":time}}
    count    = await dlt_col.count_documents(data)
    cursor   = dlt_col.find(data)
    all_data = await cursor.to_list(length=int(count))
    return all_data

async def delete_all_dlt_data(time):   
    data = {"time":{"$lte":time}}
    await dlt_col.delete_many(data)

async def search_imdb(query):
    try:
       int(query)
       movie = ia.get_movie(query)
       return movie["title"]
    except:
       movies = ia.search_movie(query, results=10)
       list = []
       for movie in movies:
           title = movie["title"]
           try: year = f" - {movie['year']}"
           except: year = ""
           list.append({"title":title, "year":year, "id":movie.movieID})
       return list

async def force_sub(bot, message):
    group = await get_group(message.chat.id)
    f_sub = group["f_sub"]
    admin = group["user_id"]
    if f_sub==False:
       return True
    if message.from_user is None:
       return True 
    try:
       f_link = (await bot.get_chat(f_sub)).invite_link
       member = await bot.get_chat_member(f_sub, message.from_user.id)     
    
    except UserNotParticipant:
        join_button = InlineKeyboardButton("Jᴏɪɴ Cʜᴀɴɴᴇʟ", url=f_link)
        keyboard = [[join_button]]  # Create a list of lists for the InlineKeyboardMarkup
        if message.from_user:
            k = await message.reply(
                f"<b>⚠ Dᴇᴀʀ Usᴇʀ {message.from_user.mention}!\n\nᴛᴏ ɢᴇᴛ ᴍᴏᴠɪᴇs ᴅɪʀᴇᴄᴛʟʏ, ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ғɪʀsᴛ 🥶\n\n ᴀғᴛᴇʀ ᴊᴏɪɴɪɴɢ ᴄᴀᴍᴇ ʙᴀᴄᴋ ᴀɴᴅ sᴇᴀʀᴄʜ ᴀɢᴀɪɴ 👻</b>",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            k = await message.reply(
                "<b>⚠ Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ʙᴇғᴏʀᴇ sᴇɴᴅɪɴɢ ᴍᴇssᴀɢᴇs ᴛᴏ ᴛʜɪs ɢʀᴏᴜᴘ 🥶</b>",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        await message.delete()
        await asyncio.sleep(45)
        await k.delete()

        return False

    else:
       return True
