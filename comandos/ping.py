import time
from utils.config import CONFIG

def execute(client, sender, args, msg):
    start_time = time.time()
    bot_name = CONFIG.get("bot_name", "Kazuma")
    msg_timestamp = msg.get("timestamp")
    
    if msg_timestamp:
        if msg_timestamp > 1000000000000:
            msg_timestamp /= 1000.0
        network_latency = start_time - msg_timestamp
        latency_ms = max(0, int(network_latency * 1000))
    else:
        execution_time = time.time() - start_time
        latency_ms = max(0, int(execution_time * 1000))

    ping_text = (
        f"⚡ [{bot_name}] PONG!\n\n"
        f"📡 Velocidad: `{latency_ms} ms`\n\n"
        "> © Developed by Félix"
    )

    try:
        client.send_message(sender, ping_text)
    except Exception:
        pass