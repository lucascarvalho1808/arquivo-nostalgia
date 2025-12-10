import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Configura a API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("AVISO: GEMINI_API_KEY não encontrada no arquivo .env")

def gerar_arquivo_confidencial(titulo, tipo_midia):
    """
    Gera uma curiosidade rápida de bastidores (Trivia) sobre a mídia.
    Ideal para a seção 'Arquivo Confidencial' da home.
    """
    if not GEMINI_API_KEY:
        return "Curiosidade confidencial indisponível no momento."

    try:
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Aja como um especialista em curiosidades de cinema, séries e games.
        Escreva UMA única curiosidade surpreendente de bastidores sobre o {tipo_midia}: "{titulo}".
        
        Regras:
        1. O texto deve ser curto e direto (máximo 40 palavras).
        2. O estilo deve ser informativo e curioso, como: "Originalmente, tal coisa seria assim..." ou "O ator tal fez isso...".
        3. NÃO use introduções como "Você sabia que" ou "Uma curiosidade é". Vá direto ao fato.
        4. Responda em Português do Brasil.
        
        Exemplo de estilo desejado:
        "Originalmente, a máquina do tempo seria uma geladeira, mas Spielberg mudou a ideia por medo de que crianças começassem a se trancar em geladeiras."
        """

        response = model.generate_content(prompt)
        
        # Retorna o texto gerado limpo
        return response.text.strip()

    except Exception as e:
        print(f"Erro ao gerar curiosidade para '{titulo}': {e}")
        return "Dados confidenciais corrompidos. Tente novamente mais tarde."

# Teste rápido
if __name__ == "__main__":
    print("--- Testando Curiosidade do Dia ---")
    # Teste com o exemplo que você deu para ver se a IA segue o padrão
    resultado = gerar_arquivo_confidencial("De Volta para o Futuro", "filme")
    print(f"Resultado:\n{resultado}")