from abc import ABC, abstractmethod
from griptape.tasks import StructureRunTask
from typing import Any
from attr import define

@define
class Chat_Interface(ABC):

    struct_run_task: StructureRunTask

    @abstractmethod
    def send_message(self, message: str, history, session_id=None) -> Any:
        pass
