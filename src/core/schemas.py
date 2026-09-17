from pydantic import BaseModel

class MeetingSummary(BaseModel):
    meeting_topic: str
    main_discussions: list[str]
    key_facts: list[str]
    opinions_and_questions: list[str]
    decisions: list[str]
    action_items: list[str]    
    