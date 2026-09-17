from .database import SessionLocal
from .models import ConversationSession, ChatMessage
from sqlalchemy import select

def create_session(title: str) -> int:
    
    with SessionLocal() as db:
        try:
            session = ConversationSession(
                title=title
            )
            db.add(session)
            db.commit()
            db.refresh(session)
            return session.id
        except Exception as e:
            db.rollback()
            raise e
            

def save_message(
    session_id: int,
    role: str,
    content: str
) -> int:
    
    with SessionLocal() as db:
        try:
            roles = ['user','assistant']
            if role not in roles:
                raise ValueError(f'Role {role} is invalid.')
                
            stmt = select(ConversationSession).where(ConversationSession.id == session_id)
            is_exist = db.execute(stmt).scalars().first()
            if is_exist is None:
                raise ValueError(f'Session{session_id} does not exist.')
                
            chat_message = ChatMessage(
                session_id=session_id,
                role=role,
                content=content
            )
            db.add(chat_message)
            db.commit()
            db.refresh(chat_message)
            return chat_message.id
        except Exception as e:
            db.rollback()
            raise e

def get_session(session_id: int) -> ConversationSession | None:
    
    with SessionLocal() as db:
        stmt = select(ConversationSession).where(ConversationSession.id == session_id)
        session = db.execute(stmt).scalars().first()
        if session is None:
            return None
        return session
        

def load_history(session_id: int) -> list[dict]:
    
    with SessionLocal() as db:
        stmt = select(ConversationSession).where(ConversationSession.id == session_id)
        is_exist = db.execute(stmt).scalars().first()
        if is_exist is None:
            raise ValueError(f'Session{session_id} does not exist.')
            
        stmt = select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.id)
        messages = db.execute(stmt).scalars().all()
        history = []
        for message in messages:
            history.append(
                {'role':message.role,'content':message.content}
            )
        return history

def list_sessions() -> list[ConversationSession]:
    
    with SessionLocal() as db:
        
        stmt = select(ConversationSession).order_by(ConversationSession.id.desc())
        sessions = db.execute(stmt).scalars().all()
        return sessions
    
def delete_session(session_id: int) -> None:
    
    with SessionLocal() as db:
        try:
            stmt = select(ConversationSession).where(ConversationSession.id == session_id)
            session = db.execute(stmt).scalars().first()
            if session is None:
                raise ValueError(f'Session{session_id} does not exist.')
            db.delete(session)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
    