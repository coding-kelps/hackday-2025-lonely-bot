import re
import hashlib

ROCKYOU_FILEPATH = "./resources/rockyou-1000.txt"

def q10(_chatty_bot, lonely_bot_line: str) -> str:
    """
    Return the expected response to the 9th question of the lonely bot.
    Translating the given word in the required language.

    # Context

    For the 9th question the bot asks us to translate a random word into a
    random language.

    ```
    This time, we're going to play with hashes!
    I'm going to give you a password, but I'm not going to tell you what it is!
    I'll give you the md5 hash of it, and you'll have to find the password!
    I'm giving you a hint, you're kind to me, so I'm kind to you!
    The password is in the first hundred lines of the rockyou.txt file!"
    Here's the hash: /fc275ac3498d6ab0f0b4389f8e94422c/
    ```
    """

    encoded_word = re.findall(r'/[^/]*/', lonely_bot_line)[0][1:-1]

    with open(ROCKYOU_FILEPATH, "r", encoding="utf-8", errors="replace") as f:
        rockyou = [line.strip() for line in f if line.strip()]
    
    for word in rockyou:
        digest = hashlib.md5(word.encode("utf-8")).hexdigest()

        if digest == encoded_word:
            return word
    
    raise Exception("hash not found in rockyou list")
