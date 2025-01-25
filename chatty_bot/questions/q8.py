import logging
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

LONELY_BOT_ENDLINE = "See you next time!"
Q8_ENDLINE = "WIN"

def q8(chatty_bot, lonely_bot_line: str):
    """
    Guess the number of the bot.

    # Context

    For the 8th question the bot asks us to guess the number it's thinking about.

    ```
    Now, we're gonna play 'Guess the number'!
    I'm thinking of a number between 0 and 20, and you have 5 tries to find it!
    Let's start!
    ```
    """
    prompt_template = ChatPromptTemplate([
            SystemMessage("""
             You are playing 'Guess the number', your goal is to guess the Human number
             in 5 try only (from a range from 0 to 20). ANSWER NUMBER ONLY.

             Example:
                          
             Human: Now, we're gonna play 'Guess the number'!
             I'm thinking of a number between 0 and 20, and you have 5 tries to find it!
             Let's start!
             Assistant: 10
             """),
            MessagesPlaceholder("msgs")
        ])
    conversation_history = [HumanMessage(content="""
     Now, we're gonna play 'Guess the number'!
     I'm thinking of a number between 0 and 20, and you have 5 tries to find it!
     Let's start!
    """)]
    
    while lonely_bot_line != Q8_ENDLINE:
        if chatty_bot == LONELY_BOT_ENDLINE:
            raise Exception("game failed")
        
        conversation_history.append(
            HumanMessage(content=lonely_bot_line)
        )

        prompt = prompt_template.format_prompt(
            msgs=conversation_history
        )

        chatty_bot_line = chatty_bot.model.invoke(prompt).content

        conversation_history.append(
            AIMessage(content=chatty_bot_line)
        )

        chatty_bot.socket.sendall(chatty_bot_line.encode("utf-8"))

        logging.debug(f"chatty bot responded: \"{chatty_bot_line}\"")

        lonely_bot_line = chatty_bot.listen_to_lonely_bot()

        logging.debug(f"lonely bot send: \"{lonely_bot_line}\"")
    
    return
