from todlib import FileType
from utils.config import CONFIG

IMAGE_URL = "https://upload.yotsuba.giize.com/u/WHmfBtAj.jpeg"

def execute(client, sender, args, msg):
    user_name = msg.get("contact_name") or msg.get("name") or "Usuario"
    bot_name = CONFIG.get("bot_name", "Kazuma")

    menu_text = (
        f"¡Hola! Soy {bot_name} *(Mood)*.\n\n"
        "*☞︎︎︎ Aquí está mi lista de comandos ☜︎︎︎*\n\n"
        "┏━━━━✿︎ 𝐈𝐍𝐅𝐎-𝐁𝐎𝐓 ✿︎━━━━╮\n"
        "┃ ✐ *Owner* »\n"
        "┃ kazuma.giize.com/Dev-FelixOfc\n"
        "┃ ✐ *Commands* »\n"
        "┃ kazuma.giize.com/commands\n"
        "┃ ✐ *Upload* »\n"
        "┃ upload.yotsuba.giize.com\n"
        "┃ ✐ *Official channel* »\n"
        "┃ https://whatsapp.com/channel/0029Vb6sgWdJkK73qeLU0J0N\n"
        "╰━━━━━━━━━━━━━━━━━━━╯\n\n"
        "┏━━━━✿︎ 𝐈𝐍𝐅𝐎-𝐔𝐒𝐄𝐑 ✿︎━━━━╮\n"
        f"┃ ✐ *Usuario* » {user_name}\n"
        "╰━━━━━━━━━━━━━━━━━━━╯\n\n"
        "*» (❍ᴥ❍ʋ) `MAIN` «*\n"
        "> ꕥ Comandos de la categoría admins.\n\n"
        "✿︎ *#menu • #help*\n"
        "> ❀ Mira la lista de comandos completa.\n\n"
        "> © Developed by Félix"
    )

    try:
        client.send_file_message(
            to_phone=sender,
            url=IMAGE_URL,
            file_type=FileType.PICTURE,
            caption=menu_text,
            file_name="Menu_Kazuma.jpeg"
        )
    except Exception:
        client.send_message(sender, menu_text)
