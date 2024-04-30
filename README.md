# SR-LLM
Exploring Spatial Reasoning Abilities of LLMs using Reinforcement Learning

```mermaid
flowchart TD
    A[Environment] --> |Observation| B[LLM]
    B --> |Action| A
    A --> |AgentAction, Observation, Stats| C[EvaluationModul]
    B --> |Language| C
```
