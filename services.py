from models import  Produto, Pedido, ItemPedido
from sqlalchemy.orm import Session
from schemas import ProdutoCreate, PedidoCreate, ItemPedidoCreate
from datetime import datetime




def create_produto(db: Session, data: ProdutoCreate):
    produto = Produto(**data.model_dump())
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


def get_produtos(db: Session):
    return db.query(Produto).all()


def get_produto(db: Session, produto_id: int):
    return db.query(Produto).filter(Produto.id == produto_id).first()


def update_produto(db: Session, data: ProdutoCreate, produto_id: int):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if produto:
        for key, value in data.model_dump().items():
            setattr(produto, key, value)
        db.commit()
        db.refresh(produto)
    return produto


def delete_produto(db: Session, produto_id: int):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if produto:
        db.delete(produto)
        db.commit()
    return produto

## Pedidos
def create_pedido(db: Session, data: PedidoCreate):
    itens = []
    valor_total_pedido = 0.0

    for item in data.itens:
        produto = db.query(Produto).filter(Produto.id == item.produto_id).first()
        if not produto or produto.quantidade < item.quantidade:
            raise ValueError(f"Produto inválido ou estoque insuficiente: ID {item.produto_id}")

        preco_unitario = produto.preco
        valor_total_item = preco_unitario * item.quantidade
        valor_total_pedido += valor_total_item

        item_pedido = ItemPedido(
            produto_id=produto.id,
            nome_produto=produto.nome,
            quantidade=item.quantidade,
            preco_unitario=preco_unitario,
            valor_total_item=valor_total_item
        )
        itens.append(item_pedido)

        # Atualiza estoque
        produto.quantidade -= item.quantidade

    pedido = Pedido(
        cliente=data.cliente,
        valor_total=valor_total_pedido,
        data_pedido=datetime.utcnow(),
        itens=itens
    )

    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido


def get_pedidos(db: Session):
    return db.query(Pedido).all()


def get_pedido(db: Session, pedido_id: int):
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()




def update_pedido(db: Session, pedido_id: int, data: PedidoCreate):
    # 1. Busca o pedido existente
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        return None

    # 2. Devolve os itens antigos ao estoque e remove do banco
    for item in pedido.itens:
        produto = db.query(Produto).filter(Produto.id == item.produto_id).first()
        if produto:
            produto.quantidade += item.quantidade  # devolve ao estoque
        db.delete(item)  # remove item do banco

    db.flush()  # garante que os itens antigos foram apagados antes de adicionar os novos

    # 3. Recria os itens atualizados
    novos_itens = []
    novo_valor_total = 0.0

    for item in data.itens:
        produto = db.query(Produto).filter(Produto.id == item.produto_id).first()
        if not produto or produto.quantidade < item.quantidade:
            raise ValueError(f"Produto inválido ou estoque insuficiente: ID {item.produto_id}")

        preco_unitario = produto.preco
        valor_total_item = preco_unitario * item.quantidade
        novo_valor_total += valor_total_item

        produto.quantidade -= item.quantidade  # retira do estoque

        novo_item = ItemPedido(
            pedido_id=pedido.id,
            produto_id=produto.id,
            nome_produto=produto.nome,
            quantidade=item.quantidade,
            preco_unitario=preco_unitario,
            valor_total_item=valor_total_item
        )
        novos_itens.append(novo_item)

    # 4. Adiciona os novos itens ao banco
    db.add_all(novos_itens)

    # 5. Atualiza os dados do pedido
    pedido.cliente = data.cliente
    pedido.valor_total = novo_valor_total
    pedido.data_pedido = datetime.utcnow()

    db.commit()
    db.refresh(pedido)

    return pedido



def delete_pedido(db: Session, pedido_id: int):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if pedido:
        # Devolve os produtos ao estoque
        for item in pedido.itens:
            produto = db.query(Produto).filter(Produto.id == item.produto_id).first()
            if produto:
                produto.quantidade += item.quantidade
        db.delete(pedido)
        db.commit()
    return pedido