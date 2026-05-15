import os
import sys
import json
import importlib
from todlib import ToDusClient2
from todlib.utils.util import normalize_phone
from utils.config import CONFIG, JSON_PATH

COMMANDS_DIR = os.path.join(os.path.dirname(__file__), "comandos")
PREFIXES = ["/", "#", "."]

class KazumaBot:
    def __init__(self):
        self.client = ToDusClient2(
            phone_number=CONFIG["phone_number"],
            password=CONFIG["password"]
        )
        self.commands = {}
        self.load_commands()

    def load_commands(self):
        self.commands.clear()
        if not os.path.exists(COMMANDS_DIR):
            os.makedirs(COMMANDS_DIR)

        for filename in os.listdir(COMMANDS_DIR):
            if filename.endswith(".py") and not filename.startswith("__"):
                cmd_name = filename[:-3]
                module_path = f"comandos.{cmd_name}"
                try:
                    if module_path in sys.modules:
                        importlib.reload(sys.modules[module_path])
                    module = importlib.import_module(module_path)
                    self.commands[cmd_name] = module
                    print(f"✅ {cmd_name}")
                except Exception as e:
                    print(f"❌ {cmd_name}: {e}")

    def setup_account(self):
        print(f"\n🌟 ¡Bienvenido a {CONFIG['bot_name']}!")
        print("Este bot es de código abierto. Vamos a configurar tu cuenta.\n")

        phone = input("📱 Ingresa el número de ToDus (ej: 535XXXXXXX): ").strip()
        self.client.phone_number = normalize_phone(phone)

        print("📨 Solicitando PIN de ToDus...")
        self.client.request_code(self.client.phone_number)

        pin = input("🔢 Ingresa el PIN recibido: ").strip()
        self.client.validate_code(self.client.phone_number, pin)

        new_config = {
            "phone_number": self.client.phone_number,
            "password": self.client.password,
            "allowed_senders": [],
            "log_file": "bot.log"
        }

        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(new_config, f, indent=2)

        print("\n✅ Configuración guardada en config.json")

    def on_message(self, msg):
        body = msg.get("body", "").strip()

        prefix_found = None
        for p in PREFIXES:
            if body.startswith(p):
                prefix_found = p
                break

        if not prefix_found:
            return

        parts = body[len(prefix_found):].split(maxsplit=1)
        if not parts:
            return

        cmd_name = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        sender = msg.get("from", "").split("@")[0]

        if cmd_name in self.commands:
            try:
                self.commands[cmd_name].execute(self.client, sender, args, msg)
            except Exception as e:
                self.client.send_message(sender, f"Error: {e}")

    def run(self):
        if not self.client.password:
            self.setup_account()

        print(f"\n--- {CONFIG['bot_name']} ONLINE ---")
        print(f"Propietario: {CONFIG['owner']}")
        self.client.login()
        self.client.listen_messages(self.on_message)

if __name__ == "__main__":
    bot = KazumaBot()
    bot.run()