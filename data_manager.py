import json
import os
from datetime import datetime

DATA_FILE = 'second_brain_data.json'

def load_data():
    """Carrega os dados do arquivo JSON ou cria a estrutura inicial."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Estrutura inicial
    initial_data = {
        "notes": [],
        "finance": {
            "transactions": [],
            "debts": []
        }
    }
    save_data(initial_data)
    return initial_data

def save_data(data):
    """Salva os dados no arquivo JSON."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_note(data, title, content):
    """Adiciona uma nota estruturada."""
    note = {
        "id": len(data['notes']) + 1,
        "timestamp": datetime.now().isoformat(),
        "title": title,
        "content": content
    }
    data['notes'].append(note)
    save_data(data)
    return note

def add_transaction(data, category, amount, description, is_income):
    """Adiciona uma transação financeira."""
    transaction = {
        "id": len(data['finance']['transactions']) + 1,
        "date": datetime.now().strftime('%Y-%m-%d'),
        "category": category,
        "amount": float(amount),
        "description": description,
        "type": "income" if is_income else "expense"
    }
    data['finance']['transactions'].append(transaction)
    save_data(data)

def get_financial_summary(data):
    """Calcula o saldo atual e retorna estatísticas básicas."""
    total_income = sum(t['amount'] for t in data['finance']['transactions'] if t['type'] == 'income')
    total_expense = sum(t['amount'] for t in data['finance']['transactions'] if t['type'] == 'expense')
    balance = total_income - total_expense
    return {
        "balance": balance,
        "total_income": total_income,
        "total_expense": total_expense
    }