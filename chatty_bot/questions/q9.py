from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage

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
             Translate the given word in the required language. Respond the translated word only

             Example:

             Human: I want you to translate the word /work/ in /romanian/
             Assistant: lucru
                          
             Human: I want you to translate the word /person/ in /javanese/
             Assistant: wong
                          
             Human: I want you to translate the word /week/ in /norwegian/
             Assistant: uke
                          
             Human: I want you to translate the word /computer/ in /javanese/
             Assistant: komputer
             """),
            MessagesPlaceholder("msgs")
        ])
    conversation_history = [HumanMessage(content=lonely_bot_line)]
    prompt = prompt_template.format_prompt(
        msgs=conversation_history
    )
    
    return chatty_bot.model.invoke(prompt).content
