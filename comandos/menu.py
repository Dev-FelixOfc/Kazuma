import requests
from todlib import FileType
from utils.config import CONFIG

IMAGE_URL = "https://upload.yotsuba.giize.com/u/WHmfBtAj.jpeg"

def execute(client, sender, args, msg):
    user_name = msg.get("contact_name") or msg.get("name") or "Usuario"
    bot_name = CONFIG.get("bot_name", "Kazuma")

    menu_text = (
        f"¡Hola! Soy {bot_name}\n\n"
        "☞︎︎︎ Aquí está mi lista de comandos ☜︎︎︎\n\n"
        "┏━━━━✿︎ 𝐈𝐍𝐅𝐎-𝐁𝐎𝐓 ✿︎━━━━╮\n"
        "┃ ✐ *Owner* »\n"
        "┃ kazuma.giize.com/Dev-FelixOfc\n"
        "┃ ✐ *Commands* »\n"
        "┃ kazuma.giize.com/commands\n"
        "┃ ✐ *Upload* »\n"
        "┃ upload.yotsuba.giize.com\n"
        "┃ ✐ *Official channel* »\n"
        "┃ https://chat.todus.cu/@0b19feada9d043baa03ce847a9984f7a\n"
        "╰━━━━━━━━━━━━━━━━━━━╯\n\n"
        "┏━━━━✿︎ 𝐈𝐍𝐅𝐎-𝐔𝐒𝐄𝐑 ✿︎━━━━╮\n"
        f"┃ ✐ *Usuario* » {user_name}\n"
        "╰━━━━━━━━━━━━━━━━━━━╯\n\n"
        "» (❍ᴥ❍ʋ) `MAIN` «\n"
        "> ꕥ Comandos de la categoría admins.\n\n"
        "✿︎ #menu • #help\n"
        "> ❀ Mira la lista de comandos completa.\n\n"
        "> © Developed by Félix"
    )

    try:
        # 1. Descargar la imagen del menú a memoria
        response = requests.get(IMAGE_URL)
        foto_bytes = response.content
        
        # 2. Subir la foto a ToDus para obtener la URL interna
        # Nota: Asegúrate de que 'upload_file' exista en la lib de tu bro
        url_todus = client.upload_file(foto_bytes, file_type=FileType.PICTURE)
        
        # 3. Enviar el mensaje con la foto adjunta
        client.send_file_message(
            to_phone=sender,
            url=url_todus,
            file_type=FileType.PICTURE,
            caption=menu_text,
            file_name="Menu_Kazuma.jpeg",
            file_size=len(foto_bytes)
        )
    except Exception as e:
        # Si algo falla (ej. no hay internet para descargar la foto), manda solo texto
        print(f"Error enviando foto: {e}")
        try:
            client.send_message(sender, menu_text)
        except Exception:
            pass