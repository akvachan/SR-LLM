# SR-LLM
Exploring Spatial Reasoning Abilities of LLMs using Reinforcement Learning

```mermaid
flowchart TD
    A[Environment] --> |Observation| B[LLM]
    B --> |Action| A
    A --> |Agent Action, Observation, Stats| C[Evaluation Module]
    B --> |Language| C
    D[System Prompt] --> B
```
