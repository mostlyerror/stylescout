import { NextResponse } from 'next/server';
import { generateAuthUrl } from '@/lib/auth';
import { cookies } from 'next/headers';
import crypto from 'crypto';

export async function GET() {
  // Generate a random state for CSRF protection
  const state = crypto.randomBytes(32).toString('hex');
  
  // Store state in a cookie for verification in callback
  const cookieStore = await cookies();
  cookieStore.set('oauth_state', state, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 3600 // 1 hour
  });

  // Generate auth URL and redirect
  const authUrl = generateAuthUrl(state);
  return NextResponse.redirect(authUrl);
} 