import logging
from ..chatty_bot import ChattyBot, LONELY_BOT_ENDLINE
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

Q8_ENDLINE = "WIN"

def q8(chatty_bot: ChattyBot, lonely_bot_line: str):
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
             You are responding to a robot which is just a facade for a form with a strict format, always with a single word.

             Example:

             Human: Would you care to spend some time with me ...?
             Assistant: yes

             Human: Starting with the basics, the name! Mine is Patrick Marcellus Playfoot
             What's yours?
             Assistant: ChattyBot

             Human: But, what about history? When was the first vapor train built? Give me the year please!
             Assistant: 1804
             """),
            MessagesPlaceholder("msgs")
        ])
    conversation_history = [HumanMessage(content="""
     Now, we're gonna play 'Guess the number'!
     I'm thinking of a number between 0 and 20, and you have 5 tries to find it!
     Let's start!
    """)]
    
    while lonely_bot_line != Q8_ENDLINE:
        logging.debug(f"lonely bot send: \"{lonely_bot_line}\"")

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

        chatty_bot.socket.sendall(chatty_bot_line.encode('utf-8'))

        logging.debug(f"lonely gpt responded: \"{chatty_bot_line}\"")

        lonely_bot_line = chatty_bot.listen_to_lonely_bot()
    
    return
