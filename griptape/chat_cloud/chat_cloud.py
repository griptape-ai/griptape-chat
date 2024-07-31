from attr import define, field, Factory
from typing import Any
import json
from griptape.drivers import GriptapeCloudStructureRunDriver
from griptape.tasks import StructureRunTask
from griptape.chat import Chat


# Class to run structures that are in a managed environment (Skatepark or GriptapeCloud)
@define
class Chat_Cloud(Chat):    

    def __init__(self, base_url:str, structure_id:str, api_key:str):
        self.struct_run_task = StructureRunTask(
                    driver=GriptapeCloudStructureRunDriver(
                        base_url=base_url,
                        structure_id=structure_id,
                        api_key=api_key,
                    )
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
    


