import json
from agent import app
from langchain_core.messages import HumanMessage


def main():
    print("============================================================")
    print("🤖 PRE-ENTREGA 5: AGENTE CÍCLICO REACT CON LANGGRAPH Y MEMORIA")
    print("============================================================\n")

    thread_config = {"configurable": {"thread_id": "sesion_cliente_102"}}

    # ----------------------------------------------------
    # TURNO 1: Consulta que requiere invocar la herramienta
    # ----------------------------------------------------
    pregunta_1 = "¿Cuántos pedidos hizo el cliente 102 y cuál fue el total gastado?"
    print(f"👤 Usuario (Turno 1): {pregunta_1}\n")

    input_1 = {"messages": [HumanMessage(content=pregunta_1)]}

    res_1 = app.invoke(
        input_1, 
        config={**thread_config, "recursion_limit": 10}
    )

    ultimo_msg_1 = res_1["messages"][-1]
    print(f"🤖 Agente: {ultimo_msg_1.content}\n")
    print("-" * 60)

    # ----------------------------------------------------
    # TURNO 2: Consulta contextual (requiere memoria del Turno 1)
    # ----------------------------------------------------
    pregunta_2 = "¿Y cuál fue el último producto que compró?"
    print(f"👤 Usuario (Turno 2 - Memoria): {pregunta_2}\n")

    input_2 = {"messages": [HumanMessage(content=pregunta_2)]}

    res_2 = app.invoke(
        input_2, 
        config={**thread_config, "recursion_limit": 10}
    )

    ultimo_msg_2 = res_2["messages"][-1]
    print(f"🤖 Agente: {ultimo_msg_2.content}\n")

    # ----------------------------------------------------
    # EXPORTAR TRAZA DE EJECUCIÓN (trace_example.json)
    # ----------------------------------------------------
    traza = []
    for msg in res_2["messages"]:
        item = {
            "tipo": msg.type,
            "contenido": msg.content
        }
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            item["tool_calls"] = msg.tool_calls
        traza.append(item)

    with open("trace_example.json", "w", encoding="utf-8") as f:
        json.dump(traza, f, indent=2, ensure_ascii=False)

    print("✅ Traza de ejecución ReAct exportada exitosamente en 'trace_example.json'.")


if __name__ == "__main__":
    main()