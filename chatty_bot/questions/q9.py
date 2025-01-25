from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def q9(chatty_bot, lonely_bot_line: str) -> str:
    """
    Return the expected response to the 9th question of the lonely bot.
    Translating the given word in the required language.

    # Context

    For the 9th question the bot asks us to translate a random word into a
    random language.

    ```
    You're tough, let's see if you are so good in languages, because personally, I know a lot of them!
    I want you to translate the word /work/ in /bengali/
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
    conversation_history = [HumanMessage(content=lonely_bot_line)]
    prompt = prompt_template.format_prompt(
        msgs=conversation_history
    )
    
    return chatty_bot.model.invoke(prompt).content
