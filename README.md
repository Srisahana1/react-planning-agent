\# ReAct Planning Agent



I built this project to understand what actually happens when an AI agent does more than generate a single response.



Instead of sending a prompt to an LLM and immediately returning the answer, this agent works through a small decision loop. It looks at the task, decides what action makes sense, uses the appropriate tool, observes the result, and determines when it has enough information to stop.



While building it, one interesting problem I ran into was that the model kept selecting the same tool even after it already had the answer. I ended up adding deterministic termination logic so a successful observation stops unnecessary repeated tool calls.



That small issue helped me understand an important part of agent engineering: \*\*a good agent needs control logic around the LLM, not just a better prompt.\*\*



\## How it works



The workflow is intentionally simple:



```text

User Task

&#x20;   |

&#x20;   v

ReAct Agent

&#x20;   |

&#x20;   v

Decide Next Action

&#x20;   |

&#x20;   +-----------------------+

&#x20;   |                       |

&#x20;   v                       v

Calculator            Knowledge Search

&#x20;   |                       |

&#x20;   +-----------+-----------+

&#x20;               |

&#x20;               v

&#x20;          Observation

&#x20;               |

&#x20;               v

&#x20;       Enough information?

&#x20;          /          \\

&#x20;        No            Yes

&#x20;        |              |

&#x20;        v              v

&#x20;      Repeat       Final Answer

```



The agent currently has two tools:



\- \*\*Calculator\*\* — safely evaluates basic mathematical expressions.

\- \*\*Knowledge Search\*\* — searches a small local knowledge base containing information about RAG, ReAct, and LangGraph.



After a tool returns a useful observation, the workflow recognizes that the task can be completed and returns the final answer.



\## Example



Input:



```text

What is ReAct?

```



The agent first chooses:



```text

action = search\_knowledge

action\_input = ReAct

```



The tool returns:



```text

ReAct is an agent pattern that combines reasoning and actions

in an iterative workflow.

```



The workflow then recognizes that it has enough information and finishes instead of calling the same tool repeatedly.



Final state:



```text

action = finish

iteration = 2

```



The same workflow can handle calculations.



Input:



```text

Calculate 25 \* 8

```



Result:



```text

200

```



\## Why I added an iteration limit



Agent loops need a stopping condition.



Without one, a model can repeatedly choose the same action or continue reasoning when it should already be finished.



This project limits execution to a maximum of three iterations and also includes deterministic termination after a successful tool observation.



That gives the workflow two protections:



```text

Successful result → Finish



or



Maximum iterations reached → Stop

```



\## Tech Stack



\- Python 3.13

\- LangGraph

\- LangChain

\- Ollama

\- Llama 3.2

\- Pydantic

\- FastAPI

\- Uvicorn

\- Pytest



\## Project Structure



```text

react-planning-agent/

│

├── src/

│   ├── \_\_init\_\_.py

│   ├── agent.py

│   ├── schemas.py

│   ├── tools.py

│   └── workflow.py

│

├── tests/

│   └── test\_workflow.py

│

├── main.py

├── pytest.ini

├── requirements.txt

├── .gitignore

└── README.md

```



\## Running the Project



Create and activate a virtual environment:



```bash

python -m venv .venv

```



Install the dependencies:



```bash

pip install -r requirements.txt

```



Make sure Ollama is running and Llama 3.2 is available:



```bash

ollama run llama3.2

```



Start the API:



```bash

python -m uvicorn main:app --reload

```



The API will run locally at:



```text

http://127.0.0.1:8000

```



FastAPI documentation is available at:



```text

http://127.0.0.1:8000/docs

```



\## API



\### Health Check



```http

GET /health

```



Response:



```json

{

&#x20; "status": "healthy"

}

```



\### Run the Agent



```http

POST /run

```



Example request:



```json

{

&#x20; "task": "What is ReAct?"

}

```



The response contains the agent state, including the observation, selected action, reflection, iteration count, and final answer.



\## Testing



The tests intentionally mock the LLM decision step so the workflow logic can be tested without depending on model behavior.



Run:



```bash

pytest -v

```



Current test suite covers:



\- Knowledge-tool execution and termination

\- Calculator execution and termination



Current result:



```text

2 passed

```



\## What I Learned



The biggest takeaway from this project wasn't simply how to call an LLM from LangGraph.



It was understanding the boundary between \*\*model reasoning and application control\*\*.



The LLM can decide what it wants to do next, but the surrounding application still needs to enforce things like:



\- iteration limits

\- valid tool execution

\- termination conditions

\- structured state

\- predictable failure behavior



That makes an agent much easier to reason about and test.



\## Current Limitations



This is intentionally a small learning project.



The knowledge tool currently uses a local dictionary rather than live search or retrieval from external documents. The agent also has only two tools and a simple success condition.



Those limitations keep the architecture easy to understand while leaving room for more advanced versions.



\## Ideas for Future Improvements



Some features I would like to experiment with next:



\- More external tools

\- Persistent memory

\- Human approval before sensitive actions

\- Better reflection strategies

\- Agent execution tracing

\- Tool retry and error recovery

\- LLM evaluation

\- Cost and latency tracking



\## Why I Built This



After working with RAG, structured LLM outputs, and multi-agent workflows, I wanted to understand the smaller control loop underneath many agent systems.



This project gave me a practical way to explore that:



\*\*reason → act → observe → decide whether to continue\*\*



Sometimes the most useful part of building an AI project isn't making it bigger. It's understanding exactly why each part of the system exists.

