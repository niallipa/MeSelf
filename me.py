"""
    Version 0.01
"""

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from time import sleep


app = Client('MyAccaunt', api_id="3791635", api_hash="cb2263b73c0d8e8c192730ed2d0a5036")


# Команда type
@app.on_message(filters.command("type", prefixes=".") & filters.me)
def typee(_, msg):
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


app.run()
