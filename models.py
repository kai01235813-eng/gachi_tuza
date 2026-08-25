from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nickname = Column(String, nullable=False)
    provider = Column(String, default="kakao")  # kakao, naver, google
    profile_img = Column(String, nullable=True)
    level = Column(Integer, default=3)
    xp = Column(Integer, default=1450)
    created_at = Column(DateTime, default=datetime.utcnow)

    journals = relationship("TradeJournal", back_populates="author")
    squad_memberships = relationship("SquadMember", back_populates="user")

class Squad(Base):
    __tablename__ = "squads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    members = relationship("SquadMember", back_populates="squad")

class SquadMember(Base):
    __tablename__ = "squad_members"

    id = Column(Integer, primary_key=True, index=True)
    squad_id = Column(Integer, ForeignKey("squads.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    joined_at = Column(DateTime, default=datetime.utcnow)

    squad = relationship("Squad", back_populates="members")
    user = relationship("User", back_populates="squad_memberships")

class TradeJournal(Base):
    __tablename__ = "trade_journals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)  # BUY or SELL
    amount_krw = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    ai_reasoning = Column(Text, nullable=False)
    risk_review = Column(Text, nullable=True)
    lesson = Column(Text, nullable=True)
    likes_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="journals")
