from ..lonely_gpt import LonelyGPT
import hashlib

def q6(lonely_gpt: LonelyGPT, lonely_bot_line: str) -> str:
    """
    Return the expected response to the 6th question of the lonely bot.
    Identifying the requested encoding base to hash the past 4 responses.

    # Context

    For the 6th question the bot request us to hash the 4 previous
    response into a specific encoding base (sha1, sha256, sha512, md5).

    ```
    I'm preparing the other questions...
    While you wait, can you hash the previous answers in sha256?
    You start with your name (format: 1,2,3,4)
    ```
    """
    raw_response = ",".join(lonely_gpt.responses[1:])

    if "sha1" in lonely_bot_line:
        hash_object = hashlib.sha1(raw_response.encode("utf-8"))
    elif "sha256" in lonely_bot_line:
        hash_object = hashlib.sha256(raw_response.encode("utf-8"))
    elif "sha512" in lonely_bot_line:
        hash_object = hashlib.sha512(raw_response.encode("utf-8"))
    elif "md5" in lonely_bot_line:
        hash_object = hashlib.md5(raw_response.encode("utf-8"))
    else:
        raise Exception("The lonely bot question didn't contained the expected keywords (sha1, sha256, sha512, md5), sending empty response")
    
    return hash_object.hexdigest()
