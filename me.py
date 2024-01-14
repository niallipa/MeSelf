"""
    Version 0.01
"""

from pyrogram import Client, filters, idle
from pyrogram.errors import FloodWait
from time import sleep


accounts = [
    
    # Добавьте больше аккаунтов здесь
]

clients = []
for account in accounts:
    session_name = account['session_name']
    api_id = account['api_id']
    api_hash = account['api_hash']
    client = Client(session_name, api_id=api_id, api_hash=api_hash)
    clients.append(client)
    print(f"Client {session_name} has started.")
    client.start()

# Функция обработчика команды .type
def typee(client, msg):
    print(msg)
    print(msg.text)
    orig_text = msg.text.split(".type ", maxsplit=1)[1]
    text = orig_text
    tbp = ""  # to be printed
    typing_symbol = "▒"

    while tbp != orig_text:
        try:
            msg.edit(tbp + typing_symbol)
            sleep(0.05)  # 50 ms

            tbp = tbp + text[0]
            text = text[1:]

            msg.edit(tbp)
            sleep(0.05)

        except FloodWait as e:
            sleep(e.x)

def heart_filling(client, msg):
    heart_stages = [
        "🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤",
        "🖤🖤❤️❤️🖤🖤🖤🖤🖤❤️❤️🖤🖤",
        "🖤❤️❤️❤️❤️🖤🖤🖤❤️❤️❤️❤️🖤",
        "🖤❤️❤️❤️❤️❤️🖤❤️❤️❤️❤️❤️🖤",
        "🖤🖤❤️❤️❤️❤️❤️❤️❤️❤️❤️🖤🖤",
        "🖤🖤🖤❤️❤️❤️❤️❤️❤️❤️🖤🖤🖤",
        "🖤🖤🖤🖤❤️❤️❤️❤️❤️🖤🖤🖤🖤",
        "🖤🖤🖤🖤🖤❤️❤️❤️🖤🖤🖤🖤🖤",
        "🖤🖤🖤🖤🖤🖤❤️🖤🖤🖤🖤🖤🖤",
        "🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤"
    ]
    chat_id = msg.chat.id
    client.delete_messages(msg.chat.id, msg.id)
    message = client.send_message(chat_id, heart_stages[0])
    text = message.text
    for stage in heart_stages[1:]:
        try:
            text = text + "\n" + stage
            message.edit_text(text)
            sleep(0.3)
        except FloodWait as e:
            sleep(e.x)

def send_reactions(client, msg):
    msg.react(emoji='👍')



for client in clients:
    @client.on_message(filters.command("type", prefixes=".") & filters.me)
    def message_handler(client, message):
        typee(client, message)

    @client.on_message(filters.command("heart", prefixes=".") & filters.me)
    def message_handler(client, message):
        heart_filling(client, message)

    # @client.on_message(filters.text & ~filters.me)
    # def message_handler(client, message):
    #     send_reactions(client, message)

idle()