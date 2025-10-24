#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sincronização de dados LIVE com GitHub (Cloud Sync)
Permite acessar dados do bot de qualquer lugar
"""

import os
import sys
import json
import subprocess
from datetime import datetime
from pathlib import Path

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class CloudSync:
    """Gerencia sincronização de dados com GitHub"""

    def __init__(self, repo_path=None):
        """
        Inicializa sync

        Args:
            repo_path: Caminho do repositório Git (None = tenta detectar)
        """
        if repo_path is None:
            # Detectar se estamos em um repo git
            result = subprocess.run(
                ['git', 'rev-parse', '--show-toplevel'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                repo_path = result.stdout.strip()
            else:
                repo_path = os.getcwd()

        self.repo_path = Path(repo_path)
        self.data_dir = self.repo_path / 'cloud_data'
        self.data_dir.mkdir(exist_ok=True)

    def save_live_data(self, symbol='BTC/USDT', timeframe='5m', data=None):
        """
        Salva dados LIVE em JSON para sincronizar com GitHub

        Args:
            symbol: Par de trading (ex: BTC/USDT)
            timeframe: Timeframe (ex: 5m, 1h, 1d)
            data: DataFrame ou dict com dados OHLCV
        """
        try:
            # Converter DataFrame para JSON
            if hasattr(data, 'to_dict'):  # pandas DataFrame
                data_dict = data.to_dict(orient='records')
            else:
                data_dict = data

            # Criar filename
            filename = f"{symbol.replace('/', '_')}_{timeframe}.json"
            filepath = self.data_dir / filename

            # Salvar com metadata
            output = {
                'symbol': symbol,
                'timeframe': timeframe,
                'timestamp': datetime.now().isoformat(),
                'count': len(data_dict) if isinstance(data_dict, list) else 1,
                'data': data_dict
            }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, default=str)

            return filepath

        except Exception as e:
            print(f"[ERRO] Falha ao salvar dados: {e}")
            return None

    def load_live_data(self, symbol='BTC/USDT', timeframe='5m'):
        """Carrega dados salvos do JSON"""
        try:
            filename = f"{symbol.replace('/', '_')}_{timeframe}.json"
            filepath = self.data_dir / filename

            if not filepath.exists():
                return None

            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)

        except Exception as e:
            print(f"[ERRO] Falha ao carregar dados: {e}")
            return None

    def sync_to_github(self, message=None):
        """
        Faz commit e push dos dados para GitHub
        Requer git configurado
        """
        try:
            if message is None:
                message = f"[AUTO] Dados LIVE sincronizados - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            # Adicionar arquivos
            subprocess.run(['git', 'add', 'cloud_data/'], cwd=self.repo_path, check=True)

            # Verificar se há mudanças
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if not result.stdout.strip():
                print("[CLOUD] Nenhuma mudança para sincronizar")
                return False

            # Commit
            subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=self.repo_path,
                check=True
            )

            # Push
            subprocess.run(['git', 'push'], cwd=self.repo_path, check=True)

            print(f"[CLOUD] Dados sincronizados com sucesso!")
            return True

        except subprocess.CalledProcessError as e:
            print(f"[CLOUD] Erro ao sincronizar: {e}")
            return False
        except Exception as e:
            print(f"[CLOUD] Erro: {e}")
            return False

    def get_cloud_data_url(self, symbol='BTC/USDT', timeframe='5m'):
        """
        Retorna URL do arquivo no GitHub
        Útil para acessar de qualquer lugar
        """
        # Detectar repo URL
        try:
            result = subprocess.run(
                ['git', 'config', '--get', 'remote.origin.url'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            remote_url = result.stdout.strip()

            # Converter SSH para HTTPS se necessário
            if remote_url.startswith('git@'):
                remote_url = remote_url.replace(':', '/').replace('git@', 'https://')

            # Remover .git
            remote_url = remote_url.rstrip('.git')

            # Construir URL raw do GitHub
            filename = f"{symbol.replace('/', '_')}_{timeframe}.json"
            raw_url = f"{remote_url}/raw/main/cloud_data/{filename}"

            return raw_url

        except Exception as e:
            print(f"[ERRO] Falha ao gerar URL: {e}")
            return None


# Testes
if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("CLOUD SYNC - Sistema de Sincronização na Nuvem")
    print("=" * 70)
    print()

    sync = CloudSync()

    print(f"[INFO] Repositório: {sync.repo_path}")
    print(f"[INFO] Diretório de dados: {sync.data_dir}")
    print()

    # Simular dados LIVE
    test_data = [
        {"timestamp": datetime.now().isoformat(), "open": 110000, "high": 110500, "low": 109500, "close": 110300},
    ]

    # Salvar
    filepath = sync.save_live_data('BTC/USDT', '5m', test_data)
    print(f"[SALVO] {filepath}")

    # Carregar
    loaded = sync.load_live_data('BTC/USDT', '5m')
    print(f"[CARREGADO] {len(loaded['data'])} registros")

    # URL do GitHub
    url = sync.get_cloud_data_url('BTC/USDT', '5m')
    print(f"[URL] {url}")

    print()
    print("Para sincronizar com GitHub:")
    print("  sync.sync_to_github('Seu mensagem aqui')")
    print()
