import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import api from "../lib/api";
import { toast } from "sonner";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Checkbox } from "../components/ui/checkbox";
import { ArrowRight, ArrowLeft, Check } from "lucide-react";

const STEPS = [
  { id: "basics", title: "Basic Info", subtitle: "Let's start with the essentials" },
  { id: "body", title: "Body Metrics", subtitle: "Your current stats" },
  { id: "goals", title: "Goals", subtitle: "What are you working towards?" },
  { id: "training", title: "Training", subtitle: "Your workout preferences" },
  { id: "lifestyle", title: "Lifestyle", subtitle: "Daily habits matter" },
  { id: "diet", title: "Diet", subtitle: "Nutrition preferences" },
];

const GOALS = [
  { value: "fat_loss", label: "Fat Loss", desc: "Reduce body fat, get leaner" },
  { value: "muscle_gain", label: "Muscle Gain", desc: "Build muscle mass" },
  { value: "strength", label: "Strength", desc: "Get stronger" },
  { value: "endurance", label: "Endurance", desc: "Improve stamina" },
  { value: "sports_performance", label: "Sports Performance", desc: "Excel in your sport" },
  { value: "general_fitness", label: "General Fitness", desc: "Overall health" },
];

const DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"];

const EQUIPMENT = [
  "barbell", "dumbbells", "bench", "squat rack", "pull up bar", "cables", 
  "leg press", "treadmill", "resistance bands", "kettlebells"
];

const MUSCLE_GROUPS = ["chest", "back", "shoulders", "biceps", "triceps", "legs", "core"];

