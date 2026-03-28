import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import api from "../lib/api";
import { toast } from "sonner";
import { ArrowLeft, User, Target, Activity, Dumbbell } from "lucide-react";

export default function Profile() {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const { data } = await api.getProfile();
      setProfile(data);
    } catch (error) {
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

  const profileData = profile?.profile_data || {};

  return (
    <div className="min-h-screen bg-[#0A0A0A]">
      {/* Header */}
      <header className="glass-header sticky top-0 z-40">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/dashboard" className="text-[#71717A] hover:text-white transition-colors">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <div>
            <p className="overline text-xs">Settings</p>
            <h1 className="font-['Barlow_Condensed'] text-2xl font-bold uppercase tracking-tight text-white">
              Profile
            </h1>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* User Info */}
        <div className="mavr-card mb-6">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-16 h-16 bg-[#262626] rounded-full flex items-center justify-center">
              <User className="w-8 h-8 text-[#71717A]" />
            </div>
            <div>
              <h2 className="font-['Barlow_Condensed'] text-2xl font-bold text-white">{user?.name}</h2>
              <p className="text-[#71717A]">{user?.email}</p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <span className={`px-3 py-1 text-xs font-bold uppercase tracking-widest ${
              user?.role === "admin" 
                ? "bg-[#E50914]/20 text-[#E50914]" 
                : "bg-[#262626] text-[#71717A]"
            }`}>
              {user?.role}
            </span>
            <span className="px-3 py-1 bg-[#10B981]/20 text-[#10B981] text-xs font-bold uppercase tracking-widest">
              {profile?.athlete_level || "Athlete"}
            </span>
          </div>
        </div>

        {/* Body Metrics */}
        <div className="mavr-card mb-6">
          <p className="text-[#71717A] text-xs uppercase tracking-widest mb-4">Body Metrics</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <MetricItem label="Age" value={profileData.age} unit="years" />
            <MetricItem label="Height" value={profileData.height_cm} unit="cm" />
            <MetricItem label="Weight" value={profileData.weight_kg} unit="kg" />
            <MetricItem label="Target" value={profileData.target_weight_kg} unit="kg" />
          </div>
        </div>

        {/* Targets */}
        <div className="mavr-card mb-6">
          <p className="text-[#71717A] text-xs uppercase tracking-widest mb-4">Daily Targets</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <MetricItem label="Calories" value={profile?.target_calories} unit="kcal" primary />
            <MetricItem label="Protein" value={profile?.target_protein} unit="g" />
            <MetricItem label="Carbs" value={profile?.target_carbs} unit="g" />
            <MetricItem label="Fats" value={profile?.target_fats} unit="g" />
          </div>
        </div>

        {/* Training Preferences */}
        <div className="mavr-card mb-6">
          <p className="text-[#71717A] text-xs uppercase tracking-widest mb-4">Training</p>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-[#71717A] text-sm">Goal</p>
              <p className="text-white capitalize">{profileData.goal?.replace('_', ' ') || "Not set"}</p>
            </div>
            <div>
              <p className="text-[#71717A] text-sm">Training Age</p>
              <p className="text-white">{profileData.training_age_months || 0} months</p>
            </div>
            <div>
              <p className="text-[#71717A] text-sm">Frequency</p>
              <p className="text-white">{profileData.workout_frequency || 0} days/week</p>
            </div>
            <div>
              <p className="text-[#71717A] text-sm">Setup</p>
              <p className="text-white capitalize">{profileData.workout_setup || "Not set"}</p>
            </div>
          </div>
          
          {profileData.preferred_workout_days?.length > 0 && (
            <div className="mt-4">
              <p className="text-[#71717A] text-sm mb-2">Workout Days</p>
              <div className="flex flex-wrap gap-2">
                {profileData.preferred_workout_days.map(day => (
                  <span key={day} className="px-3 py-1 bg-[#262626] text-white text-sm capitalize">
                    {day}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Diet Preferences */}
        <div className="mavr-card">
          <p className="text-[#71717A] text-xs uppercase tracking-widest mb-4">Diet</p>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-[#71717A] text-sm">Preference</p>
              <p className="text-white capitalize">{profileData.diet_preference?.replace('_', ' ') || "Not set"}</p>
            </div>
            <div>
              <p className="text-[#71717A] text-sm">Budget</p>
              <p className="text-white capitalize">{profileData.budget_level || "Not set"}</p>
            </div>
            <div>
              <p className="text-[#71717A] text-sm">Meals/Day</p>
              <p className="text-white">{profileData.meal_frequency || 4}</p>
            </div>
            <div>
              <p className="text-[#71717A] text-sm">Activity Level</p>
              <p className="text-white capitalize">{profileData.activity_level?.replace('_', ' ') || "Not set"}</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function MetricItem({ label, value, unit, primary }) {
  return (
    <div className={`text-center p-4 border ${primary ? 'border-[#E50914]/30 bg-[#E50914]/5' : 'border-[#262626]'}`}>
      <p className={`font-['Barlow_Condensed'] text-2xl font-bold ${primary ? 'text-[#E50914]' : 'text-white'}`}>
        {value || "--"}
      </p>
      <p className="text-[#71717A] text-xs">{unit}</p>
      <p className="text-[#A1A1AA] text-xs mt-1">{label}</p>
    </div>
  );
}
