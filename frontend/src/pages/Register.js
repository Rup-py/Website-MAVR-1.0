import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Eye, EyeOff } from "lucide-react";

export default function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    
    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }
    
    setLoading(true);

    const result = await register(name, email, password);
    
    if (result.success) {
      navigate("/onboarding");
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
            backgroundImage: `url('https://images.pexels.com/photos/35540076/pexels-photo-35540076.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940')`,
          }}
        >
          <div className="absolute inset-0 bg-[#0A0A0A]/70"></div>
        </div>
        <div className="relative z-10 flex flex-col justify-end p-12">
          <h2 className="font-['Barlow_Condensed'] text-4xl font-bold uppercase tracking-tight text-white mb-4">
            Build With Intent
          </h2>
          <p className="text-[#A1A1AA] max-w-md">
            Join thousands of Indian athletes who stopped guessing and started performing with MAVR.
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
            <p className="overline mb-2">Get Started</p>
            <h1 className="font-['Barlow_Condensed'] text-3xl sm:text-4xl font-bold uppercase tracking-tight text-white">
              Create Account
            </h1>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-[#E50914]/10 border border-[#E50914] p-4 text-[#E50914] text-sm" data-testid="register-error">
                {error}
              </div>
            )}

            <div className="space-y-2">
              <Label htmlFor="name" className="text-[#A1A1AA] text-sm uppercase tracking-widest">
                Full Name
              </Label>
              <Input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="bg-[#121212] border-[#262626] text-white h-12 rounded-none focus:border-[#E50914]"
                placeholder="Your Name"
                required
                data-testid="register-name"
              />
            </div>

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
                data-testid="register-email"
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
                  placeholder="Min 6 characters"
                  required
                  data-testid="register-password"
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
              data-testid="register-submit"
            >
              {loading ? "Creating Account..." : "Create Account"}
            </button>
          </form>

          <p className="mt-8 text-center text-[#71717A]">
            Already have an account?{" "}
            <Link to="/login" className="text-[#E50914] hover:underline" data-testid="login-link">
              Sign In
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
