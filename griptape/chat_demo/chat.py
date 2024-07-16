import os
from tempfile import TemporaryFile
from attr import define, field, Factory
from typing import Any
from dotenv import load_dotenv

from griptape.drivers import LocalVectorStoreDriver,OpenAiEmbeddingDriver,GriptapeCloudStructureRunDriver
from griptape.artifacts import TextArtifact

load_dotenv()

@define
class Chat:
    open_ai_embedding_driver = OpenAiEmbeddingDriver ()
    vector_store_driver= LocalVectorStoreDriver (embedding_driver=open_ai_embedding_driver)
    def send_message( self, message: str) -> Any:
        driver=GriptapeCloudStructureRunDriver(
                base_url=os.environ["GT_CLOUD_BASE_URL"],
                api_key=os.environ["GT_CLOUD_API_KEY"],
                structure_id=os.environ["GT_STRUCTURE_ID"],
            )
        return driver.run(TextArtifact(message)).value
   