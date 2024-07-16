import os
from tempfile import TemporaryFile
from attr import define, field, Factory
from typing import Any
from dotenv import load_dotenv

from griptape.drivers import LocalVectorStoreDriver,OpenAiEmbeddingDriver,GriptapeCloudStructureRunDriver
from griptape.loaders import PdfLoader
from griptape.rules import Ruleset, Rule
from griptape.structures import Agent
from griptape.tools import VectorStoreClient, BaseTool
from griptape.tasks import StructureRunTask
from griptape.utils import load_file

load_dotenv()

@define
class Chat:
    open_ai_embedding_driver = OpenAiEmbeddingDriver ()
    vector_store_driver= LocalVectorStoreDriver (embedding_driver=open_ai_embedding_driver)

    struct_run_task: StructureRunTask = field(
        default=Factory(
            lambda: StructureRunTask(
                driver=GriptapeCloudStructureRunDriver(
                    base_url=os.environ["GT_CLOUD_BASE_URL"],
                    api_key=os.environ["GT_CLOUD_API_KEY"],
                    structure_id=os.environ["GT_STRUCTURE_ID"],
                ),
            ),
        
        
        ),
        
        kw_only=True,
    )

    

   
    def send_message( self, message: str) -> Any:
        self.struct_run_task.input=(message, )
        return self.struct_run_task.run().value
    def upload_pdf(self,file:TemporaryFile)-> str:
        return file.name
        
    
















    #this is old PDF stuff, now time to get started on convo memory 

    '''
    def upload_pdf(self, file: TemporaryFile) -> str:
        # loaded_file= PdfLoader().load(load_file(file.name))
        # namespace = os.path.basename(file.name)
        # self.vector_store_driver.upsert_text_artifacts(
        #     {namespace: loaded_file}
        # )
        # vector_store_tool = VectorStoreClient (
        #     description=f"Contains information about a PDF with name {namespace}.",
        #     vector_store_driver=self.vector_store_driver,
        #     query_params={namespace:loaded_file},
        # )
        # self.struct_run_task= self.pdf_interact_with_Agent(
        #     [vector_store_tool]
        # )
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
   '''