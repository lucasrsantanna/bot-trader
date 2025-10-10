import ccxt
from config.settings import settings
from utils.logger import logger

class OrderExecutor:
    def __init__(self):
        # Configurar Testnet se USE_TESTNET=true
        import os
        use_testnet = os.getenv('USE_TESTNET', 'false').lower() == 'true'

        if use_testnet:
            # Para Testnet, usar modo sandbox
            self.exchange = ccxt.binance({
                'apiKey': settings.BINANCE_API_KEY,
                'secret': settings.BINANCE_SECRET_KEY,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot',
                },
            })
            # Setar URLs manualmente após criação (ccxt ignora no config)
            self.exchange.urls['api'] = 'https://testnet.binance.vision'
            self.exchange.hostname = 'testnet.binance.vision'
        else:
            # Produção - Futures
            self.exchange = ccxt.binance({
                'apiKey': settings.BINANCE_API_KEY,
                'secret': settings.BINANCE_SECRET_KEY,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future',
                }
            })

        logger.info("OrderExecutor inicializado.")

    async def create_market_order(self, symbol: str, side: str, amount: float):
        """
        Cria uma ordem de mercado (compra ou venda).
        side: 'buy' ou 'sell'
        """
        try:
            order = self.exchange.create_market_order(symbol, side, amount)
            logger.info(f"Ordem de mercado {side} para {symbol} de {amount} executada: {order['id']}")
            return order
        except ccxt.NetworkError as e:
            logger.error(f"Erro de rede ao criar ordem de mercado: {e}")
        except ccxt.ExchangeError as e:
            logger.error(f"Erro da Exchange ao criar ordem de mercado: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao criar ordem de mercado: {e}")
        return None

    async def create_limit_order(self, symbol: str, side: str, amount: float, price: float):
        """
        Cria uma ordem limitada (compra ou venda).
        side: 'buy' ou 'sell'
        """
        try:
            order = self.exchange.create_limit_order(symbol, side, amount, price)
            logger.info(f"Ordem limitada {side} para {symbol} de {amount} @ {price} executada: {order['id']}")
            return order
        except ccxt.NetworkError as e:
            logger.error(f"Erro de rede ao criar ordem limitada: {e}")
        except ccxt.ExchangeError as e:
            logger.error(f"Erro da Exchange ao criar ordem limitada: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao criar ordem limitada: {e}")
        return None

    async def create_stop_loss_limit_order(self, symbol: str, side: str, amount: float, price: float, stop_price: float):
        """
        Cria uma ordem stop-loss limitada.
        side: 'buy' ou 'sell'
        price: preço limite
        stop_price: preço de disparo do stop
        """
        try:
            # A Binance não tem um método direto para stop-loss limit em ccxt, geralmente é uma ordem STOP_LOSS_LIMIT
            # que pode ser simulada ou criada com parâmetros adicionais dependendo da exchange.
            # Para simplificar, vamos usar create_order com type='STOP_LOSS_LIMIT'
            order = self.exchange.create_order(symbol, 'STOP_LOSS_LIMIT', side, amount, price, {'stopPrice': stop_price})
            logger.info(f"Ordem Stop-Loss Limit {side} para {symbol} de {amount} @ {price} (stop: {stop_price}) executada: {order['id']}")
            return order
        except ccxt.NetworkError as e:
            logger.error(f"Erro de rede ao criar ordem Stop-Loss Limit: {e}")
        except ccxt.ExchangeError as e:
            logger.error(f"Erro da Exchange ao criar ordem Stop-Loss Limit: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao criar ordem Stop-Loss Limit: {e}")
        return None

    async def cancel_order(self, order_id: str, symbol: str):
        """
        Cancela uma ordem existente.
        """
        try:
            cancel_result = self.exchange.cancel_order(order_id, symbol)
            logger.info(f"Ordem {order_id} para {symbol} cancelada com sucesso.")
            return cancel_result
        except ccxt.NetworkError as e:
            logger.error(f"Erro de rede ao cancelar ordem: {e}")
        except ccxt.ExchangeError as e:
            logger.error(f"Erro da Exchange ao cancelar ordem: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao cancelar ordem: {e}")
        return None

    async def fetch_order_status(self, order_id: str, symbol: str):
        """
        Busca o status de uma ordem.
        """
        try:
            order = self.exchange.fetch_order(order_id, symbol)
            logger.info(f"Status da ordem {order_id} para {symbol}: {order['status']}")
            return order
        except ccxt.NetworkError as e:
            logger.error(f"Erro de rede ao buscar status da ordem: {e}")
        except ccxt.ExchangeError as e:
            logger.error(f"Erro da Exchange ao buscar status da ordem: {e}")
        except Exception as e:
            logger.error(f"Erro inesperado ao buscar status da ordem: {e}")
        return None

# Exemplo de uso (para testes)
async def main():
    executor = OrderExecutor()
    symbol = "BTC/USDT"
    amount = 0.001 # Pequena quantidade para teste
    price = 20000.0 # Preço de exemplo
    stop_price = 19950.0 # Preço de stop de exemplo

    # Certifique-se de que suas chaves de API da Binance (testnet) estão configuradas no .env
    # e que você tem saldo suficiente na conta de teste.

    # Exemplo de ordem de mercado (descomente para testar)
    # market_buy_order = await executor.create_market_order(symbol, 'buy', amount)
    # if market_buy_order:
    #     print(f"Ordem de compra de mercado criada: {market_buy_order['id']}")

    # Exemplo de ordem limitada (descomente para testar)
    # limit_sell_order = await executor.create_limit_order(symbol, 'sell', amount, price)
    # if limit_sell_order:
    #     print(f"Ordem de venda limitada criada: {limit_sell_order['id']}")

    # Exemplo de ordem stop-loss limitada (descomente para testar)
    # stop_loss_order = await executor.create_stop_loss_limit_order(symbol, 'sell', amount, price, stop_price)
    # if stop_loss_order:
    #     print(f"Ordem Stop-Loss Limit criada: {stop_loss_order['id']}")

    # Exemplo de cancelamento de ordem (substitua 'order_id' por um ID real)
    # if market_buy_order:
    #     await executor.cancel_order(market_buy_order['id'], symbol)

    # Exemplo de busca de status de ordem (substitua 'order_id' por um ID real)
    # if market_buy_order:
    #     await executor.fetch_order_status(market_buy_order['id'], symbol)

if __name__ == '__main__':
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Execução interrompida pelo usuário.")

