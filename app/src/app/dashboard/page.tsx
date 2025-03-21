import { getAccessToken } from '@/lib/auth';
import { redirect } from 'next/navigation';

export default async function Dashboard() {
  const token = await getAccessToken();

  if (!token) {
    redirect('/');
  }

  return (
    <main className="min-h-screen p-8">
      <h1 className="text-3xl font-bold mb-8">Your Fashion Scout Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Add your dashboard content here */}
        <div className="p-6 bg-white rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
          <p>Your recent fashion discoveries will appear here.</p>
        </div>
      </div>
    </main>
  );
} 