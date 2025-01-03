from typing import List, Dict

from fastapi import WebSocket


class Chat:
    def __init__(self, chat_id):
        self.active_connections: List[WebSocket] = []
        self.chat_id = chat_id


class ChatManager:
    chats: Dict[int, List[Chat]] = {}

    def create(self) -> Chat:
        new_chat = Chat(len(ChatManager.chats))
        ChatManager.chats.update({new_chat.chat_id: new_chat})

        return new_chat


chat_manager = ChatManager()