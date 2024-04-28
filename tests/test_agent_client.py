import unittest
from agentartificial.agent_client import AgentArtificial
from loguru import logger

def fixture():
    agent = AgentArtificial()
    agent.choose_api_key()
    agent.choose_baseURL()
    agent.choose_model()

    return agent


class TestAgentClient(unittest.TestCase):
    def test_choose_api_key(self):
        agent = fixture()
        logger.info(agent.choose_api_key())

    def test_choose_baseURL(self):
        agent = fixture()
        logger.info(agent.choose_baseURL())

    def test_choose_model(self):
        agent = fixture()
        logger.info(agent.choose_model())


