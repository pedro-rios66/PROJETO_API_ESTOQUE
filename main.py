from fastapi import FastAPI, Depends, HTTPException
import services, models, schemas
from db import get_db, engine
from sqlalchemy.orm import Session

app = FastAPI()



# ====================== PRODUTOS ======================

@app.get("/produtos/", response_model=list[schemas.ProdutoResponse])
def get_all_produtos(db: Session = Depends(get_db)):
    return services.get_produtos(db)


@app.get("/produtos/{id}", response_model=schemas.ProdutoResponse)
def get_produto_by_id(id: int, db: Session = Depends(get_db)):
    produto = services.get_produto(db, id)
    if produto:
        return produto
    raise HTTPException(status_code=404, detail="Produto não encontrado")


@app.post("/produtos/", response_model=schemas.ProdutoResponse)
def create_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return services.create_produto(db, produto)


@app.put("/produtos/{id}", response_model=schemas.ProdutoResponse)
def update_produto(id: int, produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    produto_atualizado = services.update_produto(db, produto, id)
    if not produto_atualizado:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto_atualizado


@app.delete("/produtos/{id}", response_model=schemas.ProdutoResponse)
def delete_produto(id: int, db: Session = Depends(get_db)):
    produto = services.delete_produto(db, id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


# ====================== PEDIDOS ======================

@app.get("/pedidos/", response_model=list[schemas.PedidoResponse])
def get_all_pedidos(db: Session = Depends(get_db)):
    return services.get_pedidos(db)


@app.get("/pedidos/{id}", response_model=schemas.PedidoResponse)
def get_pedido_by_id(id: int, db: Session = Depends(get_db)):
    pedido = services.get_pedido(db, id)
    if pedido:
        return pedido
    raise HTTPException(status_code=404, detail="Pedido não encontrado")


@app.post("/pedidos/", response_model=schemas.PedidoResponse)
def create_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    try:
        return services.create_pedido(db, pedido)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/pedidos/{id}", response_model=schemas.PedidoResponse)
def update_pedido(id: int, pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    try:
        pedido_atualizado = services.update_pedido(db, id, pedido)
        if not pedido_atualizado:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        return pedido_atualizado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/pedidos/{id}", response_model=schemas.PedidoResponse)
def delete_pedido(id: int, db: Session = Depends(get_db)):
    pedido = services.delete_pedido(db, id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido
