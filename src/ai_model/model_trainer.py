import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib # Para salvar e carregar modelos
from utils.logger import logger
import os

class AIModelTrainer:
    def __init__(self, model_path="ai_model/trained_model.pkl"):
        self.model_path = model_path
        self.model = None

    def load_data(self, file_path):
        """
        Carrega dados históricos pré-processados para treinamento.
        Os dados devem incluir features (indicadores técnicos, sentimento) e o alvo (sinal de compra/venda).
        """
        try:
            df = pd.read_csv(file_path, index_col="timestamp")
            df.index = pd.to_datetime(df.index)
            logger.info(f"Dados carregados com sucesso de {file_path}")
            return df
        except FileNotFoundError:
            logger.error(f"Arquivo de dados não encontrado: {file_path}")
            return pd.DataFrame()
        except Exception as e:
            logger.error(f"Erro ao carregar dados para treinamento: {e}")
            return pd.DataFrame()

    def train_model(self, data_df: pd.DataFrame):
        """
        Treina um modelo de IA com os dados fornecidos.
        Assume que o DataFrame contém colunas de features e uma coluna 'target' (ex: 'signal').
        """
        if data_df.empty or 'target' not in data_df.columns:
            logger.error("DataFrame vazio ou sem coluna 'target' para treinamento.")
            return False

        # Exemplo de features e target. Ajustar conforme suas features reais.
        features = ['rsi', 'macd_hist', 'average_compound_score', 'volume', 'sma_10', 'ema_10'] # Exemplo
        target = 'target' # Coluna que indica o sinal (0: HOLD, 1: BUY, 2: SELL)

        # Remover linhas com NaN nas features ou target
        data_df_cleaned = data_df.dropna(subset=features + [target])

        if data_df_cleaned.empty:
            logger.warning("Nenhum dado válido após limpeza para treinamento.")
            return False

        X = data_df_cleaned[features]
        y = data_df_cleaned[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        # Usando RandomForestClassifier como exemplo
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Avaliação básica
        y_pred = self.model.predict(X_test)
        logger.info("Relatório de Classificação:\n" + classification_report(y_test, y_pred))

        logger.info("Modelo treinado com sucesso.")
        return True

    def save_model(self):
        """
        Salva o modelo treinado em disco.
        """
        if self.model:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            logger.info(f"Modelo salvo em {self.model_path}")
            return True
        logger.warning("Nenhum modelo para salvar.")
        return False

    def load_model(self):
        """
        Carrega um modelo pré-treinado do disco.
        """
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            logger.info(f"Modelo carregado de {self.model_path}")
            return True
        logger.warning(f"Nenhum modelo encontrado em {self.model_path}")
        return False

# Exemplo de uso (para testes)
if __name__ == '__main__':
    # Criar dados de exemplo (você precisará gerar dados reais com as features e o target)
    # Este é um placeholder para simular o carregamento de dados
    sample_data = {
        'timestamp': pd.to_datetime(pd.date_range(start='2023-01-01', periods=100, freq='1min')),
        'rsi': [i % 100 for i in range(100)],
        'macd_hist': [0.1 if i % 5 == 0 else -0.1 for i in range(100)],
        'average_compound_score': [0.2 if i % 3 == 0 else -0.2 if i % 3 == 1 else 0.0 for i in range(100)],
        'volume': [1000 + i * 10 for i in range(100)],
        'sma_10': [50 + i for i in range(100)],
        'ema_10': [51 + i for i in range(100)],
        'target': [0 if i % 4 == 0 else 1 if i % 4 == 1 else 2 if i % 4 == 2 else 0 for i in range(100)] # 0:HOLD, 1:BUY, 2:SELL
    }
    sample_df = pd.DataFrame(sample_data).set_index('timestamp')

    # Salvar dados de exemplo para simular o carregamento
    sample_df.to_csv("ai_model/sample_training_data.csv")

    trainer = AIModelTrainer()
    
    # Carregar dados e treinar
    data_for_training = trainer.load_data("ai_model/sample_training_data.csv")
    if not data_for_training.empty:
        if trainer.train_model(data_for_training):
            trainer.save_model()
            # Testar carregamento
            new_trainer = AIModelTrainer()
            new_trainer.load_model()
            print("Modelo carregado com sucesso para nova instância.")


