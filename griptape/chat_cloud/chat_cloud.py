import os
from attr import define, field, Factory
from typing import Any
from dotenv import load_dotenv
import json

from griptape.structures import Agent
from griptape.rules import Rule
from griptape.drivers import GriptapeCloudStructureRunDriver, LocalStructureRunDriver, LocalConversationMemoryDriver
from griptape.tasks import StructureRunTask
from griptape.memory.structure import ConversationMemory

#Load all environment variables 
load_dotenv()

# Get host
HOST = os.environ["GT_CLOUD_BASE_URL"]

# If with skatepark or with the cloud 
GT_STRUCTURE_ID = os.environ["GT_STRUCTURE_ID"]

# For the cloud 
GT_API_KEY = os.environ.get("GT_CLOUD_API_KEY","GRIPTAPE CLOUD API KEY ONLY NEEDED FOR STRUCTURES IN GRIPTAPE CLOUD")


# Local agent 
def build_agent():
    return Agent(
        conversation_memory=ConversationMemory(
            driver=LocalConversationMemoryDriver(
                file_path="conversation_memory.json"
            )),
        rules=[
            Rule(
                value = "You are an intelligent agent tasked with answering questions."
            ),
            Rule(
                value = "All of your responses are less than 5 sentences."
            )
        ]
        
    )


# Class to run structures that run in a managed environment (Skatepark or GriptapeCloud)
@define
class Chat_Cloud:
    struct_run_task: StructureRunTask = field(
        default=Factory(
            lambda: StructureRunTask(
                driver=GriptapeCloudStructureRunDriver(
                    base_url=HOST,
                    structure_id=GT_STRUCTURE_ID,
                    api_key=GT_API_KEY,
                )
            )
        ),
        kw_only=True,
    )

    def send_message(self, message: str, history, session_id:str = None) -> Any:
        if session_id:
            args = {
                "input": message,
                "session_id": session_id
            }
            self.struct_run_task.input = [json.dumps(args)]
        else: 
            self.struct_run_task.input = (message,)
        return self.struct_run_task.run().value
    
# Used this class in order to run local agents.
@define
class Chat_Local:
    struct_run_task: StructureRunTask = field(
        default=Factory(
            lambda: StructureRunTask(
                driver= LocalStructureRunDriver(
                    structure_factory_fn = build_agent,
                )
            )
        )
    )
    def send_message(self, message: str, history,) -> Any:
        self.struct_run_task.input = (message,)
        return self.struct_run_task.run().value

