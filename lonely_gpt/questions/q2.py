from ..lonely_gpt import LonelyGPT

def q2(lonely_gpt: LonelyGPT, _lonely_bot_line: str) -> str:
    """
    Return the expected response to the 2nd question of the lonely bot.
    Simply returning our name.

    # Context

    For the 2nd question the bot ask us our name.

    ```
    Starting with the basics, the name! Mine is Arabella Etheridge
    What's yours?"
    ```
    """
    if lonely_gpt.name:
        return lonely_gpt.name
    else:
        return "LonelyGPT"
