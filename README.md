# TP 5: Agente de Razonamiento Cíclico con Memoria Persistente en LangGraph

Este repositorio contiene la implementación de un **Agente Autónomo de Razonamiento Cíclico (ReAct)** construido con **LangGraph**, capaz de ejecutar herramientas personalizadas, gestionar el flujo de ejecución mediante aristas condicionales y mantener la memoria conversacional multiturno a través de persistencia en **SQLite**.

---

## 🛠️ Arquitectura del Sistema

### 1. Herramientas Personalizadas (`tools.py`)
- Definición de funciones decoradas con `@tool` de LangChain.
- Validación estructurada de entrada mediante **Pydantic** (`ConsultarPedidoInput`).
- Herramienta implementada: `consultar_pedidos`, que consulta una base de datos simulada de clientes y compras.

### 2. Grafo de Estado y Flujo ReAct (`agent.py`)
- Construcción de un `StateGraph` basado en `MessagesState`.
- Nodos configurados: `agent` (LLM) y `tools` (`ToolNode`).
- Aristas condicionales mediante `tools_condition` para controlar los ciclos de decisión.
- Persistencia del estado con **`SqliteSaver`** en `checkpoints.sqlite`.

### 3. Ejecución Conversacional y Memoria (`main.py`)
- Prueba en 2 turnos manteniendo el contexto gracias al uso de `thread_id`.
- Configuración de límites de recursión (`recursion_limit: 10`).
- Generación y exportación automática de la traza de ejecución en `trace_example.json`.

---

## 📋 Requisitos e Instalación

### 1. Clonar e Instalar Dependencias
```cmd
git clone https://github.com/xDroikx/tp5-langgraph-agent.git
cd tp5-langgraph-agent
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt