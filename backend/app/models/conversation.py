from datetime import datetime, timezone
from app.extensions import db


class Conversation(db.Model):
    __tablename__ = "conversation"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    participant_a_id = db.Column(db.Integer, db.ForeignKey("login.id", ondelete="CASCADE"), nullable=False, index=True)
    participant_a = db.relationship("Login", foreign_keys=[participant_a_id], lazy="select")

    participant_b_id = db.Column(db.Integer, db.ForeignKey("login.id", ondelete="CASCADE"), nullable=True, index=True)
    participant_b = db.relationship("Login", foreign_keys=[participant_b_id], lazy="select")

    message_count = db.Column(db.Integer, nullable=False, default=0)
    messages = db.relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    last_message_at = db.Column(db.DateTime, nullable=True, index=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    conversation_id = db.Column(db.Integer, db.ForeignKey("conversation.id", ondelete="CASCADE"), nullable=False)
    conversation = db.relationship("Conversation", back_populates="messages")

    sender_id = db.Column(db.Integer, db.ForeignKey("login.id", ondelete="CASCADE"), nullable=False, index=True,)
    sender = db.relationship("Login", foreign_keys=[sender_id], lazy="select")

    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False, default="sent")

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    __table_args__ = (db.Index("ix_message_conversation_position", "conversation_id", "position"),)
