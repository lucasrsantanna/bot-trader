"""
TESTADOR INTERATIVO DOS CONTROLES DO BOT
Guia passo a passo para testar cada funcionalidade
"""
import json
import os
import time
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

CONTROLE_FILE = "bot_controle.json"
DADOS_FILE = "bot_dados.json"

def print_header(texto):
    print("\n" + "=" * 70)
    print(f"{Fore.CYAN}{Style.BRIGHT}{texto.center(70)}")
    print("=" * 70 + "\n")

def print_success(texto):
    print(f"{Fore.GREEN}✓ {texto}")

def print_info(texto):
    print(f"{Fore.YELLOW}→ {texto}")

def print_error(texto):
    print(f"{Fore.RED}✗ {texto}")

def carregar_dados():
    if os.path.exists(DADOS_FILE):
        with open(DADOS_FILE, 'r') as f:
            return json.load(f)
    return None

def criar_controle(comando):
    """Cria arquivo de controle para o bot"""
    controle = {
        "pausado": False,
        "forcar_entrada": None,
        "forcar_saida": False,
        "novo_intervalo": None,
        "novos_parametros": None,
        "timestamp": datetime.now().isoformat()
    }
    controle.update(comando)

    with open(CONTROLE_FILE, 'w') as f:
        json.dump(controle, f, indent=2)

    print_success(f"Comando enviado ao bot: {comando}")

def aguardar_resposta(segundos=10):
    """Aguarda o bot processar o comando"""
    print_info(f"Aguardando {segundos}s para o bot processar...")

    for i in range(segundos, 0, -1):
        print(f"{Fore.CYAN}  {i}s...", end='\r')
        time.sleep(1)
    print(" " * 50, end='\r')

def verificar_bot_rodando():
    """Verifica se o bot está rodando"""
    dados = carregar_dados()
    if not dados:
        print_error("bot_dados.json não encontrado!")
        print_info("Execute EXECUTAR_BOT.bat primeiro!")
        return False

    # Verificar última atualização
    ultima = dados.get('ultima_atualizacao', '')
    if ultima:
        ultima_dt = datetime.fromisoformat(ultima)
        diff = (datetime.now() - ultima_dt).total_seconds()

        if diff < 120:  # Menos de 2 minutos
            print_success(f"Bot está rodando! (última atualização: {int(diff)}s atrás)")
            return True
        else:
            print_error(f"Bot parece parado (última atualização: {int(diff)}s atrás)")
            print_info("Execute EXECUTAR_BOT.bat para iniciar")
            return False

    return False

def mostrar_status():
    """Mostra status atual do bot"""
    dados = carregar_dados()
    if not dados:
        return

    print_header("STATUS ATUAL DO BOT")

    print(f"{Fore.CYAN}Capital:{Style.RESET_ALL} ${dados['capital']:.2f}")
    print(f"{Fore.CYAN}Trades:{Style.RESET_ALL} {len(dados['trades'])}")

    if dados.get('posicao'):
        pos = dados['posicao']
        print(f"{Fore.GREEN}Posição:{Style.RESET_ALL} {pos['tipo']} ABERTA")
        print(f"  Entrada: ${pos['preco_entrada']:,.2f}")
        print(f"  Quantidade: {pos['quantidade']:.6f} BTC")
        print(f"  Stop Loss: ${pos['stop_loss']:,.2f}")
        print(f"  Take Profit: ${pos['take_profit']:,.2f}")
    else:
        print(f"{Fore.YELLOW}Posição:{Style.RESET_ALL} FECHADA")

    config = dados['config']
    print(f"{Fore.CYAN}Intervalo:{Style.RESET_ALL} {config['intervalo']}s")
    print(f"{Fore.CYAN}Stop Loss:{Style.RESET_ALL} {config['stop_loss']*100:.2f}%")
    print(f"{Fore.CYAN}Take Profit:{Style.RESET_ALL} {config['take_profit']*100:.2f}%")

