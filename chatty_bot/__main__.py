from langchain_ollama import ChatOllama
import os
import logging
from .chatty_bot import ChattyBot

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Set logging level to Warning to avoid overwhelming logs in output
logging.getLogger('openai._base_client').setLevel(logging.WARNING)
logging.getLogger('httpcore.connection').setLevel(logging.WARNING)
logging.getLogger('httpcore.http11').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)

if __name__ == "__main__":
    model = ChatOllama(
        model="llama3.1:latest",
        temperature=1.0,
        max_tokens=15,
        base_url=os.environ["OLLAMA_BASE_URL"]
    )

    chatty_bot = ChattyBot(model)

    try:
        chatty_bot.talk_to_lonely_bot()
    except Exception as e:
        logging.error(f"{e.args[0]}")