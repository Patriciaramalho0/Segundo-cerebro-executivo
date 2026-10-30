import streamlit as st
from services.data_service import DataService

class AuthService:
    def __init__(self):
        self.supabase = DataService.get_client() if hasattr(DataService, "get_client") else getattr(DataService, "supabase", None)

    @staticmethod
    def sign_in(email, password):
        try:
            supabase = DataService.get_client() if hasattr(DataService, "get_client") else getattr(DataService, "supabase", None)
            if not supabase:
                return None, "Cliente Supabase não configurado."
            
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if response and response.user:
                return response.user, None
            return None, "Credenciais inválidas."
        except Exception as e:
            return None, str(e)

    @staticmethod
    def sign_up(email, password):
        try:
            supabase = DataService.get_client() if hasattr(DataService, "get_client") else getattr(DataService, "supabase", None)
            if not supabase:
                return None, "Cliente Supabase não configurado."
            
            response = supabase.auth.sign_up({"email": email, "password": password})
            if response and response.user:
                return response.user, None
            return None, "Erro ao registrar conta."
        except Exception as e:
            return None, str(e)

    # Métodos de compatibilidade caso o código espere instâncias
    def login(self, email, password):
        return AuthService.sign_in(email, password)

    def register(self, email, password):
        return AuthService.sign_up(email, password)