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
    
    # --- Campos Opcionais ---
    conversation_id: NotRequired[uuid] # id do diálogo da mensagem