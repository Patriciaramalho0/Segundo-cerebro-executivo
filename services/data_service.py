import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env se existir
load_dotenv()

class DataService:
    _client: Client = None

    @classmethod
    def get_client(cls) -> Client:
        if cls._client is not None:
            return cls._client
        
        # Tenta buscar das variáveis de ambiente do sistema/arquivo .env
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        
        # Se não achar no ambiente, tenta buscar dos segredos do Streamlit
        if (not url or not key) and hasattr(st, "secrets"):
            try:
                url = st.secrets.get("SUPABASE_URL") or st.secrets.get("supabase", {}).get("url")
                key = st.secrets.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_ANON_KEY") or st.secrets.get("supabase", {}).get("key")
            except Exception:
                pass

        if url and key:
            cls._client = create_client(url, key)
            
        return cls._client

    @property
    def supabase(self):
        return DataService.get_client()

    @classmethod
    @property
    def client(cls):
        return cls.get_client()