import { GET } from '../route'
import { cookies } from 'next/headers'
import { NextResponse } from 'next/server'

jest.mock('next/headers', () => ({
  cookies: jest.fn()
}))

jest.mock('crypto', () => ({
  randomBytes: () => ({
    toString: () => 'mock_state'
  })
}))

describe('Auth Route', () => {
  it('sets oauth state cookie and redirects to TikTok auth URL', async () => {
    const mockCookieStore = {
      set: jest.fn()
    }
    ;(cookies as jest.Mock).mockReturnValue(mockCookieStore)

    const response = await GET()
    const redirectUrl = response.headers.get('Location')

    expect(mockCookieStore.set).toHaveBeenCalledWith(
      'oauth_state',
      'mock_state',
      expect.objectContaining({
        httpOnly: true,
        maxAge: 3600
      })
    )

    expect(redirectUrl).toContain('https://www.tiktok.com/auth/authorize')
    expect(redirectUrl).toContain('state=mock_state')
    expect(response instanceof NextResponse).toBe(true)
  })
}) 