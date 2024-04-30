# SR-LLM
Exploring Spatial Reasoning Abilities of LLMs using Reinforcement Learning

```mermaid
graph TB
    A[Evaluation Module] -- AgentAction, Observation, Stats --> B[Environment]
    B -- Observation --> C[LLM]
    C -- Action --> B
    C -- Observation --> D[System Prompt]
    D -- Example Reasoning --> E[Chain of Thought (Interaction per step)]
    A -- Evaluation --> C
```
