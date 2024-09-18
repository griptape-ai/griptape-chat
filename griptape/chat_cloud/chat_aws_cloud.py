from attr import define
from typing import Optional
import json
from griptape.chat_cloud.chat_cloud import ChatCloud


# Class to run structures that are in a managed environment (Skatepark or GriptapeCloud)
@define
class ChatAwsCloud(ChatCloud):

    def format_arguments(
        self, message: str, conversation_memory_id: Optional[str] = None
    ) -> list[str]:
        if conversation_memory_id:
            return [
                json.dumps({"input": message, "session_id": conversation_memory_id})
            ]
        else:
            return [message]
