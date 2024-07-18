import os
from attr import define, field, Factory
from typing import Any
from dotenv import load_dotenv

from griptape.structures import Agent
from griptape.rules import Rule
from griptape.drivers import OpenAiChatPromptDriver, GriptapeCloudStructureRunDriver, LocalStructureRunDriver
from griptape.tools import VectorStoreClient
from griptape.config import OpenAiStructureConfig
from griptape.tasks import StructureRunTask

#Load all environment variables 
load_dotenv()

# Get host
HOST = os.environ["GT_CLOUD_BASE_URL"]

# If with skatepark or with the cloud 
GT_STRUCTURE_ID = os.environ["GT_STRUCTURE_ID"]

# For the cloud 
GT_API_KEY = os.environ.get("GT_CLOUD_API_KEY","GRIPTAPE CLOUD API KEY ONLY NEEDED FOR STRUCTURES IN GRIPTAPE CLOUD")


# Local agent (a little silly) that I defined to test the Gradio app
def build_agent():
    return Agent(
        rules=[
            Rule(
                value = "You are very funny."
            ),
            Rule(
                value = "You end every response with 'haha'."
            )
        ]
    )

# Used this class in order to run GriptapeCloud and Skatepark. 
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

    def send_message(self, message: str, history) -> Any:
        self.struct_run_task.input = (message,)
        return self.struct_run_task.run().value
    
# Used this class in order to run the local agent that I defined above.
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

    def send_message(self, message: str, history) -> Any:
        self.struct_run_task.input = (message,)
        return self.struct_run_task.run().value