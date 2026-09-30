import time
import random

class PagamentoMockAdapter:
    def processar_pagamento(self, pedido_id: int) -> dict:

        time.sleep(1)

        # 70% de chance de aprovar o pagamento, 30% de falhar
        aprovado = random.choices([True, False], weights=[70, 30], k=1)[0]

        if aprovado:
            return {
                "sucesso": True,
                "status_gateway": "APROVADO",
                "transacao_id": f"mock_txn_{pedido_id}_{int(time.time())}",
                "mensagem": "Pagamento autorizado com sucesso."
            }
        else:
            return {
                "sucesso": False,
                "status_gateway": "RECUSADO",
                "transacao_id": None,
                "mensagem": "Cartão recusado por falta de limite."
            }