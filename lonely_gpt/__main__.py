from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
import logging
import socket
import os

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger('openai._base_client').setLevel(logging.WARNING)
logging.getLogger('httpcore.connection').setLevel(logging.WARNING)
logging.getLogger('httpcore.http11').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)



LONELY_BOT_ENDLINE = "See you next time!"
LONELY_BOT_TIMEOUT = "... guess you don't want to answer me ..."

class LonelyGPT():
    def __init__(self,
                 model: ChatOpenAI,
                 challenge_host: str = "challenges.hackday.Fr",
                 challenge_port: int = 41521):
        self.challenge_host = challenge_host
        self.challenge_port = challenge_port
        self.model = model
        self.lonely_bot_packet_size = 4096
        self.prompt_template = ChatPromptTemplate([
            ("system", "Respond using the fewest word possible"),
            ("system", "Respond to the last question of the robot only"),
            MessagesPlaceholder("msgs")
        ])
        self.conversation_history = []
    
    def talk_to_lonely_bot(self):
        interaction_count = 0

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.challenge_host, self.challenge_port))
            logging.debug(f"Connected to lonely bot server")

            while True:
                data = s.recv(self.lonely_bot_packet_size)

                if len(data) < 1:
                    continue
                else:
                    lonely_bot_line = data.decode('utf-8')

                    logging.debug(f"lonely bot send: \"{lonely_bot_line}\"")

                    self.conversation_history.append(
                        HumanMessage(content=lonely_bot_line)
                    )

                    if lonely_bot_line == LONELY_BOT_ENDLINE:
                        logging.warning(f"lonely bot ended conversation")

                        return
                    else:
                        if "?" in lonely_bot_line:
                            interaction_count += 1
                            logging.info(f"passed to interaction n°{interaction_count}")

                            prompt = self.prompt_template.format_prompt(
                                msgs=self.conversation_history
                            )

                            lonely_gpt_line = self.model.invoke(prompt).content.encode('utf-8')

                            s.sendall(lonely_gpt_line)

                            self.conversation_history.append(
                                AIMessage(content=lonely_gpt_line)
                            )
                            
                            logging.debug(f"lonely gpt responded: \"{lonely_gpt_line}\"")
                        else:
                            continue

if __name__ == "__main__":
    gpt = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=1.0,
        max_tokens=100,
        api_key=os.environ["OPENAI_API_KEY"],
    )

    lonely_gpt = LonelyGPT(gpt)

    lonely_gpt.talk_to_lonely_bot()
