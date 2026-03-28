import { useState, useEffect } from "react";
import { Link, useParams, useNavigate } from "react-router-dom";
import api from "../lib/api";
import { toast } from "sonner";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Slider } from "../components/ui/slider";
import { Checkbox } from "../components/ui/checkbox";
import { ArrowLeft, Sun, Dumbbell, Moon, Check, ChevronRight } from "lucide-react";

const CHECKIN_TYPES = [
  { id: "morning", icon: Sun, title: "Morning Check-in", subtitle: "Start your day right" },
  { id: "workout", icon: Dumbbell, title: "Workout Check-in", subtitle: "Log your session" },
  { id: "night", icon: Moon, title: "Night Check-in", subtitle: "End of day reflection" },
];

export default function Checkin() {
  const { type } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  // Morning check-in state
  const [morningData, setMorningData] = useState({
    weight_kg: "",
    sleep_hours: "",
    sleep_quality: 7,
    soreness_level: 3,
    mood: 7,
    energy: 7,
    notes: "",
  });

  // Workout check-in state
  const [workoutData, setWorkoutData] = useState({
    workout_completed: false,
    cardio_completed: false,
    cardio_duration_mins: "",
    session_intensity: 7,
    notes: "",
  });

  // Night check-in state
  const [nightData, setNightData] = useState({
    protein_target_hit: false,
    water_target_hit: false,
    steps_completed: false,
    steps_count: "",
    diet_adherence: 7,
    calories_consumed: "",
    reflections: "",
  });

  const handleMorningSubmit = async () => {
    setLoading(true);
    try {
      const data = {
        weight_kg: morningData.weight_kg ? parseFloat(morningData.weight_kg) : null,
        sleep_hours: morningData.sleep_hours ? parseFloat(morningData.sleep_hours) : null,
        sleep_quality: morningData.sleep_quality,
        soreness_level: morningData.soreness_level,
        mood: morningData.mood,
        energy: morningData.energy,
        notes: morningData.notes || null,
      };
      await api.morningCheckin(data);
      toast.success("Morning check-in saved!");
      navigate("/dashboard");
    } catch (error) {
      toast.error("Failed to save check-in");
      console.error(error);
    }
    setLoading(false);
  };

  const handleWorkoutSubmit = async () => {
    setLoading(true);
    try {
      const data = {
        workout_completed: workoutData.workout_completed,
        cardio_completed: workoutData.cardio_completed,
        cardio_duration_mins: workoutData.cardio_duration_mins ? parseInt(workoutData.cardio_duration_mins) : null,
        session_intensity: workoutData.session_intensity,
        notes: workoutData.notes || null,
      };
      await api.workoutCheckin(data);
      toast.success("Workout check-in saved!");
      navigate("/dashboard");
    } catch (error) {
      toast.error("Failed to save check-in");
      console.error(error);
    }
    setLoading(false);
  };

  const handleNightSubmit = async () => {
    setLoading(true);
    try {
      const data = {
        protein_target_hit: nightData.protein_target_hit,
        water_target_hit: nightData.water_target_hit,
        steps_completed: nightData.steps_completed,
        steps_count: nightData.steps_count ? parseInt(nightData.steps_count) : null,
        diet_adherence: nightData.diet_adherence,
        calories_consumed: nightData.calories_consumed ? parseInt(nightData.calories_consumed) : null,
        reflections: nightData.reflections || null,
      };
      await api.nightCheckin(data);
      toast.success("Night check-in saved!");
      navigate("/dashboard");
    } catch (error) {
      toast.error("Failed to save check-in");
      console.error(error);
    }
    setLoading(false);
  };

  // If no type specified, show selection
  if (!type) {
    return (
      <div className="min-h-screen bg-[#0A0A0A]">
        <header className="glass-header sticky top-0 z-40">
          <div className="max-w-2xl mx-auto px-4 py-4 flex items-center gap-4">
            <Link to="/dashboard" className="text-[#71717A] hover:text-white transition-colors">
              <ArrowLeft className="w-6 h-6" />
            </Link>
            <div>
              <p className="overline text-xs">Daily</p>
              <h1 className="font-['Barlow_Condensed'] text-2xl font-bold uppercase tracking-tight text-white">
                Check-in
              </h1>
            </div>
          </div>
        </header>

        <main className="max-w-2xl mx-auto px-4 py-8">
          <p className="text-[#A1A1AA] mb-6">Select a check-in type to log your progress.</p>
          
          <div className="space-y-4">
            {CHECKIN_TYPES.map(checkin => (
              <Link
                key={checkin.id}
                to={`/checkin/${checkin.id}`}
                className="mavr-card flex items-center gap-4 group"
                data-testid={`checkin-${checkin.id}`}
              >
                <div className="w-12 h-12 bg-[#E50914]/10 flex items-center justify-center group-hover:bg-[#E50914]/20 transition-colors">
                  <checkin.icon className="w-6 h-6 text-[#E50914]" />
                </div>
                <div className="flex-1">
                  <p className="text-white font-semibold">{checkin.title}</p>
                  <p className="text-[#71717A] text-sm">{checkin.subtitle}</p>
                </div>
                <ChevronRight className="w-5 h-5 text-[#71717A] group-hover:text-white transition-colors" />
              </Link>
            ))}
          </div>
        </main>
      </div>
    );
  }

  const renderContent = () => {
    switch (type) {
      case "morning":
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Weight (kg)</Label>
                <Input
                  type="number"
                  step="0.1"
                  value={morningData.weight_kg}
                  onChange={(e) => setMorningData(prev => ({ ...prev, weight_kg: e.target.value }))}
                  className="bg-[#121212] border-[#262626] text-white h-12 rounded-none"
                  placeholder="70.5"
                  data-testid="morning-weight"
                />
              </div>
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Sleep Hours</Label>
                <Input
                  type="number"
                  step="0.5"
                  value={morningData.sleep_hours}
                  onChange={(e) => setMorningData(prev => ({ ...prev, sleep_hours: e.target.value }))}
                  className="bg-[#121212] border-[#262626] text-white h-12 rounded-none"
                  placeholder="7.5"
                  data-testid="morning-sleep"
                />
              </div>
            </div>

            <SliderInput
              label="Sleep Quality"
              value={morningData.sleep_quality}
              onChange={(v) => setMorningData(prev => ({ ...prev, sleep_quality: v }))}
              testId="morning-sleep-quality"
            />

            <SliderInput
              label="Soreness Level"
              value={morningData.soreness_level}
              onChange={(v) => setMorningData(prev => ({ ...prev, soreness_level: v }))}
              lowLabel="None"
              highLabel="Very Sore"
              testId="morning-soreness"
            />

            <SliderInput
              label="Mood"
              value={morningData.mood}
              onChange={(v) => setMorningData(prev => ({ ...prev, mood: v }))}
              lowLabel="Low"
              highLabel="Great"
              testId="morning-mood"
            />

            <SliderInput
              label="Energy Level"
              value={morningData.energy}
              onChange={(v) => setMorningData(prev => ({ ...prev, energy: v }))}
              lowLabel="Tired"
              highLabel="Energized"
              testId="morning-energy"
            />

            <button
              onClick={handleMorningSubmit}
              disabled={loading}
              className="w-full py-4 bg-[#E50914] text-white font-['Barlow_Condensed'] font-bold uppercase tracking-widest hover:bg-[#B80710] transition-colors disabled:opacity-50"
              data-testid="morning-submit"
            >
              {loading ? "Saving..." : "Complete Morning Check-in"}
            </button>
          </div>
        );

      case "workout":
        return (
          <div className="space-y-6">
            <CheckboxInput
              label="Workout Completed"
              checked={workoutData.workout_completed}
              onChange={(v) => setWorkoutData(prev => ({ ...prev, workout_completed: v }))}
              testId="workout-completed"
            />

            <CheckboxInput
              label="Cardio Completed"
              checked={workoutData.cardio_completed}
              onChange={(v) => setWorkoutData(prev => ({ ...prev, cardio_completed: v }))}
              testId="cardio-completed"
            />

            {workoutData.cardio_completed && (
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Cardio Duration (mins)</Label>
                <Input
                  type="number"
                  value={workoutData.cardio_duration_mins}
                  onChange={(e) => setWorkoutData(prev => ({ ...prev, cardio_duration_mins: e.target.value }))}
                  className="bg-[#121212] border-[#262626] text-white h-12 rounded-none"
                  placeholder="30"
                />
              </div>
            )}

            <SliderInput
              label="Session Intensity"
              value={workoutData.session_intensity}
              onChange={(v) => setWorkoutData(prev => ({ ...prev, session_intensity: v }))}
              lowLabel="Easy"
              highLabel="Max Effort"
              testId="workout-intensity"
            />

            <div className="space-y-2">
              <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Notes (Optional)</Label>
              <textarea
                value={workoutData.notes}
                onChange={(e) => setWorkoutData(prev => ({ ...prev, notes: e.target.value }))}
                className="w-full bg-[#121212] border border-[#262626] text-white p-3 min-h-[100px] resize-none focus:border-[#E50914] focus:outline-none"
                placeholder="How did the session feel?"
              />
            </div>

            <button
              onClick={handleWorkoutSubmit}
              disabled={loading}
              className="w-full py-4 bg-[#E50914] text-white font-['Barlow_Condensed'] font-bold uppercase tracking-widest hover:bg-[#B80710] transition-colors disabled:opacity-50"
              data-testid="workout-submit"
            >
              {loading ? "Saving..." : "Complete Workout Check-in"}
            </button>
          </div>
        );

      case "night":
        return (
          <div className="space-y-6">
            <CheckboxInput
              label="Protein Target Hit"
              checked={nightData.protein_target_hit}
              onChange={(v) => setNightData(prev => ({ ...prev, protein_target_hit: v }))}
              testId="protein-hit"
            />

            <CheckboxInput
              label="Water Target Hit"
              checked={nightData.water_target_hit}
              onChange={(v) => setNightData(prev => ({ ...prev, water_target_hit: v }))}
              testId="water-hit"
            />

            <CheckboxInput
              label="Steps Completed"
              checked={nightData.steps_completed}
              onChange={(v) => setNightData(prev => ({ ...prev, steps_completed: v }))}
              testId="steps-completed"
            />

            {nightData.steps_completed && (
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Steps Count</Label>
                <Input
                  type="number"
                  value={nightData.steps_count}
                  onChange={(e) => setNightData(prev => ({ ...prev, steps_count: e.target.value }))}
                  className="bg-[#121212] border-[#262626] text-white h-12 rounded-none"
                  placeholder="10000"
                />
              </div>
            )}

            <SliderInput
              label="Diet Adherence"
              value={nightData.diet_adherence}
              onChange={(v) => setNightData(prev => ({ ...prev, diet_adherence: v }))}
              lowLabel="Off Plan"
              highLabel="On Point"
              testId="diet-adherence"
            />

            <div className="space-y-2">
              <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Calories Consumed (Optional)</Label>
              <Input
                type="number"
                value={nightData.calories_consumed}
                onChange={(e) => setNightData(prev => ({ ...prev, calories_consumed: e.target.value }))}
                className="bg-[#121212] border-[#262626] text-white h-12 rounded-none"
                placeholder="2000"
              />
            </div>

            <div className="space-y-2">
              <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Reflections (Optional)</Label>
              <textarea
                value={nightData.reflections}
                onChange={(e) => setNightData(prev => ({ ...prev, reflections: e.target.value }))}
                className="w-full bg-[#121212] border border-[#262626] text-white p-3 min-h-[100px] resize-none focus:border-[#E50914] focus:outline-none"
                placeholder="How was your day?"
              />
            </div>

            <button
              onClick={handleNightSubmit}
              disabled={loading}
              className="w-full py-4 bg-[#E50914] text-white font-['Barlow_Condensed'] font-bold uppercase tracking-widest hover:bg-[#B80710] transition-colors disabled:opacity-50"
              data-testid="night-submit"
            >
              {loading ? "Saving..." : "Complete Night Check-in"}
            </button>
          </div>
        );

      default:
        return null;
    }
  };

  const currentType = CHECKIN_TYPES.find(c => c.id === type);

  return (
    <div className="min-h-screen bg-[#0A0A0A]">
      <header className="glass-header sticky top-0 z-40">
        <div className="max-w-2xl mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/checkin" className="text-[#71717A] hover:text-white transition-colors">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <div className="flex items-center gap-3">
            {currentType && (
              <div className="w-10 h-10 bg-[#E50914]/10 flex items-center justify-center">
                <currentType.icon className="w-5 h-5 text-[#E50914]" />
              </div>
            )}
            <div>
              <p className="overline text-xs">{currentType?.subtitle}</p>
              <h1 className="font-['Barlow_Condensed'] text-xl font-bold uppercase tracking-tight text-white">
                {currentType?.title}
              </h1>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-4 py-8">
        {renderContent()}
      </main>
    </div>
  );
}

