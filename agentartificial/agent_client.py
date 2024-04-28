from __future__ import annotations
import os
import requests
from requests import Request
from openai import OpenAI, Client
from openai.resources import Chat, Completions
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Union

load_dotenv()


class Agent:
    isInferenceUp: bool
    model: str
    api_key: str
    base_url: str
    http_client: Union[Request, Client]


class AgentArtificial(Client, Agent):
    def __init__(self):
        super().__init__()
        self.isInferenceUp = self.spot_check()
        self.api_key = self.choose_api_key()
        self.base_url = self.choose_baseURL()
        self.model = self.choose_model()
        self.http_client = self.get_http_client() or requests

    def get_http_client(self):
        return Client(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=30,
            max_retries=5,
            default_headers={"Authorization": f"Bearer {self.api_key}"},
            default_query={"model": self.model},
            organization=None,
            http_client=self._client
        )
        
    def choose_baseURL(self) -> str:
        print(f"Inferece status: {self.isInferenceUp}")
        if self.isInferenceUp:
            print(f"Selected URL: {os.getenv('AGENTARTIFICIAL_URL')}")
            return str(f"{os.getenv('AGENTARTIFICIAL_URL')}")
        else: 
            print(f"Selected URL: {os.getenv('OPENAI_BASE_URL')}")
            return str(os.getenv('OPENAI_BASE_URL'))
        
    def choose_api_key(self):
        if self.isInferenceUp:
            print(f"Selected API key: {os.getenv('AGENTARTIFICIAL_API_KEY')}")
            return str(os.getenv('AGENTARTIFICIAL_API_KEY'))
        print(f"Selected API key: {os.getenv('OPENAI_API_KEY')}")
        return str(os.getenv('OPENAI_API_KEY'))

    def choose_model(self, model="ollama/mixtral"):
        if self.isInferenceUp:
            print(f"Selected model: {model}")
            return model or "ollama/mixtral"
        print(f"Selected model: {model}")
        return model or "gpt-3.5-turbo"

    def spot_check(self):
        result = requests.get(
            url=f"{os.getenv("AGENTARTIFICIAL_URL")}",
            headers={
                "Authorization": f"Bearer {os.getenv('AGENTARTIFICIAL_API_KEY')}"
            },
            timeout=30
        )
        print(result)

        if result.status_code == 200:
            return True
        return False

    def pull_model(self, model_name):
        url = f"{self.base_url}/model/pull"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "model_name": model_name
        }
        return requests.post(url=url, json=body, headers=headers, timeout=30)        


class Completion(Completions, AgentArtificial):
    body: str
    
    def __init__(self):
        super().__init__(self)
    
    def create(self, model="mixtral", messages=None):
        
        body = {
          "model": model,
          "messages": messages
        }

        url = f"{self.base_url}/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}text",
            "Content-Type": "application/json"
        }
        response = requests.post(
            url=url, 
            json=body, 
            headers=headers, 
            timeout=30
            )
        return response.json()["choices"][0]["message"]["content"]


class Chats(Chat):
    def __init__(self):
        super().__init__(OpenAI())
        self.completion = Completion()


if __name__ == "__main__":
    agent = AgentArtificial()