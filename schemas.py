from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime



# --------------------- PRODUTOS ---------------------

class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    quantidade: int

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


# --------------------- ITENS DE PEDIDO ---------------------

class ItemPedidoBase(BaseModel):
    produto_id: int
    nome_produto: str
    quantidade: int
    preco_unitario: float
    valor_total_item: float

class ItemPedidoCreate(ItemPedidoBase):
    pass

class ItemPedidoResponse(ItemPedidoBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


# --------------------- PEDIDOS ---------------------

class PedidoBase(BaseModel):
    cliente: str
    valor_total: float  # calculado no backend
    data_pedido: Optional[datetime] = None

class PedidoCreate(PedidoBase):
    itens: List[ItemPedidoCreate]

class PedidoResponse(PedidoBase):
    id: int
    data_pedido: datetime
    itens: List[ItemPedidoResponse]

    class Config:
        orm_mode = True
        from_attributes = True
