import React, { useState } from 'react'

export default function FeedAndRankings({ feed, rankings }) {
  const [activeTab, setActiveTab] = useState('feed')

  return (
    <div className="white-navy-card p-5 rounded-3xl space-y-4 border border-slate-200">
      <div className="flex justify-between items-center border-b border-slate-100 pb-3 font-jua">
        <div className="flex items-center gap-4 text-xs font-bold">
          <button
            onClick={() => setActiveTab('feed')}
            className={activeTab === 'feed' ? 'text-indigo-900 border-b-2 border-indigo-900 pb-1' : 'text-slate-400 hover:text-slate-700 pb-1'}
          >
            📖 모임 식구 트레이딩 기록 피드
          </button>
          <button
            onClick={() => setActiveTab('rank')}
            className={activeTab === 'rank' ? 'text-indigo-900 border-b-2 border-indigo-900 pb-1' : 'text-slate-400 hover:text-slate-700 pb-1'}
          >
            🏆 모임 실전 손익률 랭킹
          </button>
        </div>
      </div>

      {activeTab === 'feed' ? (
        <div className="space-y-3">
          {(!feed || feed.length === 0) ? (
            <div className="text-center py-4 text-slate-400 text-xs font-jua">작성된 복기가 없습니다.</div>
          ) : (
            feed.map((item) => (
              <div key={item.id} className="p-3.5 bg-slate-50 rounded-2xl border border-slate-200 space-y-1.5 text-xs">
                <div className="flex justify-between items-center font-jua">
                  <div className="flex items-center gap-2">
                    <span className="bg-slate-900 text-white text-[10px] px-2 py-0.5 rounded-md font-bold">{item.asset_type || '📈 주식'}</span>
                    <span className="font-bold text-slate-900">{item.author}</span>
                    <span className="text-emerald-600 font-bold font-mono">+{item.pnl_rate}% PnL</span>
                  </div>
                  <span className="text-slate-400 text-[10px] font-mono">{item.time}</span>
                </div>
                <div className="text-indigo-950 font-jua text-sm">
                  🚀 <strong>{item.symbol}</strong> {item.amount_krw?.toLocaleString()}원 {item.side === 'BUY' ? '매수' : '매도'} ({item.price?.toLocaleString()}원)
                </div>
                <div className="text-slate-600 text-[11px] font-jua">💡 전략: {item.strategy}</div>
                <div className="text-slate-500 text-[11px] font-jua">{item.ai_reasoning}</div>
              </div>
            ))
          )}
        </div>
      ) : (
        <div className="space-y-3">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-100 text-slate-800 border-b border-slate-200 font-jua">
              <tr>
                <th className="py-2.5 px-3">순위</th>
                <th className="py-2.5 px-3">투자자</th>
                <th className="py-2.5 px-3">투자 스타일</th>
                <th className="py-2.5 px-3">실전 손익률</th>
                <th className="py-2.5 px-3">경험치</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700 font-mono">
              {rankings.map((item) => (
                <tr key={item.rank}>
                  <td className="py-2 px-3 font-bold text-amber-700 font-jua">{item.rank}위</td>
                  <td className="py-2 px-3 font-bold text-slate-900 font-jua">{item.name}</td>
                  <td className="py-2 px-3 text-indigo-900 font-jua">{item.archetype}</td>
                  <td className="py-2 px-3 text-emerald-600 font-mono font-bold">+{item.return_pct}%</td>
                  <td className="py-2 px-3 text-amber-700 font-mono">{item.xp?.toLocaleString()} EXP</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
