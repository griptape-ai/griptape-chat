from azure.identity import ClientSecretCredential
import os
from attr import define
from typing import Any
from dotenv import load_dotenv


from griptape.drivers import OpenAiChatPromptDriver
from griptape.rules import Ruleset, Rule
from griptape.structures import Agent
from griptape.tools import VectorStoreClient
from griptape.config import OpenAiStructureConfig
from griptape.artifacts import ListArtifact
from griptape.rules import Rule, Ruleset
from griptape.structures import Agent
from griptape.drivers import BaseVectorStoreDriver, GriptapeCloudKnowledgeBaseVectorStoreDriver
from griptape.config import AzureOpenAiStructureConfig
from griptape.tools import VectorStoreClient


load_dotenv()
#not sure if this config stuff is neccessary 
config = OpenAiStructureConfig()
config.prompt_driver = OpenAiChatPromptDriver(
    model="gpt-4o",
)


azure_credential = ClientSecretCredential(
    client_id=os.environ["AZURE_CLIENT_ID"],
    client_secret=os.environ["AZURE_CLIENT_SECRET"],
    tenant_id=os.environ["AZURE_TENANT_ID"],
)

azure_structure_config = AzureOpenAiStructureConfig(
    azure_ad_token_provider=lambda: azure_credential.get_token(
        "https://cognitiveservices.azure.com/.default"
    ).token,
    azure_endpoint=os.environ["AZURE_OPENAI_DEFAULT_ENDPOINT"],
)

    
@define
class Chat:
    personality_ruleset = Ruleset(
        name="Personality",
        rules=[
            Rule(f"You are a chat bot and your name is 'EDBob'."),
            Rule(
                "You speak in a casual but professional manner."
            ),
            Rule(
                "Don't identify as an AI. You are able to have an opinion and have feelings."
            ),
            Rule("You are friendly, happy, and generally positive."),
        ],
    )
    vector_store_client_ruleset = Ruleset(
        name="Vector Store Client",
        rules=[
            Rule("Always search the Vector Store Client."),
            Rule("Only use the output of the Vector Store Client tool if it is relevant."),
            Rule("Search the Vector Store Client tool with keywords, not complete sentences or questions."),
            Rule("Do not add terms to the search like product, details, or price"),
        ],
    )

    knowledge_base_id = os.environ.get("KNOWLEDGE_BASE_ID")
    gt_cloud_api_key = os.environ.get("GT_CLOUD_API_KEY")
    gt_cloud_base_url = os.environ.get("GT_CLOUD_BASE_URL", "https://cloud.griptape.ai")

    vector_store_driver = GriptapeCloudKnowledgeBaseVectorStoreDriver(
        base_url=gt_cloud_base_url,
        api_key=gt_cloud_api_key,
        knowledge_base_id=knowledge_base_id,
    )

    def process_query_output_fn(entries: list[BaseVectorStoreDriver.Entry]):
        artifacts = []
        for entry in entries:
            artifact = entry.to_artifact()
            artifacts.append(artifact)
        return ListArtifact(artifacts)

    vector_store_tool = VectorStoreClient(
        description="Contains a Product Catalog",
        query_params={},
        vector_store_driver=vector_store_driver,
        process_query_output_fn=process_query_output_fn,
    )

    agent: Agent = Agent(
        rulesets=[personality_ruleset, vector_store_client_ruleset],
        tools=[vector_store_tool],
        config=azure_structure_config,
    )

    def send_message(self, message: str, history) -> Any:
        response = self.agent.run(message).output.value
        return response
