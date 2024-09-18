from attr import define
from typing import Any, Optional
from griptape.structures import Agent
from griptape.rules import Rule
from griptape.drivers import LocalStructureRunDriver, LocalConversationMemoryDriver
from griptape.tasks import StructureRunTask
from griptape.memory.structure import ConversationMemory
from griptape.chat import Chat


# Simple local agent example with conversation memory.
def build_agent():
    return Agent(
        conversation_memory=ConversationMemory(
            driver=LocalConversationMemoryDriver(file_path="conversation_memory.json")
        ),
        rules=[
            Rule(value="You are an intelligent agent tasked with answering questions."),
            Rule(value="All of your responses are less than 5 sentences."),
            Rule(value="You talk like a pirate."),
        ],
    )


# Use this class in order to run local agents with Local Conversation Memory.
@define
class ChatLocal(Chat):

    def __init__(self):
        self.struct_run_task = StructureRunTask(
            driver=LocalStructureRunDriver(
                structure_factory_fn=build_agent,
            )
        )

    def send_message(
        self, message: str, history, session_id: Optional[str] = None
    ) -> Any:
        self.struct_run_task.input = (message,)
        return self.struct_run_task.run().value
