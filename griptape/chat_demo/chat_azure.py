from azure.identity import ClientSecretCredential
import os
from attr import define
from typing import Any
from griptape.drivers import OpenAiChatPromptDriver
from griptape.rules import Ruleset, Rule
from griptape.structures import Agent
from griptape.tools import VectorStoreClient
from griptape.config import OpenAiStructureConfig
from griptape.artifacts import ListArtifact
from griptape.rules import Rule, Ruleset
from griptape.structures import Agent
from griptape.drivers import BaseVectorStoreDriver, LocalConversationMemoryDriver, GriptapeCloudKnowledgeBaseVectorStoreDriver
from griptape.config import AzureOpenAiStructureConfig
from griptape.tools import VectorStoreClient
from griptape.memory.structure import ConversationMemory
    
@define
class Chat_Azure:

    def __init__(self, client_id:str, client_secret:str, tenant_id:str, azure_endpoint:str, knowledge_base_id:str, gt_cloud_api_key:str, gt_cloud_base_url:str):
        config = OpenAiStructureConfig()
        config.prompt_driver = OpenAiChatPromptDriver(
            model="gpt-4o",
        )

        azure_credential = ClientSecretCredential(
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id,
        )

        self.azure_structure_config = AzureOpenAiStructureConfig(
            azure_ad_token_provider=lambda: azure_credential.get_token(
                "https://cognitiveservices.azure.com/.default"
            ).token,
            azure_endpoint=azure_endpoint,
        )
        # Creates a driver to interact with the cloud knowledge base 
        self.vector_store_driver = GriptapeCloudKnowledgeBaseVectorStoreDriver(
            base_url=gt_cloud_base_url,
            api_key=gt_cloud_api_key,
            knowledge_base_id=knowledge_base_id,
        )
    
    vector_store_driver = GriptapeCloudKnowledgeBaseVectorStoreDriver

    azure_structure_config = AzureOpenAiStructureConfig

    # Creates a ruleset for the structure 
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

    # Output of the query, returns in the form of a ListArtifacts
    def process_query_output_fn(entries: list[BaseVectorStoreDriver.Entry]):
        artifacts = []
        for entry in entries:
            artifact = entry.to_artifact()
            artifacts.append(artifact)
        return ListArtifact(artifacts)

    # Creates a VectorStore
    vector_store_tool = VectorStoreClient(
        description="Contains a Product Catalog",
        query_params={},
        vector_store_driver=vector_store_driver,
        process_query_output_fn=process_query_output_fn,
    )

    # Structure built with tools, rulesets, and Azure configuration
    agent: Agent = Agent(
        rulesets=[personality_ruleset, vector_store_client_ruleset],
        tools=[vector_store_tool],
        config=azure_structure_config,
        conversation_memory=ConversationMemory(
            driver=LocalConversationMemoryDriver(
                file_path="conversation_memory.json"
            )),
    )

    # Recieves messages and history from the agent
    def send_message(self, message: str, history) -> Any:
        self.agent.input = (message,)
        return self.agent.run().value

