import os
from tempfile import TemporaryFile
from attr import define, field, Factory
from griptape.core import BaseTool
from griptape.drivers import OpenAiPromptDriver
from griptape.engines import VectorQueryEngine
from griptape.loaders import PdfLoader
from griptape.memory.structure import ConversationMemory
from griptape.rules import Ruleset, Rule
from griptape.structures import Agent
from griptape.tools import KnowledgeBaseClient


@define
class Chat:
    agent: Agent = field(
        default=Factory(
            lambda self: self.create_agent(ConversationMemory(), []),
            takes_self=True
        )
    )
    query_engine: VectorQueryEngine = field(
        default=Factory(lambda: VectorQueryEngine()),
        kw_only=True
    )

    def send_message(self, message: str) -> str:
        return self.agent.run(message).output.value

    def upload_pdf(self, file: TemporaryFile) -> str:
        namespace = os.path.basename(file.name)

        self.query_engine.vector_store_driver.upsert_text_artifacts(
            {
                namespace: PdfLoader().load(file.name)
            }
        )

        kb_client = KnowledgeBaseClient(
            description=f"Contains information about a PDF with name {namespace}.",
            query_engine=self.query_engine,
            namespace=namespace
        )

        self.agent = self.create_agent(
            self.agent.memory,
            [kb_client]
        )

        return file.name

    def create_agent(self, memory: ConversationMemory, tools: list[BaseTool]) -> Agent:
        return Agent(
            prompt_driver=OpenAiPromptDriver(model="gpt-4"),
            memory=memory,
            tools=tools,
            rulesets=[
                Ruleset(
                    name="PDF Chat Assistant",
                    rules=[
                        Rule("Only chat about things in the PDF file that you have access to"),
                        Rule("If you don't have access to a PDF file say that you don't have access to the PDF file")
                    ]
                )
            ]
        )
