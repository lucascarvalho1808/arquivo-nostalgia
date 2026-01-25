import time
import threading
from datetime import datetime, timedelta
from services.ranking_csv import gerar_ranking_comunidade

class AgendadorRanking:
    """
    Classe para agendar a atualização automática do ranking diariamente.
    Usa apenas recursos nativos do Python (threading e time).
    """

    def __init__(self):
        self.rodando = False
        # Responsável pelo agendamento
        self.thread = None

    def iniciar(self):
        """Inicia o agendador em uma thread separada"""
        if not self.rodando:
            self.rodando = True
            self.thread = threading.Thread(target=self._executar_agendamento, daemon=True)
            self.thread.start()
            print("Agendador de ranking (atualização diária)")
    
    def parar(self):
        """Para o agendador"""
        self.rodando = False
        if self.thread:
            self.thread.join()
        print("Agendador de ranking parado")
    
    def _executar_agendamento(self):
        """
        Executa a atualização do ranking a cada 24 horas.
        Primeira execução acontece imediatamente ao iniciar.
        """
        # Gera ranking pela primeira vez ao iniciar
        print("Gerando ranking inicial...")
        gerar_ranking_comunidade()

        while self.rodando:
            # Aguarda 24 horas 
            tempo_espera = 86400  
            
            print(f"Próxima atualização do ranking em 24 horas ({datetime.now().strftime('%d/%m/%Y %H:%M:%S')})")

            # Divide a espera em intervalos menores para permitir parada suave
            for _ in range(tempo_espera):
                if not self.rodando:
                    break
                time.sleep(1)

            # Se ainda estiver rodando, gera novo ranking
            if self.rodando:
                print("Atualizando ranking da comunidade...")
                gerar_ranking_comunidade()

# Instância global do agendador para uso em toda a aplicação
agendador = AgendadorRanking()