import os
from tempfile import TemporaryFile
from attr import define, field, Factory
from typing import Any
from dotenv import load_dotenv

from griptape.drivers import LocalVectorStoreDriver,OpenAiEmbeddingDriver
from griptape.loaders import PdfLoader
from griptape.rules import Ruleset, Rule
from griptape.structures import Agent
from griptape.tools import VectorStoreClient, BaseTool
from griptape.utils import load_file

load_dotenv()

@define
class Chat:
    open_ai_embedding_driver = OpenAiEmbeddingDriver ()
    vector_store_driver= LocalVectorStoreDriver (embedding_driver=open_ai_embedding_driver)

    agent: Agent = field(
        default=Factory( 
            lambda self: self.pdf_interact_with_Agent([]),
            takes_self=True
        )
    )
    def send_message(self, message: str) -> Any:
        return self.agent.run(message).output.value
    
    def upload_pdf(self, file: TemporaryFile) -> str:
        loaded_file= PdfLoader().load(load_file(file.name))
        namespace = os.path.basename(file.name)
        
        self.vector_store_driver.upsert_text_artifacts(
         {namespace: loaded_file}
        )
        vector_store_tool = VectorStoreClient (
            description=f"Contains information about a PDF with name {namespace}.",
            vector_store_driver=self.vector_store_driver,
            query_params={},
        ) 
        self.agent = self.pdf_interact_with_Agent(
            [vector_store_tool]
        )
        return file.name

    def pdf_interact_with_Agent(self,  tools: list[BaseTool]) -> Agent:
        return Agent(
            tools=tools,
            rulesets=[Ruleset(
                    name="PDF Chat Assistant",
                    rules=[
                        Rule("Only chat about things in the PDF file that you have access to"),
                        Rule("If you don't have access to a PDF file say that you don't have access to the PDF file")
                    ] 
                )
            ]
        )
   