def teste_pausar():
    """Teste 1: Pausar o bot"""
    print_header("TESTE 1: PAUSAR O BOT")

    print_info("Este teste vai PAUSAR o bot temporariamente")
    print_info("O bot vai parar de analisar o mercado")
    print_info("Mas continuará monitorando posições abertas")
    print()

    input(f"{Fore.YELLOW}Pressione ENTER para PAUSAR o bot...{Style.RESET_ALL}")

    criar_controle({"pausado": True})
    aguardar_resposta(10)

    print()
    print_success("Bot deve estar PAUSADO agora!")
    print_info("Verifique no terminal do bot a mensagem:")
    print(f"  {Fore.GREEN}[DASHBOARD] Bot pausado pelo dashboard{Style.RESET_ALL}")
    print()

    input(f"{Fore.YELLOW}Viu a mensagem no terminal? Pressione ENTER para continuar...{Style.RESET_ALL}")

    # Retomar
    print()
    print_info("Agora vamos RETOMAR o bot...")
    input(f"{Fore.YELLOW}Pressione ENTER para RETOMAR...{Style.RESET_ALL}")

    criar_controle({"pausado": False})
    aguardar_resposta(5)

    print()
    print_success("Teste 1 COMPLETO!")
    print_info("Bot deve estar rodando normalmente de novo")

def teste_fechar_posicao():
    """Teste 2: Fechar posição manualmente"""
    print_header("TESTE 2: FECHAR POSIÇÃO MANUAL")

    dados = carregar_dados()
    if not dados or not dados.get('posicao'):
        print_error("Não há posição aberta para fechar!")
        print_info("Pulando este teste...")
        return

    pos = dados['posicao']
    print_info(f"Posição atual: {pos['tipo']}")
    print_info(f"Entrada: ${pos['preco_entrada']:,.2f}")
    print()

    input(f"{Fore.YELLOW}Pressione ENTER para FECHAR esta posição...{Style.RESET_ALL}")

    criar_controle({"forcar_saida": True})
    aguardar_resposta(15)

    print()
    print_success("Comando de fechamento enviado!")
    print_info("Verifique no terminal do bot:")
    print(f"  {Fore.GREEN}[DASHBOARD] Fechamento manual solicitado{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}[FECHANDO POSICAO - ORDEM MANUAL]{Style.RESET_ALL}")
    print()

    input(f"{Fore.YELLOW}Viu a posição fechar? Pressione ENTER...{Style.RESET_ALL}")

    # Verificar se fechou
    dados_novo = carregar_dados()
    if dados_novo and not dados_novo.get('posicao'):
        print_success("✓✓✓ Posição FECHADA com sucesso!")
        print_info(f"Novo capital: ${dados_novo['capital']:.2f}")
    else:
        print_error("Posição ainda aparece como aberta...")

    print_success("Teste 2 COMPLETO!")

def teste_forcar_compra():
    """Teste 3: Forçar entrada de compra"""
    print_header("TESTE 3: FORÇAR COMPRA MANUAL")

    dados = carregar_dados()
    if dados and dados.get('posicao'):
        print_error("Já existe uma posição aberta!")
        print_info("Feche a posição atual antes de abrir nova")
        print_info("Pulando este teste...")
        return

    print_info("Este teste vai FORÇAR uma COMPRA (LONG)")
    print_info("O bot vai comprar BTC agora, independente do RSI")
    print()

    input(f"{Fore.YELLOW}Pressione ENTER para FORÇAR COMPRA...{Style.RESET_ALL}")

    criar_controle({"forcar_entrada": "BUY"})
    aguardar_resposta(15)

    print()
    print_success("Ordem de COMPRA enviada!")
    print_info("Verifique no terminal do bot:")
    print(f"  {Fore.GREEN}[DASHBOARD] Entrada manual: BUY{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}[EXECUTANDO COMPRA]{Style.RESET_ALL}")
    print()

    input(f"{Fore.YELLOW}Viu a compra executar? Pressione ENTER...{Style.RESET_ALL}")

    # Verificar se abriu posição
    dados_novo = carregar_dados()
    if dados_novo and dados_novo.get('posicao'):
        pos = dados_novo['posicao']
        print_success("✓✓✓ Posição ABERTA com sucesso!")
        print_info(f"Tipo: {pos['tipo']}")
        print_info(f"Entrada: ${pos['preco_entrada']:,.2f}")
        print_info(f"Quantidade: {pos['quantidade']:.6f} BTC")
    else:
        print_error("Posição não foi aberta...")

    print_success("Teste 3 COMPLETO!")

