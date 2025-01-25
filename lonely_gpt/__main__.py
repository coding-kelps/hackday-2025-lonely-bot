from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
import logging
import socket
import os
import hashlib
import re

from .rockyou import ROCKYOU

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Set logging level to Warning to avoid overwhelming logs in output
logging.getLogger('openai._base_client').setLevel(logging.WARNING)
logging.getLogger('httpcore.connection').setLevel(logging.WARNING)
logging.getLogger('httpcore.http11').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)

LONELY_BOT_ENDLINE = "See you next time!"
LONELY_BOT_TIMEOUT = "... guess you don't want to answer me ..."

trigger_patterns = [
    "?",
    "Let's start!",
    "Oups",
    "translate",
    "Here's the hash"
]

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
            ("system", """
             You are responding to a robot which is just a facade for a form with a strict format, always with a single word.

             Example:

             Human: Would you care to spend some time with me ...?
             Assistant: yes

             Human: Starting with the basics, the name! Mine is Patrick Marcellus Playfoot
             What's yours?
             Assistant: LonelyGPT

             Human: But, what about history? When was the first vapor train built? Give me the year please!
             Assistant: 1804
             """),
            ("system", "The fusion temperature of brass is 932 Celsius, 1205 Kelvin, or 1709 Farenheit"),
            ("system", "The first diesiel train was built in 1902"),
            ("system", "The first electric train was built in 1879"),
            ("system", "The first magnetic suspension train was built in 1979"),
            ("system", """When the human question doesn't look like a sentence respond by the encoding bases he used on its phrase
             Example:

             Human: SSBrbm93IG1hbnkgZW5jb2RpbmcgYmFzZXMsIGJ1dCB3aGljaCBvbmUgaSdtIHVzaW5nLi4uPw==
             Assistant: base64

             Human: Ng!)(Z+9SVVQzUKWo~0WNB_^AYx&2WpgYbVs&&NcW7y2XdrKHWguxMZ6IXX>MmOE-pU
             Assistant: base85
             """),
            MessagesPlaceholder("msgs")
        ])
        self.conversation_history = []
        self.responses = []
    
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
                    lonely_bot_line = data.decode('utf-8')[:-1] # Cut last newline


                    self.conversation_history.append(
                        HumanMessage(content=lonely_bot_line)
                    )

                    if any(pattern in lonely_bot_line for pattern in trigger_patterns) or (len(lonely_bot_line) > 12 and not " " in lonely_bot_line):
                        interaction_count += 1
                        logging.info(f"passed to interaction n°{interaction_count}")
                        
                        logging.debug(f"lonely bot send: \"{lonely_bot_line}\"")

                        if interaction_count == 6:
                            raw_response = ",".join(self.responses[1:])

                            if "sha1" in lonely_bot_line:
                                hash_object = hashlib.sha1(raw_response.encode("utf-8"))
                            elif "sha256" in lonely_bot_line:
                                hash_object = hashlib.sha256(raw_response.encode("utf-8"))
                            elif "sha512" in lonely_bot_line:
                                hash_object = hashlib.sha512(raw_response.encode("utf-8"))
                            elif "md5" in lonely_bot_line:
                                hash_object = hashlib.md5(raw_response.encode("utf-8"))
    
                            lonely_gpt_line = hash_object.hexdigest()
                        elif "Here's the hash" in lonely_bot_line:
                            to_find = re.findall(r'/[^/]*/', lonely_bot_line)[0][1:-1]

                            logging.debug(f"looking for {to_find}")

                            for e in ROCKYOU:
                                digest = hashlib.md5(e.encode("utf-8")).hexdigest()

                                if digest == to_find:
                                    lonely_bot_line = e
                                    break
                        else:
                            prompt = self.prompt_template.format_prompt(
                                msgs=self.conversation_history
                            )

                            lonely_gpt_line = self.model.invoke(prompt).content

                        s.sendall(lonely_gpt_line.encode('utf-8'))

                        self.conversation_history.append(
                            AIMessage(content=lonely_gpt_line)
                        )
                        self.responses.append(lonely_gpt_line)
                            
                        logging.debug(f"lonely gpt responded: \"{lonely_gpt_line}\"")
                    else:
                        logging.debug(f"lonely bot send: \"{lonely_bot_line}\"")

                        if lonely_bot_line == LONELY_BOT_ENDLINE:
                            logging.warning(f"lonely bot ended conversation")

                            return

if __name__ == "__main__":
    gpt = ChatOpenAI(
        model="gpt-4o",
        temperature=1.0,
        max_tokens=10,
        api_key=os.environ["OPENAI_API_KEY"],
    )

    lonely_gpt = LonelyGPT(gpt)

    lonely_gpt.talk_to_lonely_bot()
