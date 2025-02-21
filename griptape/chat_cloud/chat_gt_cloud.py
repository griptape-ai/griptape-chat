from attr import define
from typing import Optional
from griptape.chat_cloud.chat_cloud import ChatCloud


# Class to run structures that are in a managed environment (Skatepark or GriptapeCloud)
@define
class ChatGTCloud(ChatCloud):
    def format_arguments(
        self,
        message: str,
        conversation_memory_id: Optional[str] = None,
        knowledge_base_id: Optional[str] = None,
        ruleset_alias: Optional[str] = None,
    ) -> list[str]:
        if knowledge_base_id and conversation_memory_id and ruleset_alias:
            return [
                "-p",
                message,
                "-t",
                conversation_memory_id,
                "-k",
                knowledge_base_id,
                "-r",
                ruleset_alias,
                "-s",
            ]
        elif knowledge_base_id:
            return ["-p", message, "-k", knowledge_base_id, "-s"]
        elif conversation_memory_id:
            return ["-p", message, "-t", conversation_memory_id, "-s"]
        else:
            return ["-p", message, "-s"]
