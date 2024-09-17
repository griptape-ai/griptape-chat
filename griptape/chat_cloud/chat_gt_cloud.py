from attr import define
from typing import Optional
from griptape.chat_cloud.chat_cloud import ChatCloud


# Class to run structures that are in a managed environment (Skatepark or GriptapeCloud)
@define
class ChatGTCloud(ChatCloud):

    def format_arguments(
        self, message: str, conversation_memory_id: Optional[str] = None
    ) -> list[str]:
        if conversation_memory_id:
            return ["-p", message, "-t", conversation_memory_id, "-s"]
        else:
            return ["-p", message, "-s"]
