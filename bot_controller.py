"""
CONTROLADOR DO BOT - Inicia/Para o bot independentemente do dashboard
"""
import os
import sys
import json
import subprocess
import psutil
import signal
from pathlib import Path

ARQUIVO_PID = "bot.pid"
ARQUIVO_DADOS = "bot_dados.json"

class BotController:
    def __init__(self):
        self.pid = self.carregar_pid()

    def carregar_pid(self):
        """Carrega PID salvo"""
        if os.path.exists(ARQUIVO_PID):
            with open(ARQUIVO_PID, 'r') as f:
                return int(f.read().strip())
        return None

    def salvar_pid(self, pid):
        """Salva PID"""
        with open(ARQUIVO_PID, 'w') as f:
            f.write(str(pid))

    def remover_pid(self):
        """Remove arquivo PID"""
        if os.path.exists(ARQUIVO_PID):
            os.remove(ARQUIVO_PID)

    def bot_esta_rodando(self):
        """Verifica se bot está rodando"""
        if not self.pid:
            return False

        try:
            process = psutil.Process(self.pid)
            return process.is_running() and 'python' in process.name().lower()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def iniciar_bot(self):
        """Inicia o bot"""
        if self.bot_esta_rodando():
            print(f"[AVISO] Bot ja esta rodando (PID: {self.pid})")
            return False

        print("[INICIANDO] Bot trader...")

        # Iniciar bot em processo separado
        python_exe = os.path.join("venv", "Scripts", "python.exe")

        # Windows: usar CREATE_NEW_PROCESS_GROUP
        if sys.platform == "win32":
            DETACHED_PROCESS = 0x00000008
            process = subprocess.Popen(
                [python_exe, "bot_automatico.py"],
                creationflags=DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            process = subprocess.Popen(
                [python_exe, "bot_automatico.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setpgrp
            )

        self.pid = process.pid
        self.salvar_pid(self.pid)

        print(f"[OK] Bot iniciado! PID: {self.pid}")
        print(f"[INFO] Bot rodara continuamente ate ser parado")
        print(f"[INFO] Dados em: {ARQUIVO_DADOS}")
        return True

    def parar_bot(self):
        """Para o bot"""
        if not self.bot_esta_rodando():
            print("[AVISO] Bot nao esta rodando")
            self.remover_pid()
            return False

        print(f"[PARANDO] Bot (PID: {self.pid})...")

        try:
            process = psutil.Process(self.pid)

            # Tentar terminar graciosamente
            process.terminate()

            # Aguardar até 5 segundos
            try:
                process.wait(timeout=5)
            except psutil.TimeoutExpired:
                # Force kill se não parar
                process.kill()
                process.wait()

            self.remover_pid()
            print("[OK] Bot parado com sucesso")
            return True

        except Exception as e:
            print(f"[ERRO] Falha ao parar bot: {e}")
            self.remover_pid()
            return False

    def status_bot(self):
        """Mostra status do bot"""
        print("="*70)
        print(" STATUS DO BOT")
        print("="*70)

        if self.bot_esta_rodando():
            print(f"Status: RODANDO")
            print(f"PID: {self.pid}")

            # Ler dados
            if os.path.exists(ARQUIVO_DADOS):
                with open(ARQUIVO_DADOS, 'r') as f:
                    dados = json.load(f)

                print(f"\nCapital: ${dados['capital']:.2f}")
                print(f"Trades executados: {len(dados['trades'])}")
                print(f"Posicao: {'ABERTA' if dados['posicao'] else 'FECHADA'}")

                if dados['logs']:
                    print(f"\nUltimos 5 logs:")
                    for log in dados['logs'][-5:]:
                        print(f"  {log}")

                print(f"\nUltima atualizacao: {dados.get('ultima_atualizacao', 'N/A')}")
        else:
            print(f"Status: PARADO")

        print("="*70)

    def reiniciar_bot(self):
        """Reinicia o bot"""
        print("[REINICIANDO] Bot...")
        self.parar_bot()
        import time
        time.sleep(2)
        self.iniciar_bot()

def main():
    controller = BotController()

    if len(sys.argv) < 2:
        print("Uso: python bot_controller.py [iniciar|parar|status|reiniciar]")
        print()
        print("Comandos:")
        print("  iniciar   - Inicia o bot em background")
        print("  parar     - Para o bot")
        print("  status    - Mostra status atual")
        print("  reiniciar - Reinicia o bot")
        sys.exit(1)

    comando = sys.argv[1].lower()

    if comando == "iniciar" or comando == "start":
        controller.iniciar_bot()
    elif comando == "parar" or comando == "stop":
        controller.parar_bot()
    elif comando == "status":
        controller.status_bot()
    elif comando == "reiniciar" or comando == "restart":
        controller.reiniciar_bot()
    else:
        print(f"[ERRO] Comando desconhecido: {comando}")
        sys.exit(1)

if __name__ == "__main__":
    main()