def teste_ajustar_intervalo():
    """Teste 4: Ajustar intervalo em tempo real"""
    print_header("TESTE 4: AJUSTAR INTERVALO")

    dados = carregar_dados()
    if not dados:
        return

    intervalo_atual = dados['config']['intervalo']
    novo_intervalo = 30 if intervalo_atual != 30 else 45

    print_info(f"Intervalo atual: {intervalo_atual}s")
    print_info(f"Vamos mudar para: {novo_intervalo}s")
    print()

    input(f"{Fore.YELLOW}Pressione ENTER para MUDAR INTERVALO...{Style.RESET_ALL}")

    criar_controle({"novos_parametros": {"intervalo": novo_intervalo}})
    aguardar_resposta(10)

    print()
    print_success(f"Intervalo alterado para {novo_intervalo}s!")
    print_info("Verifique no terminal do bot:")
    print(f"  {Fore.GREEN}[DASHBOARD] Parametros atualizados!{Style.RESET_ALL}")
    print()
    print_info("Agora o bot vai analisar o mercado mais rápido/devagar")

    print_success("Teste 4 COMPLETO!")

def teste_ajustar_stop_loss():
    """Teste 5: Ajustar Stop Loss"""
    print_header("TESTE 5: AJUSTAR STOP LOSS")

    dados = carregar_dados()
    if not dados:
        return

    stop_atual = dados['config']['stop_loss']
    novo_stop = 0.005 if stop_atual != 0.005 else 0.003

    print_info(f"Stop Loss atual: {stop_atual*100:.2f}%")
    print_info(f"Vamos mudar para: {novo_stop*100:.2f}%")
    print()

    input(f"{Fore.YELLOW}Pressione ENTER para MUDAR STOP LOSS...{Style.RESET_ALL}")

    criar_controle({"novos_parametros": {"stop_loss": novo_stop}})
    aguardar_resposta(10)

    print()
    print_success(f"Stop Loss alterado para {novo_stop*100:.2f}%!")
    print_info("Próximo trade vai usar este novo valor")

    print_success("Teste 5 COMPLETO!")

def menu_principal():
    """Menu principal"""
    while True:
        print_header("TESTADOR INTERATIVO - BOT TRADER")

        # Verificar se bot está rodando
        bot_ok = verificar_bot_rodando()
        print()

        if not bot_ok:
            print_error("ATENÇÃO: Execute EXECUTAR_BOT.bat antes de testar!")
            print()
            input("Pressione ENTER após iniciar o bot...")
            continue

        # Mostrar status
        mostrar_status()
        print()

        # Menu
        print(f"{Fore.CYAN}ESCOLHA UM TESTE:{Style.RESET_ALL}")
        print()
        print("  1. Pausar e Retomar bot")
        print("  2. Fechar posição manual")
        print("  3. Forçar compra manual")
        print("  4. Ajustar intervalo em tempo real")
        print("  5. Ajustar Stop Loss")
        print()
        print("  6. Executar TODOS os testes")
        print("  7. Ver status atualizado")
        print()
        print("  0. Sair")
        print()

        escolha = input(f"{Fore.YELLOW}Digite o número do teste: {Style.RESET_ALL}")

        if escolha == "1":
            teste_pausar()
        elif escolha == "2":
            teste_fechar_posicao()
        elif escolha == "3":
            teste_forcar_compra()
        elif escolha == "4":
            teste_ajustar_intervalo()
        elif escolha == "5":
            teste_ajustar_stop_loss()
        elif escolha == "6":
            print_header("EXECUTANDO TODOS OS TESTES")
            teste_pausar()
            input("\nPressione ENTER para próximo teste...")
            teste_fechar_posicao()
            input("\nPressione ENTER para próximo teste...")
            teste_forcar_compra()
            input("\nPressione ENTER para próximo teste...")
            teste_ajustar_intervalo()
            input("\nPressione ENTER para próximo teste...")
            teste_ajustar_stop_loss()
            print_header("TODOS OS TESTES COMPLETOS!")
        elif escolha == "7":
            continue  # Recarrega o menu com status atualizado
        elif escolha == "0":
            print()
            print_success("Até logo!")
            break
        else:
            print_error("Opção inválida!")

        print()
        input("Pressione ENTER para voltar ao menu...")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print()
        print_success("Até logo!")
