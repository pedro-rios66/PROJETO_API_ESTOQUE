# 📦 API RESTful de Gestão de Estoque

Esta é uma API desenvolvida com **FastAPI** e **SQLAlchemy**, com banco de dados **PostgreSQL**, para controle de produtos e pedidos. É voltada para pequenas e médias empresas que desejam gerir seu estoque com simplicidade, robustez e segurança.

---

## 🚀 Visão Geral do Projeto

A proposta é fornecer um sistema backend de **cadastro, atualização, exclusão e consulta de produtos e pedidos**, com validação de estoque, cálculo automático do valor total de pedidos e endpoints RESTful. Toda a lógica está implementada de forma modular e profissional.

---

## 🔧 Funcionalidades

### 📁 Produtos

- `GET /produtos/` – Lista todos os produtos
- `GET /produtos/{id}` – Retorna um produto específico
- `POST /produtos/` – Cria um novo produto
- `PUT /produtos/{id}` – Atualiza um produto
- `DELETE /produtos/{id}` – Deleta um produto

### 🧾 Pedidos

- `GET /pedidos/` – Lista todos os pedidos
- `GET /pedidos/{id}` – Retorna um pedido específico
- `POST /pedidos/` – Cria um novo pedido com múltiplos itens
- `PUT /pedidos/{id}` – Atualiza um pedido (devolve e revalida estoque)
- `DELETE /pedidos/{id}` – Remove um pedido e restaura o estoque

---

## 🧠 Arquitetura

A aplicação segue uma estrutura limpa e modular baseada em camadas:

```
estoque_api/
├── app/
│   ├── main.py              # Entrypoint da API com endpoints FastAPI
│   ├── database.py          # Conexão com banco (PostgreSQL via SQLAlchemy)
│   ├── models.py            # Modelos ORM: Produto, Pedido, ItemPedido
│   ├── schemas.py           # Esquemas Pydantic para validação e resposta
│   ├── services.py          # Camada de lógica e regras de negócio
└── README.md
```

---

## 📦 Instalação e Execução

### ✅ Pré-requisitos

- Python 3.10+
- PostgreSQL
- Git

### 🔧 Passo a passo

1. Clone o repositório:

```bash
git clone https://github.com/seuusuario/estoque_api.git
cd estoque_api
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure a variável de ambiente `DATABASE_URL` no formato:

```bash
postgresql://usuario:senha@localhost:5432/nome_do_banco
```

4. Execute a aplicação:

```bash
uvicorn app.main:app --reload
```

5. Acesse a documentação interativa via Swagger:

```
http://127.0.0.1:8000/docs
```

---



## ☁️ Deploy em Produção

Recomendado o uso de:

- Docker e Docker Compose
- Gunicorn + Uvicorn workers
- PostgreSQL hospedado (ex: Supabase, Render, NeonDB)
- Monitoramento com Prometheus + Grafana
- CI/CD via GitHub Actions

---

## 🔐 Regras de Negócio Importantes

- Não é possível realizar pedido com estoque insuficiente
- Ao atualizar pedidos, o estoque antigo é restaurado antes da nova reserva
- O valor total é calculado automaticamente com base nos preços e quantidades
- A exclusão de pedidos também restaura o estoque dos produtos envolvidos

---

## ✨ Futuras Melhorias

- Autenticação com JWT
- Dashboard administrativo (com Streamlit ou React)
- Geração de relatórios em PDF
- Integração com sistemas de pagamento

---

## 👨‍💻 Autor

Feito com 💻 e ⚙️ por [Pedro Rios]