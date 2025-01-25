import logging
import base64

ENCODED_PHRASE = "I know many encoding bases, but which one i'm using...? (write your answer in lowercase like 'base64')".encode("utf-8")

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
    SSBrbm93IG1hbnkgZW5jb2RpbmcgYmFzZXMsIGJ1dCB3aGljaCBvbmUgaSdtIHVzaW5nLi4uPyAod3JpdGUgeW91ciBhbnN3ZXIgaW4gbG93ZXJjYXNlIGxpa2UgJ2Jhc2U2NCcp
    ```
    """
    hash = chatty_bot.listen_to_lonely_bot()
    logging.debug(f"lonely bot send: \"{hash}\"")
    
    try:
        if base64.b32decode(hash) == ENCODED_PHRASE:
            return "base32"
    except:
        0
    try:
        if base64.b64decode(hash) == ENCODED_PHRASE:
            return "base64"
    except:
        0
    try:
        if base64.b85decode(hash) == ENCODED_PHRASE:
            return "base85"
    except:
        0
    
    raise Exception("The lonely bot hash didn't correspond to any encoding base, sending empty response")
