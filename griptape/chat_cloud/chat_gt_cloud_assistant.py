from attr import define
from typing import Any, Dict, List, Optional
from griptape.chat_cloud.chat_cloud import ChatCloud


# Class to run structures that are in a managed environment (Skatepark or GriptapeCloud)
@define
class ChatGTCloudAssistant(ChatCloud):

    def format_arguments(
        self,
        message: str,
        conversation_memory_id: Optional[str] = None,
        additional_args: Optional[List[str]] = [],
    ) -> list[str]:
        return []

    def format_run_kwargs(self, kwargs: Dict[str, Any] = {}) -> dict:
        formatted_kwargs: Dict = {"stream": True}
        if "message" in kwargs:
            formatted_kwargs["input"] = kwargs.get("message")
        if "conversation_memory_id" in kwargs:
            formatted_kwargs["thread_id"] = kwargs.get("conversation_memory_id")
        if (
            "knowledge_base_ids" in kwargs
            and kwargs.get("knowledge_base_ids") is not None
        ):
            formatted_kwargs["knowledge_base_ids"] = kwargs.get("knowledge_base_ids")
        if "ruleset_ids" in kwargs and kwargs.get("ruleset_ids") is not None:
            formatted_kwargs["ruleset_ids"] = kwargs.get("ruleset_ids")
        if "structure_ids" in kwargs and kwargs.get("structure_ids") is not None:
            formatted_kwargs["structure_ids"] = kwargs.get("structure_ids")
        return formatted_kwargs
