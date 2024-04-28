from agentartificial.agent_client import AgentArtificial
import requests
from openai import OpenAI
from loguru import logger


agent = AgentArtificial()
openai = OpenAI()


def test_spot_check():
    logger.info(agent.spot_check())



def test_choose_model():
    logger.info(agent.choose_model())


def test_choose_api_key():
    logger.info(agent.choose_api_key())


def test_pull_base_url():
    url = agent.choose_baseURL()
    logger.info(url)

    url = "https://mixtral-agentartificial.ngrok.app/api/pull"
    body = {
        "messages":[],
        "model": "mixtral"
    }
    response = requests.post(url=url, json=body)
    logger.info(response.text)

#test_pull_base_url()

def test_new_model():
    url = f"{agent.base_url}model/new"
    logger.info(url)
    headers = {
        "Authorization": f"Bearer {agent.api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model_name": "mixtral",
        "litellm_params": {
            "provider": "ollama",
            "model": "ollama/mixtral",
            "api_base": "https://mixtral-agentartificial.ngrok.app"
            },
        "model_info": {
            "id": "mixtral",
            "mode": "completion",
            "input_cost_per_token": 0.0006,
            "output_cost_per_token": 0.0012,
            "max_tokens": 16000,
            "base_model": "ollama/mixtral",
            "additionalProp1": {}
        }
    }
    response = requests.post(url=url, json=body, headers=headers)
    logger.info(response.json())


def test_models():
    url = f"{agent.base_url}/v1/models"
    logger.info(url)
    headers = {
        "Authorization": f"Bearer {agent.api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(url=url, headers=headers)
    logger.info(response.json())


def test_chat_completion():
    body={
      "model": "mixtral",
      "messages":[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
      ]
    }

    url = f"{agent.base_url}/v1/chat/completions"
    logger.info(url)
    headers = {
        "Authorization": f"Bearer {agent.api_key}text",
        "Content-Type": "application/json"
    }
    response = requests.post(url=url, json=body, headers=headers)
    logger.info(response.json()["choices"][0]["message"]["content"])


def test_client():
    agent = AgentArtificial()
    openai = OpenAI()
    openai.api_key = agent.api_key
    openai.base_url = agent.base_url
    
    logger.info(agent.spot_check())
    logger.info(agent.choose_api_key())
    logger.info(agent.choose_model())

    response = agent.chat.completions.create(
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "what year did alpha go become the world champion at checkers?"}],
        model=agent.model        
    )

    logger.info(response.model_dump()["choices"][0]["message"]["content"])

#test_spot_check()
#test_choose_model()
#test_choose_api_key()
#test_models()
#test_new_model()
#test_chat_completion()
test_client()