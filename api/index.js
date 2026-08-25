// Node.js Vercel Serverless Function for 같이투자 (Gachi Tuza)
export default async function handler(req, res) {
  const { url, method } = req

  // Set CORS Headers
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type')

  if (method === 'OPTIONS') {
    return res.status(200).end()
  }

  // 1. Natural Language Zero UI Chat Processing
  if (url.includes('/api/chat') && method === 'POST') {
    const { prompt, user_id } = req.body || {}
    const promptText = (prompt || '').trim()

    const isBuy = promptText.includes('매수') || promptText.includes('샀')
    const side = isBuy ? 'BUY' : 'SELL'
    const symbol = promptText.includes('삼성') ? '삼성전자' : promptText.includes('비트') ? 'BTC' : 'SOL'
    const asset_type = (promptText.includes('주식') || promptText.includes('삼성')) ? '📈 주식' : '🪙 코인'

    return res.status(200).json({
      type: 'trade_created',
      reply: `🌱 **투자자**님, [${asset_type}] '${symbol} ${side}' 매매 복기가 R3F 정원에 성공적으로 기록되었습니다!\n✨ **+150 경험치(EXP)** 획득!`,
      new_xp: 2600
    })
  }

  // 2. User info endpoint
  if (url.includes('/api/user/me')) {
    return res.status(200).json({
      id: 1,
      nickname: '김가치 (모임장)',
      provider: 'kakao',
      archetype: '💎 기업 실질가치 투자자',
      title: '👑 가치투자 1기 모임장',
      xp: 2450
    })
  }

  // 3. Social feed endpoint
  if (url.includes('/api/feed')) {
    return res.status(200).json([
      {
        id: 1,
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
        id: 2,
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
  }

  // 4. Squad Rankings
  if (url.includes('/api/squad/rankings')) {
    return res.status(200).json([
      { rank: 1, name: '김가치', archetype: '💎 기업 실질가치 투자자', return_pct: 14.8, xp: 2450 },
      { rank: 2, name: '박비트', archetype: '🛡️ 위험 방어 수호자', return_pct: 11.2, xp: 1980 },
      { rank: 3, name: '최솔라', archetype: '⚡ 가격차이 차익 투자자', return_pct: 7.6, xp: 1620 }
    ])
  }

  return res.status(200).json({ status: 'ok', message: '같이투자 Node.js R3F API Server Running' })
}