function SliderInput({ label, value, onChange, lowLabel = "Low", highLabel = "High", testId }) {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">{label}</Label>
        <span className="font-['JetBrains_Mono'] text-white font-bold">{value}/10</span>
      </div>
      <Slider
        value={[value]}
        onValueChange={([v]) => onChange(v)}
        min={1}
        max={10}
        step={1}
        className="w-full"
        data-testid={testId}
      />
      <div className="flex justify-between text-[#71717A] text-xs">
        <span>{lowLabel}</span>
        <span>{highLabel}</span>
      </div>
    </div>
  );
}

function CheckboxInput({ label, checked, onChange, testId }) {
  return (
    <button
      onClick={() => onChange(!checked)}
      className={`w-full flex items-center gap-4 p-4 border transition-all ${
        checked 
          ? "border-[#10B981]/50 bg-[#10B981]/10" 
          : "border-[#262626] hover:border-[#333]"
      }`}
      data-testid={testId}
    >
      <div className={`w-6 h-6 border-2 flex items-center justify-center transition-all ${
        checked ? "border-[#10B981] bg-[#10B981]" : "border-[#262626]"
      }`}>
        {checked && <Check className="w-4 h-4 text-white" />}
      </div>
      <span className={`font-semibold ${checked ? "text-[#10B981]" : "text-white"}`}>
        {label}
      </span>
    </button>
  );
}