export default function Onboarding() {
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const { refreshUser } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    // Basics
    age: "",
    gender: "",
    // Body
    height_cm: "",
    weight_kg: "",
    target_weight_kg: "",
    // Goals
    goal: "",
    training_age_months: "",
    event_goal: "",
    event_date: "",
    // Training
    workout_frequency: "4",
    preferred_workout_days: ["monday", "wednesday", "friday"],
    workout_setup: "gym",
    available_equipment: [],
    weak_muscle_groups: [],
    injuries: [],
    // Lifestyle
    sleep_hours: "7",
    stress_level: "5",
    activity_level: "moderately_active",
    daily_steps: "",
    water_intake_liters: "",
    // Diet
    diet_preference: "non_vegetarian",
    allergies: [],
    food_dislikes: [],
    meal_frequency: "4",
    budget_level: "medium",
    supplements: [],
  });

  const updateField = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const toggleArrayItem = (field, item) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field].includes(item) 
        ? prev[field].filter(i => i !== item)
        : [...prev[field], item]
    }));
  };

  const nextStep = () => {
    if (currentStep < STEPS.length - 1) {
      setCurrentStep(prev => prev + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      // Clean up data
      const profileData = {
        age: parseInt(formData.age) || null,
        gender: formData.gender || null,
        height_cm: parseFloat(formData.height_cm) || null,
        weight_kg: parseFloat(formData.weight_kg) || null,
        target_weight_kg: parseFloat(formData.target_weight_kg) || null,
        goal: formData.goal || null,
        training_age_months: parseInt(formData.training_age_months) || 0,
        workout_frequency: parseInt(formData.workout_frequency) || 4,
        preferred_workout_days: formData.preferred_workout_days,
        workout_setup: formData.workout_setup,
        available_equipment: formData.available_equipment,
        weak_muscle_groups: formData.weak_muscle_groups,
        injuries: formData.injuries,
        sleep_hours: parseFloat(formData.sleep_hours) || 7,
        stress_level: parseInt(formData.stress_level) || 5,
        activity_level: formData.activity_level,
        daily_steps: parseInt(formData.daily_steps) || null,
        water_intake_liters: parseFloat(formData.water_intake_liters) || null,
        diet_preference: formData.diet_preference,
        allergies: formData.allergies,
        food_dislikes: formData.food_dislikes,
        meal_frequency: parseInt(formData.meal_frequency) || 4,
        budget_level: formData.budget_level,
        supplements: formData.supplements,
        event_goal: formData.event_goal || null,
        event_date: formData.event_date || null,
      };

      await api.saveOnboarding(profileData);
      await refreshUser();
      toast.success("Your system is ready!");
      navigate("/dashboard");
    } catch (error) {
      toast.error("Failed to save profile. Please try again.");
      console.error(error);
    }
    setLoading(false);
  };

  const renderStep = () => {
    switch (STEPS[currentStep].id) {
      case "basics":
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Age</Label>
                <Input
                  type="number"
                  value={formData.age}
                  onChange={(e) => updateField("age", e.target.value)}
                  className="bg-[#121212] border-[#262626] text-white h-12 rounded-none"
                  placeholder="25"
                  data-testid="onboarding-age"
                />
              </div>
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Gender (Optional)</Label>
                <Select value={formData.gender} onValueChange={(v) => updateField("gender", v)}>
                  <SelectTrigger className="bg-[#121212] border-[#262626] text-white h-12 rounded-none" data-testid="onboarding-gender">
                    <SelectValue placeholder="Select" />
                  </SelectTrigger>
                  <SelectContent className="bg-[#121212] border-[#262626]">
                    <SelectItem value="male">Male</SelectItem>
                    <SelectItem value="female">Female</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
        );

      case "body":
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Height (cm)</Label>
                <Input
                  type="number"
                  value={formData.height_cm}
                  onChange={(e) => updateField("height_cm", e.target.value)}
                  className="bg-[#121212] border-[#262626] text-white h-12 rounded-none"
                  placeholder="175"
                  data-testid="onboarding-height"
                />
              </div>
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Weight (kg)</Label>
                <Input
                  type="number"
                  value={formData.weight_kg}
                  onChange={(e) => updateField("weight_kg", e.target.value)}
                  className="bg-[#121212] border-[#262626] text-white h-12 rounded-none"
                  placeholder="70"
                  data-testid="onboarding-weight"
                />
              </div>
            </div>
            <div className="space-y-2">
              <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Target Weight (kg)</Label>
              <Input
                type="number"
                value={formData.target_weight_kg}
                onChange={(e) => updateField("target_weight_kg", e.target.value)}
                className="bg-[#121212] border-[#262626] text-white h-12 rounded-none"
                placeholder="65"
                data-testid="onboarding-target-weight"
              />
            </div>
          </div>
        );

      case "goals":
        return (
          <div className="space-y-6">
            <div className="space-y-3">
              <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Primary Goal</Label>
              <div className="grid grid-cols-2 gap-3">
                {GOALS.map(goal => (
                  <button
                    key={goal.value}
                    type="button"
                    onClick={() => updateField("goal", goal.value)}
                    className={`p-4 border text-left transition-all ${
                      formData.goal === goal.value 
                        ? "border-[#E50914] bg-[#E50914]/10" 
                        : "border-[#262626] bg-[#121212] hover:border-[#333]"
                    }`}
                    data-testid={`goal-${goal.value}`}
                  >
                    <p className="text-white font-semibold">{goal.label}</p>
                    <p className="text-[#71717A] text-sm">{goal.desc}</p>
                  </button>
                ))}
              </div>
            </div>
            <div className="space-y-2">
              <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Training Age (months)</Label>
              <Input
                type="number"
                value={formData.training_age_months}
                onChange={(e) => updateField("training_age_months", e.target.value)}
                className="bg-[#121212] border-[#262626] text-white h-12 rounded-none"
                placeholder="12"
                data-testid="onboarding-training-age"
              />
              <p className="text-[#71717A] text-xs">How long have you been training consistently?</p>
            </div>
          </div>
        );

      case "training":
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Workouts/Week</Label>
                <Select value={formData.workout_frequency} onValueChange={(v) => updateField("workout_frequency", v)}>
                  <SelectTrigger className="bg-[#121212] border-[#262626] text-white h-12 rounded-none">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-[#121212] border-[#262626]">
                    {[2, 3, 4, 5, 6].map(n => (
                      <SelectItem key={n} value={String(n)}>{n} days</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Setup</Label>
                <Select value={formData.workout_setup} onValueChange={(v) => updateField("workout_setup", v)}>
                  <SelectTrigger className="bg-[#121212] border-[#262626] text-white h-12 rounded-none">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-[#121212] border-[#262626]">
                    <SelectItem value="gym">Gym</SelectItem>
                    <SelectItem value="home">Home</SelectItem>
                    <SelectItem value="both">Both</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Preferred Days</Label>
              <div className="flex flex-wrap gap-2">
                {DAYS.map(day => (
                  <button
                    key={day}
                    type="button"
                    onClick={() => toggleArrayItem("preferred_workout_days", day)}
                    className={`px-4 py-2 border text-sm uppercase transition-all ${
                      formData.preferred_workout_days.includes(day)
                        ? "border-[#E50914] bg-[#E50914]/10 text-white"
                        : "border-[#262626] text-[#71717A] hover:border-[#333]"
                    }`}
                  >
                    {day.slice(0, 3)}
                  </button>
                ))}
              </div>
            </div>

            {formData.workout_setup !== "home" && (
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Available Equipment</Label>
                <div className="flex flex-wrap gap-2">
                  {EQUIPMENT.map(eq => (
                    <button
                      key={eq}
                      type="button"
                      onClick={() => toggleArrayItem("available_equipment", eq)}
                      className={`px-3 py-1.5 border text-xs uppercase transition-all ${
                        formData.available_equipment.includes(eq)
                          ? "border-[#E50914] bg-[#E50914]/10 text-white"
                          : "border-[#262626] text-[#71717A] hover:border-[#333]"
                      }`}
                    >
                      {eq}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="space-y-2">
              <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Weak Points (Optional)</Label>
              <div className="flex flex-wrap gap-2">
                {MUSCLE_GROUPS.map(mg => (
                  <button
                    key={mg}
                    type="button"
                    onClick={() => toggleArrayItem("weak_muscle_groups", mg)}
                    className={`px-3 py-1.5 border text-xs uppercase transition-all ${
                      formData.weak_muscle_groups.includes(mg)
                        ? "border-[#E50914] bg-[#E50914]/10 text-white"
                        : "border-[#262626] text-[#71717A] hover:border-[#333]"
                    }`}
                  >
                    {mg}
                  </button>
                ))}
              </div>
            </div>
          </div>
        );

      case "lifestyle":
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Sleep (hours)</Label>
                <Select value={formData.sleep_hours} onValueChange={(v) => updateField("sleep_hours", v)}>
                  <SelectTrigger className="bg-[#121212] border-[#262626] text-white h-12 rounded-none">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-[#121212] border-[#262626]">
                    {[5, 6, 7, 8, 9, 10].map(n => (
                      <SelectItem key={n} value={String(n)}>{n} hours</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Stress Level</Label>
                <Select value={formData.stress_level} onValueChange={(v) => updateField("stress_level", v)}>
                  <SelectTrigger className="bg-[#121212] border-[#262626] text-white h-12 rounded-none">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-[#121212] border-[#262626]">
                    {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(n => (
                      <SelectItem key={n} value={String(n)}>{n}/10</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Activity Level</Label>
              <Select value={formData.activity_level} onValueChange={(v) => updateField("activity_level", v)}>
                <SelectTrigger className="bg-[#121212] border-[#262626] text-white h-12 rounded-none">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-[#121212] border-[#262626]">
                  <SelectItem value="sedentary">Sedentary (desk job)</SelectItem>
                  <SelectItem value="lightly_active">Lightly Active</SelectItem>
                  <SelectItem value="moderately_active">Moderately Active</SelectItem>
                  <SelectItem value="very_active">Very Active</SelectItem>
                  <SelectItem value="extremely_active">Extremely Active</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Daily Steps</Label>
                <Input
                  type="number"
                  value={formData.daily_steps}
                  onChange={(e) => updateField("daily_steps", e.target.value)}
                  className="bg-[#121212] border-[#262626] text-white h-12 rounded-none"
                  placeholder="8000"
                />
              </div>
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Water (liters)</Label>
                <Input
                  type="number"
                  step="0.1"
                  value={formData.water_intake_liters}
                  onChange={(e) => updateField("water_intake_liters", e.target.value)}
                  className="bg-[#121212] border-[#262626] text-white h-12 rounded-none"
                  placeholder="2.5"
                />
              </div>
            </div>
          </div>
        );

      case "diet":
        return (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Diet Preference</Label>
                <Select value={formData.diet_preference} onValueChange={(v) => updateField("diet_preference", v)}>
                  <SelectTrigger className="bg-[#121212] border-[#262626] text-white h-12 rounded-none">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-[#121212] border-[#262626]">
                    <SelectItem value="vegetarian">Vegetarian</SelectItem>
                    <SelectItem value="non_vegetarian">Non-Vegetarian</SelectItem>
                    <SelectItem value="eggetarian">Eggetarian</SelectItem>
                    <SelectItem value="vegan">Vegan</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Budget</Label>
                <Select value={formData.budget_level} onValueChange={(v) => updateField("budget_level", v)}>
                  <SelectTrigger className="bg-[#121212] border-[#262626] text-white h-12 rounded-none">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-[#121212] border-[#262626]">
                    <SelectItem value="low">Low Budget</SelectItem>
                    <SelectItem value="medium">Medium Budget</SelectItem>
                    <SelectItem value="high">High Budget</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-2">
              <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Meals Per Day</Label>
              <Select value={formData.meal_frequency} onValueChange={(v) => updateField("meal_frequency", v)}>
                <SelectTrigger className="bg-[#121212] border-[#262626] text-white h-12 rounded-none">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-[#121212] border-[#262626]">
                  {[3, 4, 5, 6].map(n => (
                    <SelectItem key={n} value={String(n)}>{n} meals</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="p-4 border border-[#262626] bg-[#121212]">
              <p className="text-white font-semibold mb-2">Almost Done!</p>
              <p className="text-[#71717A] text-sm">
                Based on your inputs, we'll generate a personalized diet and workout plan for you.
              </p>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-[#0A0A0A] flex flex-col">
      {/* Header */}
      <header className="border-b border-[#262626] px-6 py-4">
        <div className="max-w-2xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-[#E50914] flex items-center justify-center">
              <span className="font-['Barlow_Condensed'] font-black text-white text-lg">M</span>
            </div>
            <span className="font-['Barlow_Condensed'] font-bold text-xl tracking-tight text-white">MAVR</span>
          </div>
          <p className="text-[#71717A] text-sm">Step {currentStep + 1} of {STEPS.length}</p>
        </div>
      </header>

      {/* Progress bar */}
      <div className="mavr-progress">
        <div 
          className="mavr-progress-bar" 
          style={{ width: `${((currentStep + 1) / STEPS.length) * 100}%` }}
        ></div>
      </div>

      {/* Content */}
      <main className="flex-1 px-6 py-12">
        <div className="max-w-2xl mx-auto">
          <div className="mb-8">
            <p className="overline mb-2">{STEPS[currentStep].subtitle}</p>
            <h1 className="font-['Barlow_Condensed'] text-3xl sm:text-4xl font-bold uppercase tracking-tight text-white">
              {STEPS[currentStep].title}
            </h1>
          </div>

          {renderStep()}

          {/* Navigation */}
          <div className="mt-12 flex items-center justify-between">
            <button
              type="button"
              onClick={prevStep}
              disabled={currentStep === 0}
              className="flex items-center gap-2 px-6 py-3 border border-[#262626] text-white font-['Barlow_Condensed'] font-bold uppercase tracking-widest hover:bg-[#1A1A1A] transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <ArrowLeft className="w-4 h-4" />
              Back
            </button>

            {currentStep === STEPS.length - 1 ? (
              <button
                type="button"
                onClick={handleSubmit}
                disabled={loading}
                className="flex items-center gap-2 px-8 py-3 bg-[#E50914] text-white font-['Barlow_Condensed'] font-bold uppercase tracking-widest hover:bg-[#B80710] transition-colors disabled:opacity-50"
                data-testid="onboarding-submit"
              >
                {loading ? "Building Your System..." : "Complete Setup"}
                <Check className="w-4 h-4" />
              </button>
            ) : (
              <button
                type="button"
                onClick={nextStep}
                className="flex items-center gap-2 px-8 py-3 bg-[#E50914] text-white font-['Barlow_Condensed'] font-bold uppercase tracking-widest hover:bg-[#B80710] transition-colors"
                data-testid="onboarding-next"
              >
                Continue
                <ArrowRight className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
