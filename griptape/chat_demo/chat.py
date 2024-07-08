import os
from tempfile import TemporaryFile
from attr import define, field, Factory
from typing import Any
from dotenv import load_dotenv


from griptape.tools import BaseTool
from griptape.drivers import OpenAiChatPromptDriver,LocalVectorStoreDriver,OpenAiEmbeddingDriver
from griptape.engines import VectorQueryEngine
from griptape.loaders import PdfLoader
from griptape.rules import Ruleset, Rule
from griptape.structures import Agent
from griptape.tools import VectorStoreClient
from griptape.config import OpenAiStructureConfig
from griptape.utils import load_file


load_dotenv()
#not sure if this config stuff is neccessary 
config = OpenAiStructureConfig()
config.prompt_driver = OpenAiChatPromptDriver(
   
    model="gpt-4o",
)

    
@define
class Chat:
    open_ai_embedding_driver = OpenAiEmbeddingDriver ()
    vector_store_driver= LocalVectorStoreDriver (embedding_driver=open_ai_embedding_driver)
    open_ai_prompt_driver= OpenAiChatPromptDriver(model="gpt-4o")

 
    
    agent: Agent = field(
        default=Factory( 
            lambda self: self.pdf_interact_w_Agent([]),
           
            takes_self=True
        )
    )
   

    vector_query_engine= VectorQueryEngine(
        prompt_driver=open_ai_prompt_driver,
        vector_store_driver= vector_store_driver,
    )

    def send_message(self, message: str) -> Any:
        return self.agent.run(message).output.value
    
    def upload_pdf(self, file: TemporaryFile) -> str:
        loaded_file= PdfLoader().load(load_file(file.name))
        namespace = os.path.basename(file.name)
        
        

        self.vector_query_engine.vector_store_driver.upsert_text_artifacts(
         {namespace: loaded_file}
        )
        
        vector_store_tool = VectorStoreClient (
    
            description=f"Contains information about a PDF with name {namespace}.",
            query_engine=self.vector_query_engine,
            namespace=namespace,
        ) 

        self.agent = self.pdf_interact_w_Agent(
            [vector_store_tool]
        )
            
        return file.name

    
    def pdf_interact_w_Agent(self,  tools: list[BaseTool]) -> Agent:
        return Agent(
            prompt_driver=OpenAiChatPromptDriver(model="gpt-4o"),
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
   
