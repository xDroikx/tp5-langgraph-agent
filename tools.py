from langchain_core.tools import tool
from pydantic import BaseModel, Field

# 1. Esquema de validación con Pydantic
class ConsultarPedidoInput(BaseModel):
    cliente_id: int = Field(..., description="ID numérico del cliente a consultar (ej. 101, 102, 103).")


# 2. Base de datos simulada de pedidos
BASE_DATOS_PEDIDOS = {
    101: {"pedidos": 1, "total": 3500.0, "ultimo_producto": "Teclado Mecánico"},
    102: {"pedidos": 3, "total": 14500.0, "ultimo_producto": "Monitor 4K"},
    103: {"pedidos": 2, "total": 8900.0, "ultimo_producto": "Auriculares Bluetooth"},
}


# 3. Función decorada como @tool
@tool(args_schema=ConsultarPedidoInput)
def consultar_pedidos(cliente_id: int) -> str:
    """Consulta la base de datos de pedidos para obtener la cantidad de pedidos, el gasto total y el último producto comprado por un cliente según su cliente_id."""
    info = BASE_DATOS_PEDIDOS.get(cliente_id)
    if info:
        return (
            f"Cliente {cliente_id}: {info['pedidos']} pedidos registrados, "
            f"total gastado: ${info['total']:.2f}, "
            f"último producto comprado: '{info['ultimo_producto']}'."
        )
    return f"No se encontraron registros de pedidos para el cliente con ID {cliente_id}."


# Lista de herramientas exportables para el agente
tools = [consultar_pedidos]