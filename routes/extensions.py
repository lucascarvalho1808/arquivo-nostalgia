import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega variáveis de ambiente do arquivo .env 
load_dotenv()

# Obtém a URL e a chave do Supabase das variáveis de ambiente
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Cria a instância do cliente Supabase para uso em toda a aplicação
supabase: Client = create_client(url, key)