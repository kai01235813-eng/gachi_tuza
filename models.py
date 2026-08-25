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
    archetype = Column(String, default="💎 기업 실질가치 투자자")
    title = Column(String, default="💎 가치 탐험가 Level 3")
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
    raid_title = Column(String, default="🚀 모임 공동 목표: 1,000만원 가치투자 달성")
    raid_goal = Column(Float, default=10000000.0)
    raid_progress = Column(Float, default=7450000.0)
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
    asset_type = Column(String, default="🪙 코인")  # 📈 주식 or 🪙 코인
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)  # BUY or SELL
    amount_krw = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    target_price = Column(Float, nullable=True, default=0.0)
    pnl_rate = Column(Float, default=0.0)  # 수익 손익률 %
    strategy = Column(String, default="💎 가치분석 기반 분할매수 전략")  # 투자 전략
    ai_reasoning = Column(Text, nullable=False)
    risk_review = Column(Text, nullable=True)
    lesson = Column(Text, nullable=True)
    likes_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="journals")
