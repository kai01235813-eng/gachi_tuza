// 같이투자 (Gachi Tuza) - Vercel Serverless API
// 업비트 Open API 프록시: 브라우저에서 직접 호출하면 CORS로 막히므로
// 이 함수가 JWT 서명 + 중계를 담당한다. (조회 전용 - 주문/출금 기능 없음)
import crypto from 'crypto'

const UPBIT = 'https://api.upbit.com'

const b64url = (buf) => Buffer.from(buf).toString('base64').replace(/=+$/, '').replace(/\+/g, '-').replace(/\//g, '_')

// 업비트 인증 JWT (HS256). 쿼리가 있으면 SHA512 query_hash를 포함해야 한다.
function upbitToken(accessKey, secretKey, query) {
  const payload = { access_key: accessKey, nonce: crypto.randomUUID() }
  if (query) {
    payload.query_hash = crypto.createHash('sha512').update(query, 'utf-8').digest('hex')
    payload.query_hash_alg = 'SHA512'
  }
  const header = b64url(JSON.stringify({ alg: 'HS256', typ: 'JWT' }))
  const body = b64url(JSON.stringify(payload))
  const sig = b64url(crypto.createHmac('sha256', secretKey).update(`${header}.${body}`).digest())
  return `${header}.${body}.${sig}`
}

async function proxyUpbit(res, path, query, token) {
  const headers = { Accept: 'application/json' }
  if (token) headers.Authorization = `Bearer ${token}`
  const upstream = await fetch(`${UPBIT}${path}${query ? `?${query}` : ''}`, { headers })
  const data = await upstream.json().catch(() => ({ error: { message: '업비트 응답을 해석하지 못했어요.' } }))
  return res.status(upstream.status).json(data)
}

export default async function handler(req, res) {
  const { url, method } = req

  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type')
  if (method === 'OPTIONS') return res.status(200).end()

  try {
    // ---------- 업비트 프록시 ----------
    // 공개 시세 (인증 불필요) - 시장 온도계 / 잔고 평가용
    if (url.includes('/api/upbit/ticker')) {
      const markets = String((req.query && req.query.markets) || '').replace(/[^A-Z0-9\-,]/g, '')
      if (!markets) return res.status(400).json({ error: { message: 'markets 파라미터가 필요해요.' } })
      return await proxyUpbit(res, '/v1/ticker', `markets=${markets}`)
    }

    // 전체 계좌(잔고) 조회 - 자산조회 권한 필요
    if (url.includes('/api/upbit/accounts') && method === 'POST') {
      const { accessKey, secretKey } = req.body || {}
      if (!accessKey || !secretKey) return res.status(400).json({ error: { message: 'API 키를 입력해주세요.' } })
      return await proxyUpbit(res, '/v1/accounts', '', upbitToken(accessKey, secretKey, null))
    }

    // 종료된 주문(체결내역) 조회 - 주문조회 권한 필요
    if (url.includes('/api/upbit/orders') && method === 'POST') {
      const { accessKey, secretKey, market } = req.body || {}
      if (!accessKey || !secretKey) return res.status(400).json({ error: { message: 'API 키를 입력해주세요.' } })
      const params = new URLSearchParams({ limit: '100', order_by: 'desc' })
      if (market) params.set('market', String(market))
      const query = params.toString()
      return await proxyUpbit(res, '/v1/orders/closed', query, upbitToken(accessKey, secretKey, query))
    }
  } catch (e) {
    return res.status(500).json({ error: { message: e.message || '프록시 처리 중 오류가 발생했어요.' } })
  }

  return res.status(200).json({ status: 'ok', message: '같이투자 포춘빌리지 API 서버 작동 중 🏡' })
}
