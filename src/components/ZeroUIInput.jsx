import React, { useState } from 'react'
import { Send, Edit3 } from 'lucide-react'

export default function ZeroUIInput({ onSendPrompt, onOpenJournalModal }) {
  const [promptText, setPromptText] = useState('')
  const [selectedAsset, setSelectedAsset] = useState('📈 주식')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!promptText.trim()) return
    onSendPrompt(promptText, selectedAsset)
    setPromptText('')
  }

  const fillPrompt = (text) => {
    setPromptText(text)
  }

  return (
    <div className="white-navy-card p-4 rounded-3xl prompt-navy-shadow relative border-2 border-indigo-200 space-y-3">
      {/* Asset Class Selector Chips */}
      <div className="flex items-center gap-2 font-jua text-xs border-b border-slate-100 pb-2.5">
        <span className="text-slate-400 font-bold">🎯 투자군:</span>
        <button
          type="button"
          onClick={() => setSelectedAsset('📈 주식')}
          className={selectedAsset === '📈 주식' ? 'bg-indigo-900 text-white px-3 py-1 rounded-xl font-bold transition' : 'bg-slate-100 text-slate-700 hover:bg-slate-200 px-3 py-1 rounded-xl font-bold transition'}
        >
          📈 주식 (국장/해외)
        </button>
        <button
          type="button"
          onClick={() => setSelectedAsset('🪙 코인')}
          className={selectedAsset === '🪙 코인' ? 'bg-indigo-900 text-white px-3 py-1 rounded-xl font-bold transition' : 'bg-slate-100 text-slate-700 hover:bg-slate-200 px-3 py-1 rounded-xl font-bold transition'}
        >
          🪙 코인 (가상자산)
        </button>

        <button
          onClick={onOpenJournalModal}
          className="ml-auto bg-slate-900 text-white px-3 py-1 rounded-xl font-bold hover:bg-slate-800 transition text-[11px] flex items-center gap-1"
        >
          <Edit3 className="w-3 h-3" />
          <span>상세 매매 기록</span>
        </button>
      </div>

      {/* Single Prompt Input Form */}
      <form onSubmit={handleSubmit} className="flex items-center gap-2">
        <input
          type="text"
          value={promptText}
          onChange={(e) => setPromptText(e.target.value)}
          placeholder="예: '오늘 삼성전자 10만원 매수했어' 또는 'BTC 5만원 매수'..."
          required
          className="w-full bg-slate-50 text-slate-900 placeholder-slate-400 text-sm px-5 py-3.5 rounded-2xl focus:outline-none focus:ring-2 focus:ring-indigo-500 border border-slate-200 font-jua"
        />
        <button
          type="submit"
          className="bg-gradient-to-r from-slate-900 via-indigo-900 to-slate-900 hover:from-slate-800 hover:to-indigo-800 text-white font-black px-6 py-3.5 rounded-2xl transition font-jua text-sm flex items-center gap-1.5 shrink-0 shadow-md active:scale-95"
        >
          <span>기록</span>
          <Send className="w-3.5 h-3.5" />
        </button>
      </form>

      {/* Quick Nudge Chips */}
      <div className="flex flex-wrap gap-2 px-1 text-xs font-jua">
        <span className="text-slate-400 text-[11px] flex items-center">💡 빠른 입력:</span>
        <button
          type="button"
          onClick={() => fillPrompt('오늘 삼성전자 100만원 매수했어')}
          className="bg-slate-100 hover:bg-slate-200 text-slate-800 px-3 py-1 rounded-xl border border-slate-200 text-[11px] transition"
        >
          📈 "오늘 삼성전자 100만원 매수했어"
        </button>
        <button
          type="button"
          onClick={() => fillPrompt('오늘 비트코인 50만원 매수했어')}
          className="bg-slate-100 hover:bg-slate-200 text-slate-800 px-3 py-1 rounded-xl border border-slate-200 text-[11px] transition"
        >
          🪙 "오늘 BTC 50만원 매수했어"
        </button>
        <button
          type="button"
          onClick={() => fillPrompt('우리 모임 순위 보여줘')}
          className="bg-amber-50 hover:bg-amber-100 text-amber-900 px-3 py-1 rounded-xl border border-amber-200 text-[11px] transition"
        >
          🏆 "모임 순위 보기"
        </button>
      </div>
    </div>
  )
}
