from typing import TypedDict, Any, NotRequired
import uuid

class MessageDict(TypedDict):
    """
    Define a estrutura de um dicionário de mensagem FIPA-ACL.
    """
    # --- Campos Obrigatórios ---
    performative: str
    sender: int
    receiver: int
    content: Any    
    conversation_id: uuid # id do diálogo da mensagem