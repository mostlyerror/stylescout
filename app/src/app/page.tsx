import Image from "next/image";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-8">TikTok Fashion Scout</h1>
      <p className="text-xl mb-8">Discover and share fashion trends on TikTok</p>
      <a
        href="/api/auth"
        className="bg-black text-white px-6 py-3 rounded-lg hover:bg-gray-800 transition-colors"
      >
        Login with TikTok
      </a>
    </main>
  );
}
