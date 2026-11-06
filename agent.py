import os
import sqlite3
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver

from tools import tools

# Cargar variables del entorno (.env)
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ No se encontró OPENAI_API_KEY en el archivo .env")

model_name = os.getenv("DEFAULT_MODEL", "llama-3.3-70b-versatile")
base_url = os.getenv("OPENAI_BASE_URL", "https://api.groq.com/openai/v1")

# Instanciar LLM con herramientas vinculadas
llm = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url,
    temperature=0.0
).bind_tools(tools)


# 1. Nodo del Agente (invocación síncrona)
def call_model(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# 2. Construcción del Grafo ReAct
workflow = StateGraph(MessagesState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", tools_condition)
workflow.add_edge("tools", "agent")

# 3. Configurar Persistencia con SQLite
conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)

# Compilar el grafo integrando el checkpointer
app = workflow.compile(checkpointer=memory)