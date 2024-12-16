# AI Mock Coding Interview Agent

## Try this app here
www.leetscode.up.railway.app

## About this project

### Application
![Application Screenshot](screenshots/Screenshot%202024-12-13%20at%2010.27.55%20AM.png)
![Application Screenshot](screenshots/Screenshot%202024-12-13%20at%2010.20.58%20AM.png)

### Stack
Front-end: React
Back-end: FastAPI
LLM orchestration: LangChain
Agentic flow engineering: LangGraph

### Cognitive architecture

#### Overall
![Main System Architecture](backend/agents/graph_diagrams/main_graph.png)

#### Simplified High-level view
![High level](backend/agents/graph_diagrams/main_graph_high_level.png)


## How to run

You can run this project both backend and frontend with a single docker command.
```bash
docker compose up --build -d
```
After the services are running, you can access the app at `http://localhost:3001`
Don't forget to fill .env file in /backend and /frontend!