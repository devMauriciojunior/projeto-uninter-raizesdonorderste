from infrastructure.database import SessionLocal
from infrastructure.models import UnidadeModel, ProdutoModel, EstoqueModel

def popular_banco():
    db = SessionLocal()
    try:
        unidade_existe = db.query(UnidadeModel).first()
        if unidade_existe:
            print("⚠️ O banco já possui dados")
            return

        # Cria Unidades
        unidade_matriz = UnidadeModel(nome="Raízes do Nordeste - Matriz", endereco="Rua São Benedito, 418 - Santo Amaro - SP")
        db.add(unidade_matriz)
        db.commit()
        db.refresh(unidade_matriz)
        print(f"✅ Unidade criada: {unidade_matriz.nome} (ID: {unidade_matriz.id})")

        # Cria Produtos do Cardápio
        produtos = [
            ProdutoModel(nome="Tapioca de Carne de Sol com Queijo", preco=18.90, ativo=True),
            ProdutoModel(nome="Cuscuz Completo", preco=15.50, ativo=True),
            ProdutoModel(nome="Suco de Caju (500ml)", preco=8.00, ativo=True)
            # ProdutoModel(nome="Produto", preco=valor, ativo=True)
        ]
        db.add_all(produtos)
        db.commit()

        # Pega os IDs gerados
        for p in produtos:
            db.refresh(p)
            print(f"✅ Produto criado: (ID: {p.id}) - {p.nome} - R$ {p.preco:.2f}")

        # Abastece o Estoque da Matriz
        estoques = [
            EstoqueModel(unidade_id=unidade_matriz.id, produto_id=produtos[0].id, quantidade=50),
            EstoqueModel(unidade_id=unidade_matriz.id, produto_id=produtos[1].id, quantidade=30),
            EstoqueModel(unidade_id=unidade_matriz.id, produto_id=produtos[2].id, quantidade=100),
        ]
        db.add_all(estoques)
        db.commit()

        print("✅ Banco de dados populado com dados")

    except Exception as e:
        print(f"❌ Erro ao popular o banco: {e}")
        db.rollback()
    finally:
        db.close()

popular_banco()