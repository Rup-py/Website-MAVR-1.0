import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../lib/api";
import { toast } from "sonner";
import { ArrowLeft, TrendingUp, TrendingDown, Activity, Dumbbell, Droplets, Flame } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

export default function Progression() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState(30);

  useEffect(() => {
    loadProgression();
  }, [period]);

  const loadProgression = async () => {
    try {
      const { data: progressData } = await api.getProgressionSummary(period);
      setData(progressData);
    } catch (error) {
      toast.error("Failed to load progression data");
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

  const weightData = data?.weight_history?.map(w => ({
    date: w.date,
    weight: w.value
  })) || [];

  const readinessData = data?.readiness_history?.map(r => ({
    date: r.date,
    score: r.score
  })) || [];

  return (
    <div className="min-h-screen bg-[#0A0A0A]">
      {/* Header */}
      <header className="glass-header sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link to="/dashboard" className="text-[#71717A] hover:text-white transition-colors">
              <ArrowLeft className="w-6 h-6" />
            </Link>
            <div>
              <p className="overline text-xs">Analytics</p>
              <h1 className="font-['Barlow_Condensed'] text-2xl font-bold uppercase tracking-tight text-white">
                Progression
              </h1>
            </div>
          </div>
          
          <div className="flex gap-2">
            {[7, 14, 30].map(p => (
              <button
                key={p}
                onClick={() => setPeriod(p)}
                className={`px-4 py-2 text-sm font-semibold transition-colors ${
                  period === p 
                    ? "bg-[#E50914] text-white" 
                    : "border border-[#262626] text-[#71717A] hover:text-white"
                }`}
              >
                {p}D
              </button>
            ))}
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Summary Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <StatCard
            icon={Activity}
            label="Check-ins"
            value={data?.checkins_completed || 0}
            subLabel={`of ${period} days`}
          />
          <StatCard
            icon={Dumbbell}
            label="Workout Rate"
            value={`${data?.workout_completion_rate || 0}%`}
            trend={data?.workout_completion_rate >= 80 ? "up" : "down"}
          />
          <StatCard
            icon={Flame}
            label="Protein Adherence"
            value={`${data?.protein_adherence_rate || 0}%`}
            trend={data?.protein_adherence_rate >= 80 ? "up" : "down"}
          />
          <StatCard
            icon={Droplets}
            label="Water Adherence"
            value={`${data?.water_adherence_rate || 0}%`}
            trend={data?.water_adherence_rate >= 80 ? "up" : "down"}
          />
        </div>

        {/* Weight Change */}
        {data?.weight_change_kg !== null && (
          <div className="mavr-card mb-8">
            <div className="flex items-center justify-between mb-4">
              <div>
                <p className="text-[#71717A] text-xs uppercase tracking-widest mb-1">Weight Change</p>
                <div className="flex items-center gap-2">
                  <span className={`font-['Barlow_Condensed'] text-4xl font-black ${
                    data.weight_change_kg < 0 ? "text-[#10B981]" : 
                    data.weight_change_kg > 0 ? "text-[#E50914]" : "text-white"
                  }`}>
                    {data.weight_change_kg > 0 ? "+" : ""}{data.weight_change_kg} kg
                  </span>
                  {data.weight_change_kg !== 0 && (
                    data.weight_change_kg < 0 ? 
                      <TrendingDown className="w-6 h-6 text-[#10B981]" /> :
                      <TrendingUp className="w-6 h-6 text-[#E50914]" />
                  )}
                </div>
              </div>
              <p className="text-[#71717A] text-sm">Last {period} days</p>
            </div>

            {weightData.length > 1 && (
              <div className="h-48">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={weightData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#262626" />
                    <XAxis 
                      dataKey="date" 
                      stroke="#71717A"
                      tick={{ fontSize: 10 }}
                      tickFormatter={(v) => v.slice(5)}
                    />
                    <YAxis 
                      stroke="#71717A"
                      domain={['dataMin - 1', 'dataMax + 1']}
                      tick={{ fontSize: 10 }}
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#121212',
                        border: '1px solid #262626',
                        borderRadius: 0,
                      }}
                      labelStyle={{ color: '#71717A' }}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="weight" 
                      stroke="#E50914" 
                      strokeWidth={2}
                      dot={{ fill: '#E50914', strokeWidth: 0 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        )}

        {/* Readiness Trend */}
        <div className="mavr-card mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <p className="text-[#71717A] text-xs uppercase tracking-widest mb-1">Readiness Trend</p>
              <p className="font-['Barlow_Condensed'] text-2xl font-bold text-white">
                Average: {data?.average_readiness || 0}/100
              </p>
            </div>
          </div>

          {readinessData.length > 1 && (
            <div className="h-48">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={readinessData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#262626" />
                  <XAxis 
                    dataKey="date" 
                    stroke="#71717A"
                    tick={{ fontSize: 10 }}
                    tickFormatter={(v) => v.slice(5)}
                  />
                  <YAxis 
                    stroke="#71717A"
                    domain={[0, 100]}
                    tick={{ fontSize: 10 }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#121212',
                      border: '1px solid #262626',
                      borderRadius: 0,
                    }}
                    labelStyle={{ color: '#71717A' }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="score" 
                    stroke="#10B981" 
                    strokeWidth={2}
                    dot={{ fill: '#10B981', strokeWidth: 0 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

        {/* Adherence Breakdown */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <AdherenceCard
            label="Workout Completion"
            value={data?.workout_completion_rate || 0}
            color="#E50914"
          />
          <AdherenceCard
            label="Protein Target"
            value={data?.protein_adherence_rate || 0}
            color="#F59E0B"
          />
          <AdherenceCard
            label="Hydration"
            value={data?.water_adherence_rate || 0}
            color="#10B981"
          />
        </div>
      </main>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, subLabel, trend }) {
  return (
    <div className="mavr-card">
      <div className="flex items-center gap-3 mb-3">
        <Icon className="w-5 h-5 text-[#E50914]" />
        <p className="text-[#71717A] text-xs uppercase tracking-widest">{label}</p>
      </div>
      <div className="flex items-baseline gap-2">
        <span className="font-['Barlow_Condensed'] text-3xl font-black text-white">{value}</span>
        {trend === "up" && <TrendingUp className="w-4 h-4 text-[#10B981]" />}
        {trend === "down" && <TrendingDown className="w-4 h-4 text-[#E50914]" />}
      </div>
      {subLabel && <p className="text-[#71717A] text-xs mt-1">{subLabel}</p>}
    </div>
  );
}

function AdherenceCard({ label, value, color }) {
  return (
    <div className="mavr-card">
      <p className="text-[#71717A] text-xs uppercase tracking-widest mb-3">{label}</p>
      <div className="flex items-center gap-4">
        <div className="flex-1 h-2 bg-[#262626]">
          <div 
            className="h-full transition-all duration-500"
            style={{ width: `${value}%`, backgroundColor: color }}
          ></div>
        </div>
        <span className="font-['JetBrains_Mono'] text-white font-bold">{value}%</span>
      </div>
    </div>
  );
}
