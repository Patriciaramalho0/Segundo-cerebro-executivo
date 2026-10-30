import streamlit as st
from services.data_service import DataService

class AssistantSettingsService:
    @staticmethod
    def get_settings(user_id: str) -> dict:
        try:
            supabase = DataService.get_client() if hasattr(DataService, "get_client") else None
            if not supabase and hasattr(DataService, "supabase"):
                supabase = DataService.supabase
                
            if not supabase or not user_id:
                return AssistantSettingsService._default_settings()
            
            res = supabase.table("user_assistant_settings").select("*").eq("user_id", user_id).execute()
            if res.data and len(res.data) > 0:
                return res.data[0]
        except Exception as e:
            print(f"Erro ao buscar configurações da assistente: {e}")
            
        return AssistantSettingsService._default_settings()

    @staticmethod
    def save_settings(user_id: str, settings: dict):
        try:
            supabase = DataService.get_client() if hasattr(DataService, "get_client") else None
            if not supabase and hasattr(DataService, "supabase"):
                supabase = DataService.supabase
                
            if not supabase or not user_id:
                return
            
            data = {
                "user_id": user_id,
                "assistant_name": settings.get("assistant_name", "Luna"),
                "voice_enabled": settings.get("voice_enabled", True),
                "voice_speed": settings.get("voice_speed", 1.0),
                "communication_style": settings.get("communication_style", "Acolhedora e Profissional"),
                "wake_word": settings.get("wake_word", "Luna")
            }
            
            supabase.table("user_assistant_settings").upsert(data).execute()
        except Exception as e:
            print(f"Erro ao salvar configurações da assistente: {e}")

    @staticmethod
    def _default_settings() -> dict:
        return {
            "assistant_name": "Luna",
            "voice_enabled": True,
            "voice_speed": 1.0,
            "communication_style": "Acolhedora e Profissional",
            "wake_word": "Luna"
        }