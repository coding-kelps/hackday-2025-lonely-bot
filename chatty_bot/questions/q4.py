from ..chatty_bot import ChattyBot

def q4(_chatty_bot: ChattyBot, lonely_bot_line: str) -> str:
    """
    Return the expected response to the 4th question of the lonely bot.
    Give the year in which the first vapor/eletric/diesiel/magnetic suspension
    train was built.

    # Context

    For the 4th question the bot asks us when does either the first
    vapor/eletric/diesiel/magnetic suspension train was built.

    ```
    But, what about history? When was the first vapor train built? Give me the year please!
    ```
    """
    
    if "vapor" in lonely_bot_line:
        return "1804"
    elif "electric" in lonely_bot_line:
        return "1879"
    elif "diesiel" in lonely_bot_line:
        return "1901"
    elif "magnetic suspension" in lonely_bot_line:
        return "1979"
    else:
        raise Exception("The lonely bot question didn't contained the expected keywords (vapor, eletric, diesiel, magnetic suspension), sending empty response")
