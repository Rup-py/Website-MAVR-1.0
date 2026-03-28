import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../lib/api";
import { toast } from "sonner";
import { ArrowLeft, Utensils, Droplets, Clock, ChevronDown, ChevronUp } from "lucide-react";

export default function DietPlan() {
  const [dietPlan, setDietPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [expandedMeals, setExpandedMeals] = useState({});

  useEffect(() => {
    loadDietPlan();
  }, []);

  const loadDietPlan = async () => {
    try {
      const { data } = await api.getTodayDiet();
      setDietPlan(data);
      // Expand first meal by default
      if (data?.meals?.length > 0) {
        setExpandedMeals({ 0: true });
      }
    } catch (error) {
      toast.error("Failed to load diet plan");
      console.error(error);
    }
    setLoading(false);
  };

  const toggleMeal = (index) => {
    setExpandedMeals(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
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
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center gap-4">
          <Link to="/dashboard" className="text-[#71717A] hover:text-white transition-colors">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <div>
            <p className="overline text-xs">{dietPlan?.date || "Today"}</p>
            <h1 className="font-['Barlow_Condensed'] text-2xl font-bold uppercase tracking-tight text-white">
              Diet Plan
            </h1>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Targets Summary */}
        <div className="mavr-card mb-6" data-testid="diet-targets">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <TargetCard label="Calories" value={dietPlan?.target_calories} unit="kcal" primary />
            <TargetCard label="Protein" value={dietPlan?.target_protein} unit="g" />
            <TargetCard label="Carbs" value={dietPlan?.target_carbs} unit="g" />
            <TargetCard label="Fats" value={dietPlan?.target_fats} unit="g" />
            <TargetCard label="Water" value={dietPlan?.target_water_liters} unit="L" icon={Droplets} />
          </div>
        </div>

        {/* AI Guidance */}
        {dietPlan?.ai_guidance && (
          <div className="mavr-card mb-6 border-[#E50914]/30">
            <p className="text-[#71717A] text-xs uppercase tracking-widest mb-2">AI Insight</p>
            <p className="text-white">{dietPlan.ai_guidance}</p>
          </div>
        )}

        {/* Notes */}
        {dietPlan?.notes && (
          <div className="mavr-card mb-6">
            <p className="text-[#71717A] text-xs uppercase tracking-widest mb-2">Today's Focus</p>
            <p className="text-[#A1A1AA]">{dietPlan.notes}</p>
          </div>
        )}

        {/* Meals */}
        <div className="space-y-4" data-testid="meals-list">
          {dietPlan?.meals?.map((meal, index) => (
            <div key={index} className="mavr-card">
              <button
                onClick={() => toggleMeal(index)}
                className="w-full flex items-center justify-between"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 bg-[#E50914]/10 flex items-center justify-center">
                    <Utensils className="w-5 h-5 text-[#E50914]" />
                  </div>
                  <div className="text-left">
                    <p className="text-white font-semibold capitalize">
                      {meal.meal_type?.replace('_', ' ')}
                    </p>
                    <div className="flex items-center gap-2 text-[#71717A] text-sm">
                      <Clock className="w-4 h-4" />
                      <span>{meal.time_suggestion}</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <p className="text-white font-semibold">{meal.total_calories} kcal</p>
                    <p className="text-[#71717A] text-xs">P: {meal.total_protein}g</p>
                  </div>
                  {expandedMeals[index] ? (
                    <ChevronUp className="w-5 h-5 text-[#71717A]" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-[#71717A]" />
                  )}
                </div>
              </button>

              {expandedMeals[index] && (
                <div className="mt-4 pt-4 border-t border-[#262626] space-y-4">
                  {meal.items?.map((item, itemIndex) => (
                    <div key={itemIndex} className="flex items-start justify-between">
                      <div className="flex-1">
                        <p className="text-white">{item.name}</p>
                        <p className="text-[#71717A] text-sm">{item.quantity}</p>
                        {item.notes && (
                          <p className="text-[#A1A1AA] text-xs mt-1">{item.notes}</p>
                        )}
                        {item.substitutes?.length > 0 && (
                          <p className="text-[#71717A] text-xs mt-1">
                            Substitutes: {item.substitutes.join(', ')}
                          </p>
                        )}
                      </div>
                      <div className="text-right">
                        <p className="text-[#A1A1AA] text-sm">{item.calories} kcal</p>
                        <p className="text-[#71717A] text-xs">P: {item.protein}g</p>
                      </div>
                    </div>
                  ))}
                  
                  <div className="pt-4 border-t border-[#262626] grid grid-cols-4 gap-4 text-center">
                    <div>
                      <p className="text-white font-semibold">{meal.total_calories}</p>
                      <p className="text-[#71717A] text-xs">Calories</p>
                    </div>
                    <div>
                      <p className="text-white font-semibold">{meal.total_protein}g</p>
                      <p className="text-[#71717A] text-xs">Protein</p>
                    </div>
                    <div>
                      <p className="text-white font-semibold">{meal.total_carbs}g</p>
                      <p className="text-[#71717A] text-xs">Carbs</p>
                    </div>
                    <div>
                      <p className="text-white font-semibold">{meal.total_fats}g</p>
                      <p className="text-[#71717A] text-xs">Fats</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

function TargetCard({ label, value, unit, primary, icon: Icon }) {
  return (
    <div className={`text-center p-4 border ${primary ? 'border-[#E50914]/30 bg-[#E50914]/5' : 'border-[#262626]'}`}>
      {Icon && <Icon className="w-5 h-5 text-[#E50914] mx-auto mb-2" />}
      <p className={`font-['Barlow_Condensed'] text-2xl font-bold ${primary ? 'text-[#E50914]' : 'text-white'}`}>
        {value || "--"}
      </p>
      <p className="text-[#71717A] text-xs uppercase tracking-widest">{unit}</p>
      <p className="text-[#A1A1AA] text-xs mt-1">{label}</p>
    </div>
  );
}
