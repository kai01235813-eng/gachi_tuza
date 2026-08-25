import React, { useState, useEffect } from 'react'
import R3FCanvas from './components/R3FCanvas'
import Navbar from './components/Navbar'
import ZeroUIInput from './components/ZeroUIInput'
import FeedAndRankings from './components/FeedAndRankings'
import { LoginModal, GroupCreateModal, GroupJoinModal, JournalFormModal } from './components/Modals'

export default function App() {
  const [user, setUser] = useState({
    id: 1,
    nickname: '김가치 (가치 모임장)',
    xp: 2450,
    archetype: '💎 기업 실질가치 투자자'
  })

  const [group, setGroup] = useState({
    name: '같이투자 1기 챔피언 모임',
    code: 'GACHI7'
  })

  const [chatStream, setChatStream] = useState([
    {
      id: 1,
      sender: 'AI',
      reply: '안녕하세요! 주식 또는 코인 트레이딩 이야기를 편안하게 남겨보세요. 위 프롬프트 창에 **\'오늘 엔비디아 50만원 매수했어\'**처럼 말씀하시면 투자 전략과 함께 **+150 경험치**를 기록해드립니다!'
    }
  ])

  const [feed, setFeed] = useState([
    {
      id: 101,
      author: '김가치 (모임장)',
      asset_type: '📈 주식',
      symbol: '삼성전자',
      side: 'BUY',
      amount_krw: 1000000,
      price: 72000,
      pnl_rate: 8.5,
      strategy: '💎 실적 개선 펀더멘털 저점 매수 전략',
      ai_reasoning: '영업이익 반등 기대감 및 외국인 순매수 지속 수급 분석 완료.',
      time: '방금 전'
    },
    {
      id: 102,
      author: '박비트 (가치투자가)',
      asset_type: '🪙 코인',
      symbol: 'BTC',
      side: 'BUY',
      amount_krw: 500000,
      price: 135000000,
      pnl_rate: 12.4,
      strategy: '⚡ 국내외 가격차이 김프 0.04% 스캘핑 전략',
      ai_reasoning: '업비트 프리미엄 2.1% 회복 및 현물 ETF 유입세 확인.',
      time: '10분 전'
    }
  ])

  const [rankings, setRankings] = useState([
    { rank: 1, name: '김가치', archetype: '💎 기업 실질가치 투자자', return_pct: 14.8, xp: 2450 },
    { rank: 2, name: '박비트', archetype: '🛡️ 위험 방어 수호자', return_pct: 11.2, xp: 1980 },
    { rank: 3, name: '최솔라', archetype: '⚡ 가격차이 차익 투자자', return_pct: 7.6, xp: 1620 }
  ])

  // Modal Open States
  const [loginOpen, setLoginOpen] = useState(false)
  const [createGroupOpen, setCreateGroupOpen] = useState(false)
  const [joinGroupOpen, setJoinGroupOpen] = useState(false)
  const [journalModalOpen, setJournalModalOpen] = useState(false)

  // Natural Language Prompt Handler
  const handleSendPrompt = (promptText, assetType) => {
    const isBuy = promptText.includes('매수') || promptText.includes('샀')
    const side = isBuy ? 'BUY' : 'SELL'
    const symbol = promptText.includes('삼성') ? '삼성전자' : promptText.includes('비트') ? 'BTC' : 'SOL'

    const newXp = user.xp + 150
    setUser((prev) => ({ ...prev, xp: newXp }))

    // Append to Chat Stream
    const userMessage = { id: Date.now(), sender: 'USER', text: promptText, assetType }
    const aiResponse = {
      id: Date.now() + 1,
      sender: 'AI',
      reply: `🌱 **${user.nickname}**님, [${assetType}] '${symbol} ${side}' 매매 복기가 성공적으로 기록되었습니다!\n✨ **+150 경험치(EXP)** 획득 (현재 ${newXp.toLocaleString()} EXP)`
    }
    setChatStream((prev) => [aiResponse, userMessage, ...prev])

    // Append to Social Feed
    const newJournal = {
      id: Date.now(),
      author: user.nickname,
      asset_type: assetType,
      symbol,
      side,
      amount_krw: 100000,
      price: 100000,
      pnl_rate: 5.2,
      strategy: '💎 대화형 입력 자동 전략 감지',
      ai_reasoning: `자연어 입력 '${promptText}' 감지 및 AI 시세 분석 완료.`,
      time: '방금 전'
    }
    setFeed((prev) => [newJournal, ...prev])
  }

  // Social Login Handler
  const handleLogin = (provider) => {
    setUser({
      id: Date.now(),
      nickname: `${provider.toUpperCase()} 소셜 투자자`,
      xp: 1500,
      archetype: '💎 기업 실질가치 투자자'
    })
    setLoginOpen(false)
    alert(`🎉 ${provider.toUpperCase()} 1초 소셜 로그인 성공!`)
  }

  // Create Group Handler
  const handleCreateGroup = (name, goal) => {
    const code = Math.random().toString(36).substring(2, 8).toUpperCase()
    setGroup({ name, code })
    setCreateGroupOpen(false)
    alert(`🎉 '${name}' 모임이 생성되었습니다! 초대 코드: [${code}]`)
  }

  // Join Group Handler
  const handleJoinGroup = (code) => {
    setGroup({ name: `'${code}' 모임`, code })
    setJoinGroupOpen(false)
    alert(`🤝 '${code}' 모임에 성공적으로 참여하셨습니다!`)
  }

  // Submit Detailed Journal Handler
  const handleSubmitJournal = (data) => {
    const newXp = user.xp + 150
    setUser((prev) => ({ ...prev, xp: newXp }))

    const newJournal = {
      id: Date.now(),
      author: user.nickname,
      ...data,
      time: '방금 전'
    }
    setFeed((prev) => [newJournal, ...prev])
    setJournalModalOpen(false)
    alert(`⚡ [${data.asset_type}] ${data.symbol} 트레이딩 복기 작성 완료! +150 EXP 획득!`)
  }

  return (
    <div className="bg-gradient-to-br from-[#f8fafc] via-[#f1f5f9] to-[#e2e8f0] text-slate-900 min-h-screen relative overflow-x-hidden pb-20 selection:bg-indigo-900 selection:text-white">
      {/* 3D React Three Fiber (R3F) Background Canvas */}
      <R3FCanvas />

      {/* Top Navbar */}
      <Navbar
        user={user}
        onOpenLogin={() => setLoginOpen(true)}
        onOpenCreateGroup={() => setCreateGroupOpen(true)}
        onOpenJoinGroup={() => setJoinGroupOpen(true)}
        onOpenProfile={() => setLoginOpen(true)}
      />

      {/* Main Container */}
      <main className="max-w-2xl mx-auto px-4 pt-8 pb-6 space-y-7 relative z-10">
        {/* Welcome Banner */}
        <div className="white-navy-card p-6 rounded-3xl text-center space-y-3 relative overflow-hidden">
          <div className="flex justify-center items-center gap-2 font-jua">
            <span className="bg-slate-900 text-white px-3.5 py-1 rounded-full text-xs font-bold">{group.name}</span>
            <span className="bg-indigo-50 text-indigo-900 px-3 py-1 rounded-full text-xs font-bold border border-indigo-200">
              초대코드: {group.code}
            </span>
          </div>
          <h1 className="text-2xl font-black text-slate-900 font-jua leading-tight">
            주식 & 코인 트레이딩을 함께 기록하세요
          </h1>
          <p className="text-xs text-slate-600 font-jua leading-relaxed">
            React Three Fiber 3D 캔버스 엔진에서 투자군과 전략, 손익률을 함께 기록해보세요.
          </p>
        </div>

        {/* Zero UI Single Prompt Input Bar */}
        <ZeroUIInput onSendPrompt={handleSendPrompt} onOpenJournalModal={() => setJournalModalOpen(true)} />

        {/* Chat Stream Cards */}
        <div className="space-y-4">
          {chatStream.map((msg) =>
            msg.sender === 'USER' ? (
              <div key={msg.id} className="white-navy-card p-4 rounded-3xl space-y-1 border border-indigo-200 shadow-sm ml-8 bg-indigo-50/50">
                <div className="flex justify-between items-center text-xs font-jua">
                  <span className="text-indigo-950 font-bold">👤 내 입력 [{msg.assetType}]</span>
                  <span className="text-slate-400 text-[10px]">방금 전</span>
                </div>
                <p className="text-sm font-bold text-slate-900 font-jua">{msg.text}</p>
              </div>
            ) : (
              <div key={msg.id} className="white-navy-card p-5 rounded-3xl space-y-2 border border-slate-200">
                <div className="flex items-center gap-2">
                  <div className="w-7 h-7 rounded-xl bg-slate-900 text-white flex justify-center items-center font-bold text-xs">AI</div>
                  <span className="font-bold text-slate-900 text-xs font-jua">같이투자 AI</span>
                </div>
                <div className="text-xs text-slate-700 leading-relaxed font-jua whitespace-pre-line">{msg.reply}</div>
              </div>
            )
          )}
        </div>

        {/* Social Feed & Group Rankings View */}
        <FeedAndRankings feed={feed} rankings={rankings} />
      </main>

      {/* Modals */}
      <LoginModal isOpen={loginOpen} onClose={() => setLoginOpen(false)} onLogin={handleLogin} />
      <GroupCreateModal isOpen={createGroupOpen} onClose={() => setCreateGroupOpen(false)} onCreateGroup={handleCreateGroup} />
      <GroupJoinModal isOpen={joinGroupOpen} onClose={() => setJoinGroupOpen(false)} onJoinGroup={handleJoinGroup} />
      <JournalFormModal isOpen={journalModalOpen} onClose={() => setJournalModalOpen(false)} onSubmitJournal={handleSubmitJournal} />
    </div>
  )
}
