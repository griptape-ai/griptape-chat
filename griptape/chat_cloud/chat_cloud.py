import logging
from attr import define, field, Factory
from typing import Any, Dict, List, Optional
from griptape.chat import Chat
import requests
import time

logger = logging.getLogger(__name__)


# Class to run structures that are in a managed environment (Skatepark or GriptapeCloud)
@define
class ChatCloud(Chat):
    base_url: str = field(kw_only=True)
    api_key: str = field(kw_only=True)
    structure_id: Optional[str] = field(kw_only=True, default=None)
    assistant_id: Optional[str] = field(kw_only=True, default=None)
    _resource_id: str = field(
        kw_only=True,
        default=Factory(
            lambda self: self.assistant_id if self.assistant_id else self.structure_id,
            takes_self=True,
        ),
    )
    _resource_type: str = field(
        kw_only=True,
        default=Factory(
            lambda self: "assistant" if self.assistant_id else "structure",
            takes_self=True,
        ),
    )

    def __attrs_post_init__(self) -> None:
        if self.assistant_id is None and self.structure_id is None:
            raise ValueError("Either structure_id or assistant_id must be provided")

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _create_run(self, args: List[str], kwargs: dict = {}) -> requests.Response:
        if self._resource_type == "assistant":
            url = f"{self.base_url}/api/assistants/{self.assistant_id}/runs"
        else:
            url = f"{self.base_url}/api/structures/{self.structure_id}/runs"

        input_dict = {"args": args}
        input_dict.update(kwargs)
        response = requests.post(
            f"{url}",
            json=input_dict,
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response

    def _list_events_for_run(
        self, run_id: str, offset: int, limit: int = 100
    ) -> requests.Response:
        if self._resource_type == "assistant":
            url = f"{self.base_url}/api/assistant-runs/{run_id}/events"
        else:
            url = f"{self.base_url}/api/structure-runs/{run_id}/events"
        response = requests.get(
            f"{url}",
            params={"offset": offset, "limit": limit},
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response

    def format_arguments(
        self,
        message: str,
        conversation_memory_id: Optional[str] = None,
        additional_args: Optional[List[str]] = [],
    ) -> list[str]: ...

    def format_run_kwargs(self, kwargs: Dict[str, Any] = {}) -> dict:
        return {}

    def send_message(
        self,
        message: str,
        history,
        conversation_memory_id: Optional[str] = None,
        knowledge_base_ids: Optional[List[str] | str] = None,
        ruleset_ids: Optional[List[str] | str] = None,
        structure_ids: Optional[List[str]] = None,
    ) -> Any:

        logger.info("Handling message")

        additional_args = []

        if isinstance(knowledge_base_ids, str):
            additional_args.extend(["-k", knowledge_base_ids])

        if isinstance(ruleset_ids, str):
            additional_args.extend(["-r", ruleset_ids])

        args = self.format_arguments(message, conversation_memory_id, additional_args)
        kwargs = self.format_run_kwargs(
            {
                "message": message,
                "conversation_memory_id": conversation_memory_id,
                "knowledge_base_ids": knowledge_base_ids,
                "ruleset_ids": ruleset_ids,
                "structure_ids": structure_ids,
            }
        )

        # Create StructureRun
        response = self._create_run(args, kwargs)
        response.raise_for_status()
        response_json = response.json()

        if self._resource_type == "assistant":
            run_id = response_json["assistant_run_id"]
        else:
            run_id = response_json["structure_run_id"]

        offset = 0  # NOTE: client should keep track of the offset
        partial_message = ""
        final_output = ""
        while True:
            response = self._list_events_for_run(run_id, offset)
            response.raise_for_status()
            response_json = response.json()
            events = response_json["events"]

            finished = False
            for event in events:
                if event["type"] in [
                    # "CompletionChunkEvent",
                    "TextChunkEvent",
                ]:  # Get chunks
                    partial_message += event["payload"]["token"]
                if event["type"] == "FinishStructureRunEvent":  # This means we're done
                    finished = True
                    final_output = event["payload"]["output_task_output"]["value"]
            if partial_message != "":
                yield partial_message  # NOTE: Gradio allows yielding partial messages for streaming
            if finished:
                # Handle Structures that are not streaming
                if final_output and partial_message == "":
                    yield final_output
                break

            offset = response_json["next_offset"]
            time.sleep(0.5)
