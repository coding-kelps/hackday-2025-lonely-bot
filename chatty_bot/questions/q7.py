import logging
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

LONELY_BOT_ENDLINE = "See you next time!"
Q7_ENDLINE = "Good game, you won!"

def q7(chatty_bot, lonely_bot_line: str):
    """
    Play rock-paper-scissors with the bot.

    # Context

    For the 7th question the bot asks us to play rock-paper-scissors with him.

    ```
    Now, I would like to play a little game with you, something more interactive!
    I hope you know the game rock-paper-scissors!
    I modified it a little bit, i'll explain.
    I'm going to give you my first move, and you'll answer with your two moves.
    My second move will be drawn randomly, and we'll see who wins!
    In case of draw, we play another pair of moves in the same way.
    To be simple, we're going to use R for Rock, P for Paper and S for Scissors.
    The format of your answer should be: R,P
    Let's play together!"
    ```
    """
    prompt_template = ChatPromptTemplate([
            SystemMessage("""
             You are responding to a robot which is just a facade for a form with a strict format, always with a single word.

             Example:

             Human: My first move is P! What are yours?
             Assistant: R,S
             """),
            MessagesPlaceholder("msgs")
        ])
    conversation_history = [HumanMessage(content="""
     Now, I would like to play a little game with you, something more interactive!
     I hope you know the game rock-paper-scissors!
     I modified it a little bit, i'll explain.
     I'm going to give you my first move, and you'll answer with your two moves.
     My second move will be drawn randomly, and we'll see who wins!
     In case of draw, we play another pair of moves in the same way.
     To be simple, we're going to use R for Rock, P for Paper and S for Scissors.
     The format of your answer should be: R,P
     Let's play together!
    """)]
    
    while lonely_bot_line != Q7_ENDLINE:
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

        logging.debug(f"chatty bot responded: \"{chatty_bot_line}\"")

        lonely_bot_line = chatty_bot.listen_to_lonely_bot()

        logging.debug(f"lonely bot send: \"{lonely_bot_line}\"")
    
    return
