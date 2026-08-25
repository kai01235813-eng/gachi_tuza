import React, { useState } from 'react'
import { X, MessageSquare, Shield, CheckCircle } from 'lucide-react'

export function LoginModal({ isOpen, onClose, onLogin }) {
  if (!isOpen) return null
  return (
    <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex justify-center items-center p-4 font-jua">
      <div className="bg-white w-full max-w-sm rounded-3xl p-6 shadow-2xl space-y-5 text-center relative border border-slate-200">
        <button onClick={onClose} className="absolute top-4 right-4 text-slate-400 hover:text-slate-700">
          <X className="w-5 h-5" />
        </button>
        <div className="space-y-1">
          <div className="w-12 h-12 bg-slate-900 text-white rounded-2xl flex justify-center items-center mx-auto text-xl shadow-md">
            <Shield className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-black text-slate-900">같이투자 1초 간편 로그인</h3>
          <p class="text-xs text-slate-500">소셜 계정으로 빠르게 시작하세요</p>
        </div>
        <div className="space-y-2.5 pt-2">
          <button
            onClick={() => onLogin('kakao')}
            className="w-full bg-[#FEE500] hover:bg-[#FEE500]/90 text-[#191919] font-bold text-xs py-3 px-4 rounded-xl transition flex justify-center items-center gap-2 shadow-sm"
          >
            <MessageSquare className="w-4 h-4" />
            <span>카카오 1초 로그인</span>
          </button>
          <button
            onClick={() => onLogin('naver')}
            className="w-full bg-[#03C75A] hover:bg-[#03C75A]/90 text-white font-bold text-xs py-3 px-4 rounded-xl transition flex justify-center items-center gap-2 shadow-sm"
          >
            <span className="font-black text-sm">N</span>
            <span>네이버 1초 로그인</span>
          </button>
          <button
            onClick={() => onLogin('google')}
            className="w-full bg-slate-100 hover:bg-slate-200 text-slate-900 font-bold text-xs py-3 px-4 rounded-xl transition flex justify-center items-center gap-2 shadow-sm border border-slate-200"
          >
            <span className="font-bold text-sm text-red-500">G</span>
            <span>구글 1초 로그인</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export function GroupCreateModal({ isOpen, onClose, onCreateGroup }) {
  const [name, setName] = useState('')
  const [goal, setGoal] = useState('10000000')

  if (!isOpen) return null

  const handleSubmit = (e) => {
    e.preventDefault()
    onCreateGroup(name, parseFloat(goal))
    setName('')
  }

  return (
    <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex justify-center items-center p-4 font-jua">
      <div className="bg-white w-full max-w-md rounded-3xl p-6 shadow-2xl space-y-4 relative border border-slate-200">
        <button onClick={onClose} className="absolute top-4 right-4 text-slate-400 hover:text-slate-700">
          <X className="w-5 h-5" />
        </button>
        <div className="text-center space-y-1">
          <h3 className="text-lg font-black text-slate-900">새 투자 모임/그룹 만들기</h3>
          <p className="text-xs text-slate-500">지인들과 함께 트레이딩할 모임을 생성합니다</p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-3 text-xs">
          <div>
            <label className="block text-slate-700 mb-1">📢 모임 이름</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="예: 2026 주식&코인 가치투자 모임"
              required
              className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2.5 text-slate-900 focus:outline-none focus:border-indigo-500"
            />
          </div>
          <div>
            <label className="block text-slate-700 mb-1">🎯 모임 공동 목표 금액 (원)</label>
            <input
              type="number"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              placeholder="10000000"
              required
              className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2.5 text-slate-900 focus:outline-none focus:border-indigo-500"
            />
          </div>
          <button type="submit" className="w-full bg-slate-900 hover:bg-slate-800 text-white font-black py-3 rounded-xl shadow-md text-sm">
            모임 생성하고 초대 코드 받기
          </button>
        </form>
      </div>
    </div>
  )
}

export function GroupJoinModal({ isOpen, onClose, onJoinGroup }) {
  const [code, setCode] = useState('')

  if (!isOpen) return null

  const handleSubmit = (e) => {
    e.preventDefault()
    onJoinGroup(code)
    setCode('')
  }

  return (
    <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex justify-center items-center p-4 font-jua">
      <div className="bg-white w-full max-w-md rounded-3xl p-6 shadow-2xl space-y-4 relative border border-slate-200">
        <button onClick={onClose} className="absolute top-4 right-4 text-slate-400 hover:text-slate-700">
          <X className="w-5 h-5" />
        </button>
        <div className="text-center space-y-1">
          <h3 className="text-lg font-black text-slate-900">기존 모임 참여하기</h3>
          <p className="text-xs text-slate-500">지인에게 받은 6자리 초대 코드를 입력하세요</p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-3 text-xs">
          <div>
            <label className="block text-slate-700 mb-1">🔑 6자리 초대 코드</label>
            <input
              type="text"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="예: GACHI7"
              required
              className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2.5 text-slate-900 focus:outline-none focus:border-indigo-500 uppercase tracking-widest text-center font-mono font-bold"
            />
          </div>
          <button type="submit" className="w-full bg-indigo-900 hover:bg-indigo-800 text-white font-black py-3 rounded-xl shadow-md text-sm">
            모임 참여 완료
          </button>
        </form>
      </div>
    </div>
  )
}

export function JournalFormModal({ isOpen, onClose, onSubmitJournal }) {
  const [assetType, setAssetType] = useState('📈 주식')
  const [symbol, setSymbol] = useState('')
  const [side, setSide] = useState('BUY')
  const [amount, setAmount] = useState('1000000')
  const [price, setPrice] = useState('72000')
  const [pnl, setPnl] = useState('8.5')
  const [strategy, setStrategy] = useState('💎 기업 실질가치 장기분석 전략')
  const [reasoning, setReasoning] = useState('')

  if (!isOpen) return null

  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmitJournal({
      asset_type: assetType,
      symbol,
      side,
      amount_krw: parseFloat(amount),
      price: parseFloat(price),
      pnl_rate: parseFloat(pnl || 0),
      strategy,
      ai_reasoning: reasoning
    })
    setSymbol('')
    setReasoning('')
  }

  return (
    <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex justify-center items-center p-4 font-jua">
      <div className="bg-white w-full max-w-md rounded-3xl p-6 shadow-2xl space-y-4 relative border border-slate-200">
        <button onClick={onClose} className="absolute top-4 right-4 text-slate-400 hover:text-slate-700">
          <X className="w-5 h-5" />
        </button>
        <h3 className="text-base font-black text-slate-900 flex items-center gap-2">
          <CheckCircle className="w-5 h-5 text-indigo-900" /> 트레이딩 기록 작성 (+150 EXP)
        </h3>
        <form onSubmit={handleSubmit} className="space-y-3 text-xs">
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-slate-700 mb-1">🎯 투자군</label>
              <select
                value={assetType}
                onChange={(e) => setAssetType(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-slate-900 focus:outline-none focus:border-indigo-500"
              >
                <option value="📈 주식">📈 주식 (국장/해외)</option>
                <option value="🪙 코인">🪙 코인 (가상자산)</option>
              </select>
            </div>
            <div>
              <label className="block text-slate-700 mb-1">매매 구분</label>
              <select
                value={side}
                onChange={(e) => setSide(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-slate-900 focus:outline-none focus:border-indigo-500"
              >
                <option value="BUY">BUY (매수)</option>
                <option value="SELL">SELL (매도)</option>
              </select>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-slate-700 mb-1">종목명 (예: 삼성전자, BTC)</label>
              <input
                type="text"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value)}
                placeholder="예: 삼성전자"
                required
                className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-slate-900 focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-slate-700 mb-1">실전 손익률 (% )</label>
              <input
                type="number"
                step="0.1"
                value={pnl}
                onChange={(e) => setPnl(e.target.value)}
                placeholder="8.5"
                className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-slate-900 focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-slate-700 mb-1">체결 금액 (원)</label>
              <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="1000000"
                required
                className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-slate-900 focus:outline-none focus:border-indigo-500"
              />
            </div>
            <div>
              <label className="block text-slate-700 mb-1">체결 단가 (원)</label>
              <input
                type="number"
                step="0.1"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                placeholder="72000"
                required
                className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-slate-900 focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>
          <div>
            <label className="block text-slate-700 mb-1">💡 수립된 투자 전략 (Strategy)</label>
            <select
              value={strategy}
              onChange={(e) => setStrategy(e.target.value)}
              className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-slate-900 focus:outline-none focus:border-indigo-500"
            >
              <option value="💎 기업 실질가치 장기분석 전략">💎 기업 실질가치 장기분석 전략</option>
              <option value="⚡ 국내외 가격차이 라우팅 전략">⚡ 국내외 가격차이 라우팅 전략</option>
              <option value="🛡️ 손실 방어 분할매수 수칙 전략">🛡️ 손실 방어 분할매수 수칙 전략</option>
              <option value="🔮 정량 수치 기반 지표 전략">🔮 정량 수치 기반 지표 전략</option>
            </select>
          </div>
          <div>
            <label className="block text-slate-700 mb-1">🧠 AI 매수 근거</label>
            <textarea
              rows="2"
              value={reasoning}
              onChange={(e) => setReasoning(e.target.value)}
              placeholder="실적 영업이익 반등 및 수급 분석 완료..."
              required
              className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-slate-900 focus:outline-none focus:border-indigo-500"
            ></textarea>
          </div>
          <button type="submit" className="w-full bg-slate-900 hover:bg-slate-800 text-white font-black py-3 rounded-xl shadow-md text-sm">
            기록 완료하고 경험치 받기
          </button>
        </form>
      </div>
    </div>
  )
}
