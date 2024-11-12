#!/usr/bin/env python3

import argparse
import sqlite3
import sys
import time

import telethon
from telethon import sync  # this module must be imported, although never used
from telethon.tl import functions, types

from config import TG_BOT_TOKEN


def sql_insert_group(con, entities):
    cursorObj = con.cursor()
    cursorObj.execute(
        "insert into 'group' ("
        "'group_id', 'group_name', 'group_title', 'user_count'"
        ") values ("
        "?, ?, ?, ?)",
        entities)
    con.commit()


def sql_insert_user(con, entities):
    cursorObj = con.cursor()
    cursorObj.execute(
        "insert into 'user' ("
        "'user_id', 'is_bot', 'name', 'username'"
        ") values ("
        "?, ?, ?, ?)",
        entities)
    con.commit()


async def get_group_users(chat, client):
    if isinstance(chat, types.Channel) or isinstance(chat, types.ChannelFull):
        # get users list
        try:
            print(chat.stringify())
            chat_users = await client.get_participants(chat.username,
                                                       aggressive=True)
            return (0, chat_users)
        except Exception as e:
            if 'ChatAdminRequiredError' in str(e):
                e = 'Only admins can see the list of users in this group'

            return (1, 'Error while getting groups users:\n\t%s' % e)
    elif isinstance(chat, types.ChatForbidden):
        return (1, '%s | no username | %s' % (chat.id, chat.title) + '\nThis is a private chat')
    else:
        return (1, 'WARNING: Chat type is not supported: %s' % type(chat))


def save_user_data(user, db_con):
    try:
        # save user data
        sql_insert_user(
            db_con,
            (user.id,
             user.bot,
             '%s %s' % (user.first_name, user.last_name),
             user.username),
        )
    except Exception as e:
        print('Error while saving user data:\n\t%s' % e)

    return


async def run_main(target_group, SESSION_NAME, APP_API_ID, APP_API_HASH):
    # login and start
    async with await telethon.TelegramClient(SESSION_NAME, APP_API_ID, APP_API_HASH).start(bot_token=TG_BOT_TOKEN) as client:
        chats = []
        if await client.is_user_authorized():
            try:
                chat_obj = await client(functions.channels.GetChannelsRequest(
                    id=[target_group]
                ))
                group = chat_obj.chats[0]
            except Exception as e:
                return 1, str(e)

            chats = [group]

        res = []
        # get groups participants
        for chat in chats:
            exc, chat_users = await get_group_users(chat, client)
            if exc == 1:
                return exc, chat_users
            if chat_users:
                for user in chat_users:
                    res.append(user.username)

        return 0, res
