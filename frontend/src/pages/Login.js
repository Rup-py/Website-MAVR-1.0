import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Eye, EyeOff } from "lucide-react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const result = await login(email, password);
    
    if (result.success) {
      if (!result.data.onboarding_completed) {
        navigate("/onboarding");
      } else {
        navigate("/dashboard");
      }
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-[#0A0A0A] flex">
      {/* Left side - Image */}
      <div className="hidden lg:flex lg:w-1/2 relative">
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{ 
            backgroundImage: `url('https://images.pexels.com/photos/12201296/pexels-photo-12201296.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940')`,
          }}
        >
          <div className="absolute inset-0 bg-[#0A0A0A]/70"></div>
        </div>
        <div className="relative z-10 flex flex-col justify-end p-12">
          <h2 className="font-['Barlow_Condensed'] text-4xl font-bold uppercase tracking-tight text-white mb-4">
            Stay Locked In
          </h2>
          <p className="text-[#A1A1AA] max-w-md">
            Your dashboard is waiting. Daily plans, check-ins, and progression tracking — all in one place.
          </p>
        </div>
      </div>

      {/* Right side - Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-md">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 mb-12">
            <div className="w-8 h-8 bg-[#E50914] flex items-center justify-center">
              <span className="font-['Barlow_Condensed'] font-black text-white text-lg">M</span>
            </div>
            <span className="font-['Barlow_Condensed'] font-bold text-xl tracking-tight text-white">MAVR</span>
          </Link>

          <div className="mb-8">
            <p className="overline mb-2">Welcome Back</p>
            <h1 className="font-['Barlow_Condensed'] text-3xl sm:text-4xl font-bold uppercase tracking-tight text-white">
              Sign In
            </h1>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-[#E50914]/10 border border-[#E50914] p-4 text-[#E50914] text-sm" data-testid="login-error">
                {error}
              </div>
            )}

            <div className="space-y-2">
              <Label htmlFor="email" className="text-[#A1A1AA] text-sm uppercase tracking-widest">
                Email
              </Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="bg-[#121212] border-[#262626] text-white h-12 rounded-none focus:border-[#E50914]"
                placeholder="you@email.com"
                required
                data-testid="login-email"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password" className="text-[#A1A1AA] text-sm uppercase tracking-widest">
                Password
              </Label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="bg-[#121212] border-[#262626] text-white h-12 rounded-none focus:border-[#E50914] pr-12"
                  placeholder="••••••••"
                  required
                  data-testid="login-password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-[#71717A] hover:text-white"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-[#E50914] text-white h-12 font-['Barlow_Condensed'] font-bold uppercase tracking-widest hover:bg-[#B80710] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              data-testid="login-submit"
            >
              {loading ? "Signing In..." : "Sign In"}
            </button>
          </form>

          <p className="mt-8 text-center text-[#71717A]">
            Don't have an account?{" "}
            <Link to="/register" className="text-[#E50914] hover:underline" data-testid="register-link">
              Get Started
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
