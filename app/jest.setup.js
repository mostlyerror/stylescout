import '@testing-library/jest-dom'
import { server } from './src/mocks/server'
import fetch, { Request, Response } from 'node-fetch'

// Polyfill for Next.js testing environment
global.Request = Request
global.Response = Response
global.fetch = fetch

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => server.resetHandlers())
afterAll(() => server.close()) 