from langchain_openai import ChatOpenAI
import logging
import os
from .lonely_gpt import LonelyGPT

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
    gpt = ChatOpenAI(
        model="gpt-4o",
        temperature=1.0,
        max_tokens=10,
        api_key=os.environ["OPENAI_API_KEY"],
    )

    lonely_gpt = LonelyGPT(gpt)

    try:
        lonely_gpt.talk_to_lonely_bot()
    except Exception as e:
        logging.error(f"{e.args}")