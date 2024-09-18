from abc import ABC, abstractmethod
from typing import Any, Optional
from griptape.tasks import StructureRunTask


# Interface for the chat agents - local and cloud.
class Chat(ABC):

    struct_run_task: StructureRunTask

    @abstractmethod
    def send_message(
        self, message: str, history: Any, conversation_memory_id: Optional[str] = None
    ) -> Any:
        pass
