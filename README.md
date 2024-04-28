# Agent Artificial OpenAI Client

This library enables OpenAI standard client to interface with the Agent Artificial API endpoints for inference. 

## Instillation 

`pip install agentartificial`

## Usage

Import `AgentArtificial` and instantiate a new instance and pass the `OpenAI` class into the agent client. It will automatically configure the client to hit Agent Artificial endpoints. 

Example
```
from openai import OpenAI
from agentartifiical import AgentArtificial, InferenceModels

agent = AgentArtificial(OpenAI())


result = agent.chat.completion.create(
    model=InferenceModels.mixtral
)

```
