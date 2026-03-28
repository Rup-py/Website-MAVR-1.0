import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../lib/api";
import { toast } from "sonner";
import { ArrowLeft, Users, Activity, TrendingUp, Calendar, ChevronRight } from "lucide-react";

export default function Admin() {
  const [analytics, setAnalytics] = useState(null);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("overview");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [analyticsRes, usersRes] = await Promise.all([
        api.adminGetAnalytics(),
        api.adminGetUsers(0, 20)
      ]);
      setAnalytics(analyticsRes.data);
      setUsers(usersRes.data.users);
    } catch (error) {
      toast.error("Failed to load admin data");
      console.error(error);
    }
    setLoading(false);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0A0A0A] flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-[#E50914] border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0A0A0A]">
      {/* Header */}
      <header className="glass-header sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/dashboard" className="text-[#71717A] hover:text-white transition-colors">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <div>
            <p className="overline text-xs">Admin</p>
            <h1 className="font-['Barlow_Condensed'] text-2xl font-bold uppercase tracking-tight text-white">
              Control Panel
            </h1>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Tabs */}
        <div className="flex gap-1 mb-8 border-b border-[#262626]">
          {["overview", "users"].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-6 py-3 font-['Barlow_Condensed'] font-bold uppercase tracking-widest transition-colors ${
                activeTab === tab 
                  ? "text-white border-b-2 border-[#E50914]" 
                  : "text-[#71717A] hover:text-white"
              }`}
              data-testid={`tab-${tab}`}
            >
              {tab}
            </button>
          ))}
        </div>

        {activeTab === "overview" && (
          <>
            {/* Analytics Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <StatCard
                icon={Users}
                label="Total Users"
                value={analytics?.total_users || 0}
              />
              <StatCard
                icon={Activity}
                label="Onboarded"
                value={analytics?.onboarded_users || 0}
                subLabel={`${analytics?.onboarding_rate || 0}% rate`}
              />
              <StatCard
                icon={TrendingUp}
                label="Active Today"
                value={analytics?.active_today || 0}
              />
              <StatCard
                icon={Calendar}
                label="Active Events"
                value={analytics?.active_events || 0}
              />
            </div>

            {/* Athlete Level Distribution */}
            <div className="mavr-card mb-8">
              <p className="text-[#71717A] text-xs uppercase tracking-widest mb-4">
                Athlete Level Distribution
              </p>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(analytics?.athlete_level_distribution || {}).map(([level, count]) => (
                  <div key={level} className="text-center p-4 border border-[#262626]">
                    <p className="font-['Barlow_Condensed'] text-3xl font-black text-white">{count}</p>
                    <p className="text-[#71717A] text-sm capitalize">{level}</p>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}

        {activeTab === "users" && (
          <div className="mavr-card">
            <div className="flex items-center justify-between mb-4">
              <p className="text-[#71717A] text-xs uppercase tracking-widest">Recent Users</p>
              <p className="text-[#71717A] text-sm">{users.length} shown</p>
            </div>
            
            <div className="space-y-2">
              {users.map(user => (
                <div 
                  key={user._id}
                  className="flex items-center justify-between p-4 border border-[#262626] hover:border-[#333] transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 bg-[#262626] rounded-full flex items-center justify-center">
                      <span className="text-white font-bold">
                        {user.name?.charAt(0)?.toUpperCase() || "?"}
                      </span>
                    </div>
                    <div>
                      <p className="text-white font-semibold">{user.name}</p>
                      <p className="text-[#71717A] text-sm">{user.email}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <span className={`px-2 py-1 text-xs font-bold uppercase ${
                      user.role === "admin" 
                        ? "bg-[#E50914]/20 text-[#E50914]" 
                        : "bg-[#262626] text-[#71717A]"
                    }`}>
                      {user.role}
                    </span>
                    <span className={`px-2 py-1 text-xs ${
                      user.onboarding_completed 
                        ? "bg-[#10B981]/20 text-[#10B981]" 
                        : "bg-[#F59E0B]/20 text-[#F59E0B]"
                    }`}>
                      {user.onboarding_completed ? "Onboarded" : "Pending"}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, subLabel }) {
  return (
    <div className="mavr-card">
      <div className="flex items-center gap-3 mb-3">
        <Icon className="w-5 h-5 text-[#E50914]" />
        <p className="text-[#71717A] text-xs uppercase tracking-widest">{label}</p>
      </div>
      <p className="font-['Barlow_Condensed'] text-3xl font-black text-white">{value}</p>
      {subLabel && <p className="text-[#71717A] text-xs mt-1">{subLabel}</p>}
    </div>
  );
}
