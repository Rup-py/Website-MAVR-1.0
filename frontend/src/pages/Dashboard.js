import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import api from "../lib/api";
import { toast } from "sonner";
import { 
  Activity, Dumbbell, Utensils, TrendingUp, Calendar, 
  CheckSquare, Flame, Droplets, Footprints, Moon, Sun, 
  ChevronRight, LogOut, User, LayoutDashboard, BarChart3,
  Settings, ShieldCheck
} from "lucide-react";
import { Progress } from "../components/ui/progress";

export default function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const { data: dashboardData } = await api.getDashboard();
      setData(dashboardData);
    } catch (error) {
      toast.error("Failed to load dashboard");
      console.error(error);
    }
    setLoading(false);
  };

  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0A0A0A] flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-[#E50914] border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-[#71717A] text-sm uppercase tracking-widest">Loading Dashboard</p>
        </div>
      </div>
    );
  }

  const checklist = data?.checklist || {};
  const streak = data?.streak || {};
  const readiness = data?.readiness || {};
  const dietPlan = data?.diet_plan || {};
  const workoutPlan = data?.workout_plan || {};
  const profile = data?.profile || {};

  // Calculate checklist completion
  const checklistItems = Object.values(checklist);
  const completedItems = checklistItems.filter(Boolean).length;
  const totalItems = checklistItems.length;
  const completionPercent = totalItems > 0 ? (completedItems / totalItems) * 100 : 0;

  return (
    <div className="min-h-screen bg-[#0A0A0A]">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 bottom-0 w-64 bg-[#121212] border-r border-[#262626] z-50 hidden lg:flex flex-col">
        <div className="p-6 border-b border-[#262626]">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-[#E50914] flex items-center justify-center">
              <span className="font-['Barlow_Condensed'] font-black text-white text-lg">M</span>
            </div>
            <span className="font-['Barlow_Condensed'] font-bold text-xl tracking-tight text-white">MAVR</span>
          </Link>
        </div>

        <nav className="flex-1 p-4">
          <ul className="space-y-1">
            {[
              { icon: LayoutDashboard, label: "Dashboard", path: "/dashboard", active: true },
              { icon: Utensils, label: "Diet Plan", path: "/diet" },
              { icon: Dumbbell, label: "Workout", path: "/workout" },
              { icon: CheckSquare, label: "Check-in", path: "/checkin" },
              { icon: BarChart3, label: "Progression", path: "/progression" },
              { icon: Calendar, label: "Event Mode", path: "/event" },
            ].map(item => (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`flex items-center gap-3 px-4 py-3 transition-colors ${
                    item.active 
                      ? "bg-[#E50914]/10 text-white border-l-2 border-[#E50914]" 
                      : "text-[#71717A] hover:text-white hover:bg-[#1A1A1A]"
                  }`}
                  data-testid={`nav-${item.label.toLowerCase().replace(' ', '-')}`}
                >
                  <item.icon className="w-5 h-5" />
                  <span className="font-medium">{item.label}</span>
                </Link>
              </li>
            ))}
          </ul>

          {user?.role === "admin" && (
            <div className="mt-6 pt-6 border-t border-[#262626]">
              <p className="px-4 text-xs text-[#71717A] uppercase tracking-widest mb-2">Admin</p>
              <Link
                to="/admin"
                className="flex items-center gap-3 px-4 py-3 text-[#71717A] hover:text-white hover:bg-[#1A1A1A] transition-colors"
                data-testid="nav-admin"
              >
                <ShieldCheck className="w-5 h-5" />
                <span className="font-medium">Admin Panel</span>
              </Link>
            </div>
          )}
        </nav>

        <div className="p-4 border-t border-[#262626]">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-[#262626] rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-[#71717A]" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-white font-medium truncate">{user?.name}</p>
              <p className="text-[#71717A] text-xs uppercase tracking-widest">
                {profile?.athlete_level || "Athlete"}
              </p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 w-full px-4 py-2 text-[#71717A] hover:text-white hover:bg-[#1A1A1A] transition-colors"
            data-testid="logout-btn"
          >
            <LogOut className="w-4 h-4" />
            <span className="text-sm">Sign Out</span>
          </button>
        </div>
      </aside>

      {/* Mobile Header */}
      <header className="lg:hidden glass-header fixed top-0 left-0 right-0 z-40">
        <div className="px-4 py-3 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-[#E50914] flex items-center justify-center">
              <span className="font-['Barlow_Condensed'] font-black text-white text-lg">M</span>
            </div>
          </Link>
          <div className="flex items-center gap-4">
            <Link to="/checkin" className="text-[#71717A] hover:text-white">
              <CheckSquare className="w-6 h-6" />
            </Link>
            <button onClick={handleLogout} className="text-[#71717A] hover:text-white">
              <LogOut className="w-6 h-6" />
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="lg:ml-64 min-h-screen pt-16 lg:pt-0">
        <div className="p-4 lg:p-8">
          {/* Header */}
          <div className="mb-8">
            <p className="overline mb-2">{data?.date}</p>
            <h1 className="font-['Barlow_Condensed'] text-3xl lg:text-4xl font-bold uppercase tracking-tight text-white">
              {getGreeting()}, {user?.name?.split(' ')[0]}
            </h1>
            <p className="text-[#A1A1AA] mt-2">Your system is ready. Today decides the week.</p>
          </div>

          {/* Dashboard Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Readiness Score - Large */}
            <div className="md:col-span-2 mavr-card" data-testid="readiness-card">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <p className="text-[#71717A] text-xs uppercase tracking-widest mb-1">Readiness Score</p>
                  <div className="flex items-baseline gap-2">
                    <span className="font-['Barlow_Condensed'] text-5xl font-black text-white">
                      {readiness?.score || "--"}
                    </span>
                    <span className="text-[#71717A]">/100</span>
                  </div>
                </div>
                <div className={`px-3 py-1 text-xs font-bold uppercase tracking-widest ${
                  readiness?.level === "push" ? "bg-[#10B981]/20 text-[#10B981]" :
                  readiness?.level === "maintain" ? "bg-[#F59E0B]/20 text-[#F59E0B]" :
                  "bg-[#E50914]/20 text-[#E50914]"
                }`}>
                  {readiness?.level || "Check In"}
                </div>
              </div>
              <p className="text-[#A1A1AA] text-sm mb-4">{readiness?.recommendation || "Complete your morning check-in to get your readiness score."}</p>
              {!checklist.morning_checkin && (
                <Link 
                  to="/checkin/morning" 
                  className="inline-flex items-center gap-2 text-[#E50914] hover:underline text-sm font-semibold"
                >
                  Start Morning Check-in <ChevronRight className="w-4 h-4" />
                </Link>
              )}
            </div>

            {/* Streak */}
            <div className="mavr-card" data-testid="streak-card">
              <div className="flex items-center gap-3 mb-4">
                <Flame className="w-8 h-8 text-[#E50914]" />
                <div>
                  <p className="text-[#71717A] text-xs uppercase tracking-widest">Streak</p>
                  <p className="font-['Barlow_Condensed'] text-3xl font-black text-white">
                    {streak?.current_streak || 0} <span className="text-lg font-normal text-[#71717A]">days</span>
                  </p>
                </div>
              </div>
              <p className="text-[#71717A] text-xs">Best: {streak?.longest_streak || 0} days</p>
            </div>

            {/* Consistency */}
            <div className="mavr-card" data-testid="consistency-card">
              <div className="flex items-center gap-3 mb-4">
                <TrendingUp className="w-8 h-8 text-[#10B981]" />
                <div>
                  <p className="text-[#71717A] text-xs uppercase tracking-widest">7-Day Consistency</p>
                  <p className="font-['Barlow_Condensed'] text-3xl font-black text-white">
                    {data?.consistency_score || 0}<span className="text-lg font-normal text-[#71717A]">%</span>
                  </p>
                </div>
              </div>
              <Progress value={data?.consistency_score || 0} className="h-1 bg-[#262626]" />
            </div>

            {/* Daily Checklist */}
            <div className="md:col-span-2 mavr-card" data-testid="checklist-card">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <p className="text-[#71717A] text-xs uppercase tracking-widest mb-1">Daily Checklist</p>
                  <p className="text-white font-semibold">{completedItems}/{totalItems} completed</p>
                </div>
                <Link 
                  to="/checkin"
                  className="text-[#E50914] hover:underline text-sm font-semibold flex items-center gap-1"
                >
                  Check In <ChevronRight className="w-4 h-4" />
                </Link>
              </div>
              
              <div className="space-y-3">
                <ChecklistItem 
                  icon={Sun} 
                  label="Morning Check-in" 
                  completed={checklist.morning_checkin}
                  link="/checkin/morning"
                />
                <ChecklistItem 
                  icon={Dumbbell} 
                  label="Workout Completed" 
                  completed={checklist.workout_completed}
                  link="/checkin/workout"
                />
                <ChecklistItem 
                  icon={Flame} 
                  label="Protein Target Hit" 
                  completed={checklist.protein_hit}
                  link="/checkin/night"
                />
                <ChecklistItem 
                  icon={Droplets} 
                  label="Water Target Hit" 
                  completed={checklist.water_hit}
                  link="/checkin/night"
                />
                <ChecklistItem 
                  icon={Footprints} 
                  label="Steps Completed" 
                  completed={checklist.steps_completed}
                  link="/checkin/night"
                />
                <ChecklistItem 
                  icon={Moon} 
                  label="Night Check-in" 
                  completed={checklist.night_checkin}
                  link="/checkin/night"
                />
              </div>
            </div>

            {/* Macros Summary */}
            <div className="md:col-span-2 mavr-card" data-testid="macros-card">
              <p className="text-[#71717A] text-xs uppercase tracking-widest mb-4">Today's Targets</p>
              <div className="grid grid-cols-4 gap-4">
                <MacroItem label="Calories" value={dietPlan?.target_calories} unit="kcal" />
                <MacroItem label="Protein" value={dietPlan?.target_protein} unit="g" />
                <MacroItem label="Carbs" value={dietPlan?.target_carbs} unit="g" />
                <MacroItem label="Water" value={dietPlan?.target_water_liters} unit="L" />
              </div>
            </div>

            {/* Today's Workout */}
            <div className="md:col-span-2 mavr-card" data-testid="workout-card">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <Dumbbell className="w-6 h-6 text-[#E50914]" />
                  <div>
                    <p className="text-[#71717A] text-xs uppercase tracking-widest">Today's Workout</p>
                    <p className="text-white font-semibold">
                      {workoutPlan?.session?.name || (workoutPlan?.rest_day ? "Rest Day" : "No Workout")}
                    </p>
                  </div>
                </div>
                <Link 
                  to="/workout"
                  className="text-[#E50914] hover:underline text-sm font-semibold flex items-center gap-1"
                >
                  View <ChevronRight className="w-4 h-4" />
                </Link>
              </div>
              
              {workoutPlan?.session ? (
                <div className="space-y-2">
                  <div className="flex items-center gap-4 text-sm text-[#A1A1AA]">
                    <span>{workoutPlan.session.estimated_duration_mins} mins</span>
                    <span className={`uppercase text-xs font-bold ${
                      workoutPlan.session.intensity_level === "high" ? "text-[#E50914]" :
                      workoutPlan.session.intensity_level === "medium" ? "text-[#F59E0B]" :
                      "text-[#10B981]"
                    }`}>
                      {workoutPlan.session.intensity_level} intensity
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {workoutPlan.session.focus_areas?.slice(0, 4).map((area, i) => (
                      <span key={i} className="px-2 py-1 bg-[#262626] text-[#A1A1AA] text-xs uppercase">
                        {area}
                      </span>
                    ))}
                  </div>
                </div>
              ) : workoutPlan?.rest_day ? (
                <p className="text-[#A1A1AA] text-sm">{workoutPlan.message}</p>
              ) : null}
            </div>

            {/* Today's Diet */}
            <div className="md:col-span-2 mavr-card" data-testid="diet-card">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <Utensils className="w-6 h-6 text-[#E50914]" />
                  <div>
                    <p className="text-[#71717A] text-xs uppercase tracking-widest">Today's Diet Plan</p>
                    <p className="text-white font-semibold">{dietPlan?.meals?.length || 0} Meals Planned</p>
                  </div>
                </div>
                <Link 
                  to="/diet"
                  className="text-[#E50914] hover:underline text-sm font-semibold flex items-center gap-1"
                >
                  View Full Plan <ChevronRight className="w-4 h-4" />
                </Link>
              </div>
              
              {dietPlan?.meals?.length > 0 && (
                <div className="space-y-2">
                  {dietPlan.meals.slice(0, 3).map((meal, i) => (
                    <div key={i} className="flex items-center justify-between py-2 border-b border-[#262626] last:border-0">
                      <div>
                        <p className="text-white text-sm capitalize">{meal.meal_type?.replace('_', ' ')}</p>
                        <p className="text-[#71717A] text-xs">{meal.time_suggestion}</p>
                      </div>
                      <p className="text-[#A1A1AA] text-sm">{meal.total_calories} kcal</p>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Event Countdown */}
            {data?.event && (
              <div className="mavr-card bg-cover bg-center relative overflow-hidden" 
                style={{ backgroundImage: `url('https://images.pexels.com/photos/12201296/pexels-photo-12201296.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940')` }}
                data-testid="event-card"
              >
                <div className="absolute inset-0 bg-[#0A0A0A]/80"></div>
                <div className="relative z-10">
                  <div className="flex items-center gap-2 mb-2">
                    <Calendar className="w-5 h-5 text-[#E50914]" />
                    <p className="text-[#71717A] text-xs uppercase tracking-widest">Event Mode</p>
                  </div>
                  <p className="text-white font-semibold mb-2">{data.event.event_name}</p>
                  <p className="font-['Barlow_Condensed'] text-4xl font-black text-[#E50914]">
                    {data.event_countdown || 0} <span className="text-lg text-white">days left</span>
                  </p>
                </div>
              </div>
            )}

            {/* Clothing Recommendation */}
            {data?.clothing_recommendation && (
              <div className="mavr-card" data-testid="clothing-card">
                <p className="text-[#71717A] text-xs uppercase tracking-widest mb-2">Gear Update</p>
                <p className="text-white font-semibold mb-2">{data.clothing_recommendation.recommendation_text}</p>
                <p className="text-[#A1A1AA] text-sm">{data.clothing_recommendation.reason}</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

function ChecklistItem({ icon: Icon, label, completed, link }) {
  return (
    <Link 
      to={link}
      className={`flex items-center gap-3 p-3 border transition-all ${
        completed 
          ? "border-[#10B981]/30 bg-[#10B981]/5" 
          : "border-[#262626] hover:border-[#333] hover:bg-[#1A1A1A]"
      }`}
    >
      <div className={`w-6 h-6 border-2 flex items-center justify-center ${
        completed ? "border-[#10B981] bg-[#10B981]" : "border-[#262626]"
      }`}>
        {completed && <span className="text-white text-xs">✓</span>}
      </div>
      <Icon className={`w-5 h-5 ${completed ? "text-[#10B981]" : "text-[#71717A]"}`} />
      <span className={`flex-1 text-sm ${completed ? "text-[#10B981] line-through" : "text-white"}`}>
        {label}
      </span>
    </Link>
  );
}

function MacroItem({ label, value, unit }) {
  return (
    <div className="text-center">
      <p className="font-['Barlow_Condensed'] text-2xl font-bold text-white">
        {value || "--"}
      </p>
      <p className="text-[#71717A] text-xs uppercase tracking-widest">{unit}</p>
      <p className="text-[#A1A1AA] text-xs mt-1">{label}</p>
    </div>
  );
}

function getGreeting() {
  const hour = new Date().getHours();
  if (hour < 12) return "Good Morning";
  if (hour < 17) return "Good Afternoon";
  return "Good Evening";
}
