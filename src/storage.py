from .database import SessionLocal
from .models import ConversationSession, ChatMessage
from sqlalchemy import select

def create_session(title: str) -> int:
    db = SessionLocal()
    session = ConversationSession(
        title=title
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    db.close()
    return session.id

def save_message(
    session_id: int,
    role: str,
    content: str
) -> int:
    
    db = SessionLocal()
    
    chat_message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content
    )
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    db.close()
    return chat_message.id

def load_history(session_id: int) -> list[dict]:
    db = SessionLocal()
    
    stmt = select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.id)
    messages = db.execute(stmt).scalars().all()
    history = []
    for message in messages:
        history.append(
            {'role':message.role,'content':message.content}
        )
    db.close()
    return history