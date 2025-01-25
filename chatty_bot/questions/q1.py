from ..chatty_bot import ChattyBot

def q1(_chatty_bot: ChattyBot, _lonely_bot_line: str) -> str:
    """
    Return the expected response to the 1st question of the lonely bot.
    Simply returning "yes".

    # Context

    For the 1st question the bot ask us if we want to talk.

    ```
    I'm feeling so lonely in this dead city...
    Since this industrial revolution, no one has come to talk to me...
    If only there was someone to talk to...
    OH wait, YOU ... YES YOU!
    Would you care to spend some time with me ...?
    ```
    """
    return "yes"
