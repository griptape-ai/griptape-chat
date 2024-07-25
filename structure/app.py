
from attr import define, field, Factory
from typing import Any
from dotenv import load_dotenv

from uuid import uuid4 as uuid
from griptape.structures import Agent
from griptape.rules import Rule
from griptape.drivers import OpenAiChatPromptDriver,  LocalStructureRunDriver, LocalConversationMemoryDriver
from griptape.tasks import StructureRunTask
from griptape.memory.structure import ConversationMemory
def build_agent():
    return Agent(
        prompt_driver=LocalStructureRunDriver(
            
        ),
        conversation_memory=ConversationMemory(
            driver=LocalConversationMemoryDriver(
                file_path="conversation_memory.json"
            )),
        rules=[
            Rule(
                value = "You are very funny."
            ),
            Rule(
                value = "You end every response with 'haha'."
            )
        ]
    )