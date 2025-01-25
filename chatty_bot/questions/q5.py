import base64

ENCODED_PHRASE = "I know many encoding bases, but which one i'm using...?"

def q5(chatty_bot, lonely_bot_line: str) -> str:
    """
    Return the expected response to the 5th question of the lonely bot.
    Give the encoding base of the lonely bot line.

    # Context

    For the 5th question the bot send us the encoded phrase
    "I know many encoding bases, but which one i'm using...?" in either base64
    or base85.

    ```
    Can't have you on this point, you know your basics! We'll see if you can keep up!
    Ng!)(Z+9SVVQzUKWo~0{WNB_^AYx&2WpgYbVs&&NcW7y2XdrKHWguxMZ6I}XX>MmOE-pU
    ```
    """
    hash = chatty_bot.listen_to_lonely_bot()
    
    if base64.b64decode(hash).decode("utf-8") == ENCODED_PHRASE:
        return "base64"
    elif base64.b85decode(hash).decode("utf-8") == ENCODED_PHRASE:
        return "base85"
    else:
        raise Exception("The lonely bot line didn't correspond to any encoding base, sending empty response")
