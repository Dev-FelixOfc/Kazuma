import os
import sys
import importlib
from todlib import ToDusClient2
from utils.config import CONFIG

COMMANDS_DIR = os.path.join(os.path.dirname(__file__), "comandos")

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

    def on_message(self, msg):
        body = msg.get("body", "").strip()
        if not body.startswith(CONFIG["prefix"]):
            return

        parts = body[len(CONFIG["prefix"]):].split(maxsplit=1)
        cmd_name = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        sender = msg.get("from", "").split("@")[0]

        if cmd_name in self.commands:
            try:
                self.commands[cmd_name].execute(self.client, sender, args, msg)
            except Exception as e:
                self.client.send_message(sender, f"Error: {e}")

    def run(self):
        self.client.login()
        print(f"Bot: {CONFIG['bot_name']}")
        print(f"Owner: {CONFIG['owner']}")
        self.client.listen_messages(self.on_message)

if __name__ == "__main__":
    bot = KazumaBot()
    bot.run()