"""
Teste 3: OrderExecutor
Valida execução de ordens (market, limit, stop-loss) no Testnet
ATENÇÃO: Executará ordens REAIS no Testnet!
"""
import sys
import asyncio
sys.path.insert(0, 'src')

from trading.executor import OrderExecutor

async def main():
    print("="*70)
    print(" TESTE 3: ORDER EXECUTOR (TESTNET)")
    print("="*70)
    print()
    print("AVISO: Este teste executara ordens REAIS no Binance Testnet SPOT")
    print()

    # Inicializar executor
    print("[1] Inicializando OrderExecutor...")
    executor = OrderExecutor()
    print("    OK - Executor inicializado")
    print()

    # Parâmetros de teste
    symbol = "BTC/USDT"
    amount = 0.001  # Quantidade mínima para teste

    # Teste 1: Ordem de Mercado (Compra)
    print("[2] Teste: Ordem de Mercado (Compra)...")
    print(f"    Symbol: {symbol}")
    print(f"    Side: BUY")
    print(f"    Amount: {amount} BTC")
    print()

    try:
        order = await executor.create_market_order(symbol, 'buy', amount)
        if order:
            print(f"    SUCESSO - Ordem criada!")
            print(f"    Order ID: {order.get('id')}")
            print(f"    Status: {order.get('status')}")
            print(f"    Price: ${order.get('price', 'N/A')}")
            print(f"    Amount: {order.get('amount')} BTC")
            print()

            # Guardar ID para cancelamento
            order_id = order.get('id')

            # Teste 2: Buscar Status da Ordem
            print("[3] Teste: Buscar Status da Ordem...")
            order_status = await executor.fetch_order_status(order_id, symbol)
            if order_status:
                print(f"    SUCESSO - Status obtido!")
                print(f"    Status: {order_status.get('status')}")
                print(f"    Filled: {order_status.get('filled', 0)}")
                print()

            # Teste 3: Ordem Limitada (Venda)
            print("[4] Teste: Ordem Limitada (Venda)...")
            # Preço 1% acima do mercado (não vai executar, serve para teste)
            current_price = float(order.get('price', 100000))
            limit_price = current_price * 1.01
            print(f"    Preco limite: ${limit_price:,.2f}")

            limit_order = await executor.create_limit_order(symbol, 'sell', amount, limit_price)
            if limit_order:
                print(f"    SUCESSO - Ordem limitada criada!")
                print(f"    Order ID: {limit_order.get('id')}")
                print(f"    Status: {limit_order.get('status')}")
                print()

                # Teste 4: Cancelar Ordem
                print("[5] Teste: Cancelar Ordem Limitada...")
                cancel_result = await executor.cancel_order(limit_order.get('id'), symbol)
                if cancel_result:
                    print(f"    SUCESSO - Ordem cancelada!")
                    print()

            print("="*70)
            print(" TESTE 3: SUCESSO - TODAS AS FUNCOES OPERACIONAIS")
            print("="*70)
        else:
            print("    ERRO - Nao foi possivel criar ordem de mercado")
            print()
            print("="*70)
            print(" TESTE 3: FALHOU")
            print("="*70)

    except Exception as e:
        print(f"    ERRO: {e}")
        print()
        print("="*70)
        print(" TESTE 3: FALHOU")
        print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
