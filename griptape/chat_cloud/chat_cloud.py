from attr import define, field
from typing import Any, Optional
from griptape.chat import Chat
import requests
import time


# Class to run structures that are in a managed environment (Skatepark or GriptapeCloud)
@define
class ChatCloud(Chat):
    base_url: str = field()
    structure_id: str = field()
    api_key: str = field()

    def __init__(self, base_url: str, structure_id: str, api_key: str):
        self.base_url = base_url
        self.structure_id = structure_id
        self.api_key = api_key

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _create_structure_run(self, args) -> requests.Response:
        response = requests.post(
            f"{self.base_url}/api/structures/{self.structure_id}/runs",
            json={"args": args},
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response

    def _list_events_for_structure_run(
        self, structure_run_id: str, offset: int, limit: int = 100
    ) -> requests.Response:
        response = requests.get(
            f"{self.base_url}/api/structure-runs/{structure_run_id}/events",
            params={"offset": offset, "limit": limit},
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response

    def format_arguments(
        self, message: str, conversation_memory_id: Optional[str] = None
    ) -> list[str]: ...

    def send_message(
        self, message: str, history, conversation_memory_id: Optional[str] = None
    ) -> Any:

        args = self.format_arguments(message, conversation_memory_id)

        # Create StructureRun
        response = self._create_structure_run(args)
        response.raise_for_status()
        response_json = response.json()
        structure_run_id = response_json["structure_run_id"]

        offset = 0  # NOTE: client should keep track of the offset
        partial_message = ""
        final_output = ""
        while True:
            response = self._list_events_for_structure_run(structure_run_id, offset)
            response.raise_for_status()
            response_json = response.json()
            events = response_json["events"]

            finished = False
            for event in events:
                if event["type"] == "CompletionChunkEvent":  # Get chunks
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
