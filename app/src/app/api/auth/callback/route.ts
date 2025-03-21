import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import { exchangeCodeForToken } from '@/lib/auth';
import type { TikTokAuthResponse } from '@/types/tiktok';

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const code = searchParams.get('code');
  const state = searchParams.get('state');
  const cookieStore = await cookies();
  const storedState = cookieStore.get('oauth_state')?.value;

  // Verify state to prevent CSRF attacks
  if (!state || !storedState || state !== storedState) {
    return NextResponse.redirect('/auth-error?error=invalid_state');
  }

  if (!code) {
    return NextResponse.redirect('/auth-error?error=no_code');
  }

  try {
    const tokenData = await exchangeCodeForToken(code) as TikTokAuthResponse;
    
    // Store the access token in an HTTP-only cookie
    cookieStore.set('tiktok_token', tokenData.access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: tokenData.expires_in
    });

    // Clear the state cookie
    cookieStore.delete('oauth_state');

    return NextResponse.redirect('/dashboard');
  } catch (error) {
    console.error('Auth error:', error);
    return NextResponse.redirect('/auth-error?error=token_exchange');
  }
} 