import logging
import socket
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from .questions import *

LONELY_BOT_ENDLINE = "See you next time!"
LONELY_BOT_TIMEOUT = "... guess you don't want to answer me ..."
SIMPLE_QUESTION = 0
INTERACTIVE_QUESTION = 1

class ChattyBot():
    def __init__(self,
                 model: ChatOllama | ChatOpenAI,
                 challenge_host: str = "challenges.hackday.Fr",
                 challenge_port: int = 41521,
                 name: str = "ChattyBot"):
        self.name = name
        self.challenge_host = challenge_host
        self.challenge_port = challenge_port
        self.model = model
        self.lonely_bot_packet_size = 4096
        self.responses = []
        self.questions = [
            ("Would you care to spend some time with me ...?",                                                          q1,     SIMPLE_QUESTION     ),
            ("Starting with the basics, the name!",                                                                     q2,     SIMPLE_QUESTION     ),
            ("what's the fusion temperature of brass?",                                                                 q3,     SIMPLE_QUESTION     ),
            ("But, what about history?",                                                                                q4,     SIMPLE_QUESTION     ),
            ("Can't have you on this point, you know your basics! We'll see if you can keep up!",                       q5,     SIMPLE_QUESTION     ),
            ("You start with your name (format: 1,2,3,4)",                                                              q6,     SIMPLE_QUESTION     ),
            ("Let's play together!",                                                                                    q7,     INTERACTIVE_QUESTION),
            ("Let's start!",                                                                                            q8,     INTERACTIVE_QUESTION),
            ("I want you to translate the word",                                                                        q9,     SIMPLE_QUESTION     ),
            ("Here's the hash",                                                                                         q10,    SIMPLE_QUESTION     ),
        ]

    def listen_to_lonely_bot(self) -> str:
        if not self.socket:
            raise Exception("no connection to lonely bot")

        while True:
            data = self.socket.recv(self.lonely_bot_packet_size)

            if len(data) < 1:
                continue
            else:
                return data.decode('utf-8')[:-1] # Cut last newline
    

    def talk_to_lonely_bot(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.challenge_host, self.challenge_port))
        logging.debug(f"Connected to lonely bot server")

        question_counter = 0
        answered_question = 0

        lonely_bot_line = self.listen_to_lonely_bot()

        while lonely_bot_line != LONELY_BOT_ENDLINE:
            logging.debug(f"lonely bot send: \"{lonely_bot_line}\"")
            
            if answered_question:
                answered_question = False
                question_counter += 1
                logging.info(f"Passing to next question n°{question_counter+1}")

            if self.questions[question_counter][0] in lonely_bot_line:
                if self.questions[question_counter][2] == INTERACTIVE_QUESTION:
                    self.questions[question_counter][1](self, lonely_bot_line)
                else:
                    chatty_bot_line = self.questions[question_counter][1](self, lonely_bot_line)

                    self.socket.sendall(chatty_bot_line.encode('utf-8'))

                    logging.debug(f"chatty bot responded: \"{chatty_bot_line}\"")
                    self.responses.append(chatty_bot_line)
                
                answered_question = True
                
            lonely_bot_line = self.listen_to_lonely_bot()

        raise Exception(f"failed at question {question_counter+1}")
