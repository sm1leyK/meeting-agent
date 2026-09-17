from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

class ConversationSession(Base):
    __tablename__ = 'conversation_sessions'
    
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    title: Mapped[str] = mapped_column(String(200),default='')
    
    messages: Mapped[list['ChatMessage']] = relationship(
        back_populates='session',
        cascade='all, delete-orphan'
    )
    
class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    session_id: Mapped[int] = mapped_column(Integer,ForeignKey('conversation_sessions.id'))
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    
    session: Mapped['ConversationSession'] = relationship(
        back_populates='messages'
    )