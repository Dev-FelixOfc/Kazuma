import os
import sys
import json
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

    def setup_account(self):
        os.system('clear')
        print(f"{Fore.BLUE}{Style.BRIGHT}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print(f"{Fore.BLUE}{Style.BRIGHT}┃                                                ┃")
        print(f"{Fore.CYAN}{Style.BRIGHT}┃    🌟 ¡BIENVENIDO A {CONFIG['bot_name'].upper()}!    ┃")
        print(f"{Fore.CYAN}┃         Desarrollado por Félix                 ┃")
        print(f"{Fore.BLUE}{Style.BRIGHT}┃                                                ┃")
        print(f"{Fore.BLUE}{Style.BRIGHT}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n")
        
        print(f"{Fore.YELLOW}➤ Configuración de cuenta nueva\n")
        
        phone = input(f"{Fore.WHITE}📱 Ingresa el número de ToDus (ej: 535XXXXXXX): {Fore.CYAN}").strip()
        num_final = normalize_phone(phone)
        
        self.client = ToDusClient2(phone_number=num_final)

        print(f"\n{Fore.MAGENTA}📨 Solicitando PIN de ToDus...")
        self.client.request_code()

        pin = input(f"{Fore.WHITE}🔢 Ingresa el PIN recibido: {Fore.CYAN}").strip()
        self.client.validate_code(pin)
        
        pass_generada = self.client.password

        new_config = {
            "phone_number": num_final,
            "password": pass_generada,
            "bot_name": CONFIG["bot_name"],
            "owner": CONFIG["owner"]
        }

        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(new_config, f, indent=2)

        print(f"\n{Fore.GREEN}✔ Configuración guardada con éxito.")
        print(f"{Fore.CYAN}⚙️ Iniciando sesión...\n")

    def on_message(self, msg):
        body = msg.get("body", "").strip()
        prefix_found = None
        for p in PREFIXES:
            if body.startswith(p):
                prefix_found = p
                break
        if not prefix_found: return

        parts = body[len(prefix_found):].split(maxsplit=1)
        cmd_name = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        sender = msg.get("from", "").split("@")[0]

        if cmd_name in self.commands:
            try:
                self.commands[cmd_name].execute(self.client, sender, args, msg)
                print(f"{Fore.BLUE}[CMD] {Fore.WHITE}{cmd_name} - {Fore.CYAN}{sender}")
            except Exception as e:
                print(f"{Fore.RED}[ERR] {e}")

    def run(self):
        if not CONFIG.get("password"):
            self.setup_account()
            with open(JSON_PATH, "r") as f:
                temp_cfg = json.load(f)
                self.client = ToDusClient2(
                    phone_number=temp_cfg["phone_number"],
                    password=temp_cfg["password"]
                )

        print(f"{Fore.BLUE}{Style.BRIGHT}--- {CONFIG['bot_name']} ONLINE ---")
        try:
            self.client.login()
            print(f"{Fore.GREEN}💡 Bot conectado y escuchando...\n")
            self.client.listen_messages(self.on_message)
        except Exception as e:
            print(f"{Fore.RED}💥 Error crítico: {e}")

if __name__ == "__main__":
    bot = KazumaBot()
    bot.run()