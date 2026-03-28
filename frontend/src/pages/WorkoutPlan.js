import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../lib/api";
import { toast } from "sonner";
import { ArrowLeft, Dumbbell, Clock, Flame, ChevronDown, ChevronUp, Play, CheckCircle } from "lucide-react";

export default function WorkoutPlan() {
  const [workoutPlan, setWorkoutPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [expandedSections, setExpandedSections] = useState({ warmup: true, main: true, cooldown: false });

  useEffect(() => {
    loadWorkoutPlan();
  }, []);

  const loadWorkoutPlan = async () => {
    try {
      const { data } = await api.getTodayWorkout();
      setWorkoutPlan(data);
    } catch (error) {
      toast.error("Failed to load workout plan");
      console.error(error);
    }
    setLoading(false);
  };

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0A0A0A] flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-[#E50914] border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  const session = workoutPlan?.session;
  const isRestDay = workoutPlan?.rest_day;

  return (
    <div className="min-h-screen bg-[#0A0A0A]">
      {/* Header */}
      <header className="glass-header sticky top-0 z-40">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/dashboard" className="text-[#71717A] hover:text-white transition-colors">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <div>
            <p className="overline text-xs">{workoutPlan?.date || "Today"}</p>
            <h1 className="font-['Barlow_Condensed'] text-2xl font-bold uppercase tracking-tight text-white">
              Workout
            </h1>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        {isRestDay ? (
          <div className="mavr-card text-center py-12" data-testid="rest-day">
            <div className="w-16 h-16 bg-[#10B981]/10 rounded-full flex items-center justify-center mx-auto mb-6">
              <CheckCircle className="w-8 h-8 text-[#10B981]" />
            </div>
            <h2 className="font-['Barlow_Condensed'] text-3xl font-bold uppercase text-white mb-4">
              Rest Day
            </h2>
            <p className="text-[#A1A1AA] max-w-md mx-auto">
              {workoutPlan?.message || "Recovery is part of progress. Focus on mobility, hydration, and nutrition today."}
            </p>
          </div>
        ) : session ? (
          <>
            {/* Session Overview */}
            <div className="mavr-card mb-6" data-testid="workout-overview">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-12 h-12 bg-[#E50914]/10 flex items-center justify-center">
                  <Dumbbell className="w-6 h-6 text-[#E50914]" />
                </div>
                <div>
                  <h2 className="font-['Barlow_Condensed'] text-2xl font-bold uppercase text-white">
                    {session.name}
                  </h2>
                  <div className="flex items-center gap-4 text-[#71717A] text-sm">
                    <span className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      {session.estimated_duration_mins} mins
                    </span>
                    <span className={`flex items-center gap-1 uppercase text-xs font-bold ${
                      session.intensity_level === "high" ? "text-[#E50914]" :
                      session.intensity_level === "medium" ? "text-[#F59E0B]" :
                      "text-[#10B981]"
                    }`}>
                      <Flame className="w-4 h-4" />
                      {session.intensity_level}
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="flex flex-wrap gap-2">
                {session.focus_areas?.map((area, i) => (
                  <span key={i} className="px-3 py-1 bg-[#262626] text-[#A1A1AA] text-sm uppercase">
                    {area}
                  </span>
                ))}
              </div>
            </div>

            {/* AI Guidance */}
            {workoutPlan?.ai_guidance && (
              <div className="mavr-card mb-6 border-[#E50914]/30">
                <p className="text-[#71717A] text-xs uppercase tracking-widest mb-2">AI Insight</p>
                <p className="text-white">{workoutPlan.ai_guidance}</p>
              </div>
            )}

            {/* Progression Notes */}
            {workoutPlan?.progression_notes && (
              <div className="mavr-card mb-6">
                <p className="text-[#71717A] text-xs uppercase tracking-widest mb-2">Progression Focus</p>
                <p className="text-[#A1A1AA]">{workoutPlan.progression_notes}</p>
              </div>
            )}

            {/* Warmup */}
            {session.warmup?.length > 0 && (
              <ExerciseSection
                title="Warmup"
                exercises={session.warmup}
                expanded={expandedSections.warmup}
                onToggle={() => toggleSection('warmup')}
              />
            )}

            {/* Main Workout */}
            {session.main_workout?.length > 0 && (
              <ExerciseSection
                title="Main Workout"
                exercises={session.main_workout}
                expanded={expandedSections.main}
                onToggle={() => toggleSection('main')}
                primary
              />
            )}

            {/* Cooldown */}
            {session.cooldown?.length > 0 && (
              <ExerciseSection
                title="Cooldown"
                exercises={session.cooldown}
                expanded={expandedSections.cooldown}
                onToggle={() => toggleSection('cooldown')}
              />
            )}

            {/* Start Workout Button */}
            <div className="mt-8">
              <Link
                to="/checkin/workout"
                className="flex items-center justify-center gap-2 w-full py-4 bg-[#E50914] text-white font-['Barlow_Condensed'] font-bold uppercase tracking-widest hover:bg-[#B80710] transition-colors"
                data-testid="start-workout-btn"
              >
                <Play className="w-5 h-5" />
                Start Workout
              </Link>
            </div>
          </>
        ) : (
          <div className="mavr-card text-center py-12">
            <p className="text-[#A1A1AA]">No workout plan available for today.</p>
          </div>
        )}
      </main>
    </div>
  );
}

function ExerciseSection({ title, exercises, expanded, onToggle, primary }) {
  return (
    <div className={`mavr-card mb-4 ${primary ? 'border-[#E50914]/30' : ''}`} data-testid={`section-${title.toLowerCase()}`}>
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between"
      >
        <div className="flex items-center gap-3">
          <p className={`font-['Barlow_Condensed'] text-lg font-bold uppercase ${primary ? 'text-[#E50914]' : 'text-white'}`}>
            {title}
          </p>
          <span className="text-[#71717A] text-sm">{exercises.length} exercises</span>
        </div>
        {expanded ? (
          <ChevronUp className="w-5 h-5 text-[#71717A]" />
        ) : (
          <ChevronDown className="w-5 h-5 text-[#71717A]" />
        )}
      </button>

      {expanded && (
        <div className="mt-4 pt-4 border-t border-[#262626] space-y-4">
          {exercises.map((exercise, index) => (
            <div key={index} className="flex items-start gap-4">
              <div className="w-8 h-8 bg-[#262626] flex items-center justify-center shrink-0">
                <span className="text-[#71717A] text-sm font-bold">{index + 1}</span>
              </div>
              <div className="flex-1">
                <p className="text-white font-semibold">{exercise.name}</p>
                <div className="flex flex-wrap items-center gap-3 mt-1 text-[#71717A] text-sm">
                  <span>{exercise.sets} sets × {exercise.reps}</span>
                  {exercise.rest_seconds > 0 && (
                    <span>Rest: {exercise.rest_seconds}s</span>
                  )}
                </div>
                {exercise.notes && (
                  <p className="text-[#A1A1AA] text-xs mt-2">{exercise.notes}</p>
                )}
                {exercise.equipment_needed?.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {exercise.equipment_needed.map((eq, i) => (
                      <span key={i} className="px-2 py-0.5 bg-[#1A1A1A] text-[#71717A] text-xs">
                        {eq}
                      </span>
                    ))}
                  </div>
                )}
                {exercise.substitutes?.length > 0 && (
                  <p className="text-[#71717A] text-xs mt-1">
                    Alt: {exercise.substitutes.join(', ')}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
