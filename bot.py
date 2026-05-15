import os
import sys
import json
import time
import importlib
from colorama import Fore, Style, init
from todlib import ToDusClient2
from todlib.utils.util import normalize_phone
from utils.config import CONFIG, JSON_PATH

init(autoreset=True)

COMMANDS_DIR = os.path.join(os.path.dirname(__file__), "comandos")
PREFIXES = ["/", "#", "."]

class KazumaBot:
    def __init__(self):
        self.client = ToDusClient2(
            phone_number=CONFIG.get("phone_number", ""),
            password=CONFIG.get("password", "")
        )
        self.commands = {}
        self.last_command_time = {} # Para el control de spam
        self.load_commands()

    def load_commands(self):
        self.commands.clear()
        if not os.path.exists(COMMANDS_DIR):
            os.makedirs(COMMANDS_DIR)

        print(f"\n{Fore.CYAN}🚀 Cargando módulos...")
        for filename in os.listdir(COMMANDS_DIR):
            if filename.endswith(".py") and not filename.startswith("__"):
                cmd_name = filename[:-3]
                module_path = f"comandos.{cmd_name}"
                try:
                    if module_path in sys.modules:
                        importlib.reload(sys.modules[module_path])
                    module = importlib.import_module(module_path)
                    self.commands[cmd_name] = module
                    print(f"{Fore.GREEN}  ✅ {cmd_name}")
                except Exception as e:
                    print(f"{Fore.RED}  ❌ {cmd_name}: {e}")

    def on_message(self, msg):
        sender = msg.get("from", "").split("@")[0]
        
        # 1. ANTIBUCLE: Ignorar si el mensaje es del propio bot
        if sender == self.client.phone_number:
            return

        body = msg.get("body", "").strip()
        prefix_found = None
        for p in PREFIXES:
            if body.startswith(p):
                prefix_found = p
                break
        
        if not prefix_found: 
            return

        parts = body[len(prefix_found):].split(maxsplit=1)
        cmd_name = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        # 2. ANTISPAM: Cooldown de 2 segundos por usuario
        current_time = time.time()
        if sender in self.last_command_time:
            if current_time - self.last_command_time[sender] < 2:
                return
        
        if cmd_name in self.commands:
            self.last_command_time[sender] = current_time
            try:
                self.commands[cmd_name].execute(self.client, sender, args, msg)
                print(f"{Fore.BLUE}[CMD] {Fore.WHITE}{cmd_name} - {Fore.CYAN}{sender}")
            except Exception as e:
                print(f"{Fore.RED}[ERR en {cmd_name}]: {e}")

    def run(self):
        print(f"{Fore.BLUE}{Style.BRIGHT}--- {CONFIG['bot_name']} ONLINE ---")
        try:
            self.client.login()
            print(f"{Fore.GREEN}💡 Bot conectado y escuchando...\n")
            self.client.listen_messages(self.on_message)
        except Exception as e:
            print(f"{Fore.RED}💥 Error: {e}")

if __name__ == "__main__":
    bot = KazumaBot()
    bot.run()