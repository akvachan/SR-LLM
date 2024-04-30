# SR-LLM
Exploring Spatial Reasoning Abilities of LLMs using Reinforcement Learning

```mermaid
flowchart TD
    A[Environment] --> |Observation| B[LLM]
    D[System Prompt] --> B
    B --> |Action| A
    A --> |Agent Action, Observation, Stats| C[Evaluation Module]
    B --> |Language| C
```
