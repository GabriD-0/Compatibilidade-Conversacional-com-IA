from datetime import datetime, timezone
from app.extensions import db


class Conversation(db.Model):
    __tablename__ = "conversation"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    participant_a_id = db.Column(
        db.Integer,
        db.ForeignKey("login.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    participant_b_id = db.Column(
        db.Integer,
        db.ForeignKey("login.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    message_count = db.Column(db.Integer, nullable=False, default=0)
    last_message_at = db.Column(db.DateTime, nullable=True, index=True)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    participant_a = db.relationship("Login", foreign_keys=[participant_a_id], lazy="select")
    participant_b = db.relationship("Login", foreign_keys=[participant_b_id], lazy="select")
    messages = db.relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversation.id", ondelete="CASCADE"),
        nullable=False,
    )
    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("login.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False, default="sent")

    conversation = db.relationship("Conversation", back_populates="messages")
    sender = db.relationship("Login", foreign_keys=[sender_id], lazy="select")

    __table_args__ = (
        db.Index("ix_message_conversation_position", "conversation_id", "position"),
    )
