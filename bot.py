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
            phone_number=CONFIG["phone_number"],
            password=CONFIG["password"]
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
        self.client.phone_number = normalize_phone(phone)

        print(f"\n{Fore.MAGENTA}📨 Solicitando PIN de ToDus...")
        self.client.request_code(self.client.phone_number)

        pin = input(f"{Fore.WHITE}🔢 Ingresa el PIN recibido: {Fore.CYAN}").strip()
        
        # Validar y capturar el password generado
        self.client.validate_code(self.client.phone_number, pin)
        
        # Sincronizar el password al cliente para el login inmediato
        self.client.password = self.client.password 

        new_config = {
            "phone_number": self.client.phone_number,
            "password": self.client.password,
            "allowed_senders": [],
            "log_file": "bot.log"
        }

        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(new_config, f, indent=2)

        print(f"\n{Fore.GREEN}✔ Configuración guardada con éxito en config.json")
        print(f"{Fore.CYAN}⚙️ Iniciando sesión...\n")

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
                print(f"{Fore.BLUE}[CMD] {Fore.WHITE}{cmd_name} ejecutado por {Fore.CYAN}{sender}")
            except Exception as e:
                self.client.send_message(sender, f"Error: {e}")
                print(f"{Fore.RED}[ERR] {e}")

    def run(self):
        if not self.client.password:
            self.setup_account()

        print(f"{Fore.BLUE}{Style.BRIGHT}--- {CONFIG['bot_name']} ONLINE ---")
        print(f"{Fore.CYAN}Propietario: {Fore.WHITE}{CONFIG['owner']}")
        
        try:
            self.client.login()
            print(f"{Fore.GREEN}💡 Bot conectado y escuchando mensajes...\n")
            self.client.listen_messages(self.on_message)
        except Exception as e:
            print(f"{Fore.RED}💥 Error crítico al conectar: {e}")

if __name__ == "__main__":
    bot = KazumaBot()
    bot.run()