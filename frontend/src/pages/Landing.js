import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { ArrowRight, Target, Activity, TrendingUp, Calendar, Dumbbell, Utensils } from "lucide-react";

export default function Landing() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-[#0A0A0A]">
      {/* Header */}
      <header className="glass-header fixed top-0 left-0 right-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-[#E50914] flex items-center justify-center">
              <span className="font-['Barlow_Condensed'] font-black text-white text-lg">M</span>
            </div>
            <span className="font-['Barlow_Condensed'] font-bold text-xl tracking-tight text-white">MAVR</span>
          </Link>
          
          <nav className="flex items-center gap-6">
            {user ? (
              <Link 
                to="/dashboard" 
                className="bg-[#E50914] text-white px-6 py-2 font-['Barlow_Condensed'] font-bold uppercase tracking-widest hover:bg-[#B80710] transition-colors"
                data-testid="dashboard-btn"
              >
                Dashboard
              </Link>
            ) : (
              <>
                <Link 
                  to="/login" 
                  className="text-[#A1A1AA] hover:text-white transition-colors font-medium"
                  data-testid="login-link"
                >
                  Login
                </Link>
                <Link 
                  to="/register" 
                  className="bg-[#E50914] text-white px-6 py-2 font-['Barlow_Condensed'] font-bold uppercase tracking-widest hover:bg-[#B80710] transition-colors"
                  data-testid="get-started-btn"
                >
                  Get Started
                </Link>
              </>
            )}
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center pt-20">
        {/* Background */}
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{ 
            backgroundImage: `url('https://images.pexels.com/photos/35540076/pexels-photo-35540076.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940')`,
          }}
        >
          <div className="absolute inset-0 bg-[#0A0A0A]/80"></div>
        </div>
        
        <div className="relative z-10 max-w-5xl mx-auto px-6 text-center">
          <p className="overline mb-6 animate-fade-in">Athlete Operating System</p>
          
          <h1 className="font-['Barlow_Condensed'] text-5xl sm:text-6xl lg:text-8xl font-black uppercase tracking-tighter text-white mb-6 animate-slide-up">
            What Should You Do<br />
            <span className="text-[#E50914]">Today?</span>
          </h1>
          
          <p className="text-[#A1A1AA] text-lg sm:text-xl max-w-2xl mx-auto mb-10 animate-fade-in stagger-2" style={{ animationDelay: '0.2s' }}>
            MAVR gives you daily clarity. Personalized diet plans, workout programs, 
            readiness tracking, and progression analytics. Built for Indian athletes.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-fade-in stagger-3" style={{ animationDelay: '0.3s' }}>
            <Link 
              to="/register" 
              className="bg-[#E50914] text-white px-8 py-4 font-['Barlow_Condensed'] font-bold uppercase tracking-widest hover:bg-[#B80710] transition-all flex items-center gap-2 group"
              data-testid="hero-cta"
            >
              Start Free
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link 
              to="/login" 
              className="border border-[#262626] text-white px-8 py-4 font-['Barlow_Condensed'] font-bold uppercase tracking-widest hover:bg-[#1A1A1A] hover:border-white/40 transition-all"
            >
              I Have an Account
            </Link>
          </div>
        </div>
        
        {/* Scroll indicator */}
        <div className="absolute bottom-10 left-1/2 -translate-x-1/2">
          <div className="w-6 h-10 border-2 border-[#262626] rounded-full flex items-start justify-center p-2">
            <div className="w-1 h-2 bg-[#E50914] rounded-full animate-bounce"></div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-24 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <p className="overline mb-4">The System</p>
            <h2 className="font-['Barlow_Condensed'] text-3xl sm:text-4xl lg:text-5xl font-bold uppercase tracking-tight text-white">
              Assess. Prescribe. Execute. Track.
            </h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-1">
            {/* Feature Cards */}
            {[
              {
                icon: Target,
                title: "Athlete Classification",
                desc: "Rule-based assessment that classifies you as beginner, intermediate, advanced, or professional based on your actual training data."
              },
              {
                icon: Utensils,
                title: "Diet Engine",
                desc: "Budget-aware Indian diet plans. Practical meals you'll actually eat. Protein targets you can hit. No complicated restrictions."
              },
              {
                icon: Dumbbell,
                title: "Workout Engine",
                desc: "Structured workout programs based on your level, equipment, and goals. Clear sets, reps, and progression paths."
              },
              {
                icon: Activity,
                title: "Readiness Score",
                desc: "Know when to push and when to recover. Daily readiness scoring based on sleep, soreness, mood, and energy."
              },
              {
                icon: TrendingUp,
                title: "Progression Tracking",
                desc: "Weight trends, workout completion rates, adherence scores, strength gains. See exactly where you're improving."
              },
              {
                icon: Calendar,
                title: "Event Mode",
                desc: "Preparing for a competition, trial, or transformation? Event mode keeps you locked in with countdown tracking."
              }
            ].map((feature, i) => (
              <div 
                key={i}
                className="mavr-card group"
              >
                <feature.icon className="w-8 h-8 text-[#E50914] mb-4" />
                <h3 className="font-['Barlow_Condensed'] text-xl font-bold uppercase tracking-tight text-white mb-2">
                  {feature.title}
                </h3>
                <p className="text-[#A1A1AA] text-sm leading-relaxed">
                  {feature.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-6 relative">
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{ 
            backgroundImage: `url('https://images.pexels.com/photos/12201296/pexels-photo-12201296.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940')`,
          }}
        >
          <div className="absolute inset-0 bg-[#0A0A0A]/90"></div>
        </div>
        
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <p className="overline mb-4">Ready to Start?</p>
          <h2 className="font-['Barlow_Condensed'] text-3xl sm:text-4xl lg:text-5xl font-bold uppercase tracking-tight text-white mb-6">
            Your System is Waiting
          </h2>
          <p className="text-[#A1A1AA] text-lg mb-10">
            Join thousands of Indian athletes who stopped guessing and started performing.
          </p>
          <Link 
            to="/register" 
            className="inline-flex items-center gap-2 bg-[#E50914] text-white px-10 py-4 font-['Barlow_Condensed'] font-bold uppercase tracking-widest hover:bg-[#B80710] transition-all group"
            data-testid="bottom-cta"
          >
            Build With Intent
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[#262626] py-12 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 bg-[#E50914] flex items-center justify-center">
              <span className="font-['Barlow_Condensed'] font-black text-white text-sm">M</span>
            </div>
            <span className="font-['Barlow_Condensed'] font-bold text-lg tracking-tight text-white">MAVR</span>
          </div>
          
          <p className="text-[#71717A] text-sm">
            &copy; {new Date().getFullYear()} MAVR. Built for athletes.
          </p>
        </div>
      </footer>
    </div>
  );
}
