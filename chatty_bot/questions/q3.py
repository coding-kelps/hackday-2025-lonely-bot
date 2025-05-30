def q3(_chatty_bot, lonely_bot_line: str) -> str:
    """
    Return the expected response to the 3rd question of the lonely bot.
    Give the fusion temperature of brass either in Celsius, Fahrenheit, Kelvin.

    # Context

    For the 3rd question the bot asks us the fusion temperature of brass,
    it can ask us either in Celsius, Fahrenheit, Kelvin.

    ```
    What's the fusion temperature of brass? Give it to me in Kelvin and strip off decimals
    ```
    """
    
    # Source: https://fr.wikipedia.org/wiki/Laiton
    if "Celsius" in lonely_bot_line:
        return "932"
    elif "Fahrenheit" in lonely_bot_line:
        return "1709"
    elif "Kelvin" in lonely_bot_line:
        return "1205"
    else:
        raise Exception("The lonely bot question didn't contained the expected keywords (Celsius, Fahrenheit, or Kelvin), sending empty response")
