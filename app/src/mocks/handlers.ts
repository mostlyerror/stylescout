import { rest } from 'msw'
import type { TikTokAuthResponse } from '@/types/tiktok'

export const handlers = [
  // Mock TikTok token exchange
  rest.post('https://open-api.tiktok.com/oauth/access_token/', async (req, res, ctx) => {
    const body = await req.text()
    const params = new URLSearchParams(body)
    const code = params.get('code')
    
    if (code === 'valid_code') {
      return res(
        ctx.json<TikTokAuthResponse>({
          access_token: 'mock_access_token',
          expires_in: 3600,
          refresh_token: 'mock_refresh_token',
          refresh_expires_in: 86400,
          open_id: 'mock_open_id',
          scope: 'user.info.basic,video.list,comment.create'
        })
      )
    }
    
    return res(
      ctx.status(400),
      ctx.json({ message: 'Invalid code' })
    )
  })
] 