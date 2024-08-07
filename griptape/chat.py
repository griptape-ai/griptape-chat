from abc import ABC, abstractmethod
import json
from typing import Any
from griptape.tasks import StructureRunTask

#Interface for the chat agents - local and cloud. 
class Chat(ABC):
    
    struct_run_task: StructureRunTask

    @abstractmethod
    def send_message(self, message: str, history, session_id=None) -> Any:
        pass

