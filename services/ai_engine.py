import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configura a API do Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def get_ai_response(prompt, system_instruction=None, history=None):
    try:
        model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=system_instruction or "Você é a Luna, uma assistente executiva de elite, acolhedora, inteligente e altamente focada em produtividade e alta performance."
        )
        
        # Conversa com histórico opcional
        chat = model.start_chat(history=history or [])
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao processar com a IA: {str(e)}"