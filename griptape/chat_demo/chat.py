import os
from typing import Any
from attr import define, field, Factory
from griptape.drivers import GriptapeCloudStructureRunDriver
from griptape.tasks import StructureRunTask


@define
class Chat:

    struct_run_task: StructureRunTask = field(
        default=Factory(
            lambda: StructureRunTask(
                driver=GriptapeCloudStructureRunDriver(
                    api_key=os.environ["GT_CLOUD_API_KEY"],
                    structure_id=os.environ["GT_CLOUD_STRUCTURE_ID"],
                )
            )
        ),
        kw_only=True,
    )

    def send_message(self, message: str) -> Any:
        self.struct_run_task.input = (message,)
        return self.struct_run_task.run().value
