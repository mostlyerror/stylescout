import { GET } from '../route'
import { cookies } from 'next/headers'
import { NextRequest } from 'next/server'

jest.mock('next/headers', () => ({
  cookies: jest.fn()
}))

const BASE_URL = 'http://localhost:3000'

describe('Auth Callback Route', () => {
  const mockCookieStore = {
    get: jest.fn(),
    set: jest.fn(),
    delete: jest.fn()
  }

  beforeEach(() => {
    jest.clearAllMocks()
    ;(cookies as jest.Mock).mockReturnValue(mockCookieStore)
  })

  it('redirects to error page when state is invalid', async () => {
    mockCookieStore.get.mockReturnValue({ value: 'stored_state' })
    
    const request = new NextRequest(
      new URL('http://localhost:3000/auth/callback?state=different_state&code=test_code')
    )

    const response = await GET(request)
    expect(response.status).toBe(307)
    expect(response.headers.get('Location')).toBe(`${BASE_URL}/auth-error?error=invalid_state`)
  })

  it('redirects to error page when code is missing', async () => {
    mockCookieStore.get.mockReturnValue({ value: 'test_state' })
    
    const request = new NextRequest(
      new URL('http://localhost:3000/auth/callback?state=test_state')
    )

    const response = await GET(request)
    expect(response.status).toBe(307)
    expect(response.headers.get('Location')).toBe(`${BASE_URL}/auth-error?error=no_code`)
  })

  it('successfully handles valid callback and sets token cookie', async () => {
    mockCookieStore.get.mockReturnValue({ value: 'test_state' })
    
    const request = new NextRequest(
      new URL('http://localhost:3000/auth/callback?state=test_state&code=valid_code')
    )

    const response = await GET(request)
    
    expect(mockCookieStore.set).toHaveBeenCalledWith(
      'tiktok_token',
      'mock_access_token',
      expect.objectContaining({
        httpOnly: true
      })
    )
    expect(mockCookieStore.delete).toHaveBeenCalledWith('oauth_state')
    expect(response.status).toBe(307)
    expect(response.headers.get('Location')).toBe(`${BASE_URL}/dashboard`)
  })

  it('redirects to error page when token exchange fails', async () => {
    mockCookieStore.get.mockReturnValue({ value: 'test_state' })
    
    const request = new NextRequest(
      new URL('http://localhost:3000/auth/callback?state=test_state&code=invalid_code')
    )

    const response = await GET(request)
    expect(response.status).toBe(307)
    expect(response.headers.get('Location')).toBe(`${BASE_URL}/auth-error?error=token_exchange`)
  })
}) 