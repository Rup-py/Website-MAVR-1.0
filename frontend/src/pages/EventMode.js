import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../lib/api";
import { toast } from "sonner";
import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { ArrowLeft, Calendar, Target, Flame, X } from "lucide-react";

const EVENT_TYPES = [
  { value: "transformation", label: "Transformation Challenge", desc: "Body recomposition focus" },
  { value: "football_trial", label: "Football Trial", desc: "Sports tryout preparation" },
  { value: "fight_camp", label: "Fight Camp", desc: "Combat sports preparation" },
  { value: "marathon", label: "Marathon", desc: "Endurance event" },
  { value: "powerlifting", label: "Powerlifting Meet", desc: "Strength competition" },
  { value: "physique", label: "Physique Competition", desc: "Bodybuilding/physique show" },
  { value: "custom", label: "Custom Event", desc: "Your own goal" },
];

export default function EventMode() {
  const navigate = useNavigate();
  const [activeEvent, setActiveEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [showForm, setShowForm] = useState(false);

  const [formData, setFormData] = useState({
    event_name: "",
    event_type: "",
    event_date: "",
    target_weight: "",
    notes: "",
  });

  useEffect(() => {
    loadActiveEvent();
  }, []);

  const loadActiveEvent = async () => {
    try {
      const { data } = await api.getActiveEvent();
      setActiveEvent(data && Object.keys(data).length > 0 ? data : null);
    } catch (error) {
      console.error(error);
    }
    setLoading(false);
  };

  const handleCreate = async () => {
    if (!formData.event_name || !formData.event_type || !formData.event_date) {
      toast.error("Please fill in all required fields");
      return;
    }

    setCreating(true);
    try {
      await api.createEvent({
        event_name: formData.event_name,
        event_type: formData.event_type,
        event_date: formData.event_date,
        target_weight: formData.target_weight ? parseFloat(formData.target_weight) : null,
        notes: formData.notes || null,
      });
      toast.success("Event mode activated!");
      await loadActiveEvent();
      setShowForm(false);
    } catch (error) {
      toast.error("Failed to create event");
      console.error(error);
    }
    setCreating(false);
  };

  const calculateDaysLeft = (eventDate) => {
    const event = new Date(eventDate);
    const today = new Date();
    const diff = Math.ceil((event - today) / (1000 * 60 * 60 * 24));
    return diff > 0 ? diff : 0;
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
            <p className="overline text-xs">Focused Preparation</p>
            <h1 className="font-['Barlow_Condensed'] text-2xl font-bold uppercase tracking-tight text-white">
              Event Mode
            </h1>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        {activeEvent ? (
          // Active Event View
          <div className="space-y-6">
            {/* Event Hero */}
            <div 
              className="mavr-card relative overflow-hidden bg-cover bg-center min-h-[300px]"
              style={{ backgroundImage: `url('https://images.pexels.com/photos/12201296/pexels-photo-12201296.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940')` }}
              data-testid="active-event"
            >
              <div className="absolute inset-0 bg-[#0A0A0A]/80"></div>
              <div className="relative z-10 flex flex-col justify-center h-full p-8">
                <div className="flex items-center gap-2 mb-4">
                  <Flame className="w-6 h-6 text-[#E50914]" />
                  <span className="px-3 py-1 bg-[#E50914] text-white text-xs font-bold uppercase tracking-widest">
                    Active
                  </span>
                </div>
                
                <h2 className="font-['Barlow_Condensed'] text-4xl lg:text-5xl font-black uppercase text-white mb-2">
                  {activeEvent.event_name}
                </h2>
                
                <p className="text-[#A1A1AA] capitalize mb-6">
                  {activeEvent.event_type?.replace('_', ' ')}
                </p>
                
                <div className="flex items-baseline gap-2">
                  <span className="font-['Barlow_Condensed'] text-6xl lg:text-7xl font-black text-[#E50914]">
                    {calculateDaysLeft(activeEvent.event_date)}
                  </span>
                  <span className="text-2xl text-white">days left</span>
                </div>
              </div>
            </div>

            {/* Event Details */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="mavr-card">
                <div className="flex items-center gap-3 mb-2">
                  <Calendar className="w-5 h-5 text-[#E50914]" />
                  <p className="text-[#71717A] text-xs uppercase tracking-widest">Event Date</p>
                </div>
                <p className="text-white font-semibold">{activeEvent.event_date}</p>
              </div>
              
              <div className="mavr-card">
                <div className="flex items-center gap-3 mb-2">
                  <Target className="w-5 h-5 text-[#E50914]" />
                  <p className="text-[#71717A] text-xs uppercase tracking-widest">Target Weight</p>
                </div>
                <p className="text-white font-semibold">
                  {activeEvent.target_weight ? `${activeEvent.target_weight} kg` : "Not set"}
                </p>
              </div>
              
              <div className="mavr-card">
                <div className="flex items-center gap-3 mb-2">
                  <Calendar className="w-5 h-5 text-[#E50914]" />
                  <p className="text-[#71717A] text-xs uppercase tracking-widest">Started</p>
                </div>
                <p className="text-white font-semibold">{activeEvent.start_date}</p>
              </div>
            </div>

            {/* Notes */}
            {activeEvent.notes && (
              <div className="mavr-card">
                <p className="text-[#71717A] text-xs uppercase tracking-widest mb-2">Notes</p>
                <p className="text-[#A1A1AA]">{activeEvent.notes}</p>
              </div>
            )}

            {/* Focus Message */}
            <div className="mavr-card border-[#E50914]/30 bg-[#E50914]/5">
              <p className="text-white font-semibold mb-2">Stay Locked In</p>
              <p className="text-[#A1A1AA]">
                Event mode intensifies your tracking and accountability. Every check-in counts. 
                Every meal matters. Stay focused on the goal.
              </p>
            </div>
          </div>
        ) : showForm ? (
          // Create Event Form
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="font-['Barlow_Condensed'] text-2xl font-bold uppercase text-white">
                Create Event
              </h2>
              <button
                onClick={() => setShowForm(false)}
                className="text-[#71717A] hover:text-white"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            <div className="space-y-4">
              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Event Name</Label>
                <Input
                  value={formData.event_name}
                  onChange={(e) => setFormData(prev => ({ ...prev, event_name: e.target.value }))}
                  className="bg-[#121212] border-[#262626] text-white h-12 rounded-none"
                  placeholder="My Transformation"
                  data-testid="event-name"
                />
              </div>

              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Event Type</Label>
                <Select 
                  value={formData.event_type} 
                  onValueChange={(v) => setFormData(prev => ({ ...prev, event_type: v }))}
                >
                  <SelectTrigger className="bg-[#121212] border-[#262626] text-white h-12 rounded-none" data-testid="event-type">
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent className="bg-[#121212] border-[#262626]">
                    {EVENT_TYPES.map(type => (
                      <SelectItem key={type.value} value={type.value}>
                        {type.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Event Date</Label>
                <Input
                  type="date"
                  value={formData.event_date}
                  onChange={(e) => setFormData(prev => ({ ...prev, event_date: e.target.value }))}
                  className="bg-[#121212] border-[#262626] text-white h-12 rounded-none"
                  data-testid="event-date"
                />
              </div>

              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Target Weight (Optional)</Label>
                <Input
                  type="number"
                  value={formData.target_weight}
                  onChange={(e) => setFormData(prev => ({ ...prev, target_weight: e.target.value }))}
                  className="bg-[#121212] border-[#262626] text-white h-12 rounded-none"
                  placeholder="70"
                />
              </div>

              <div className="space-y-2">
                <Label className="text-[#A1A1AA] text-sm uppercase tracking-widest">Notes (Optional)</Label>
                <textarea
                  value={formData.notes}
                  onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
                  className="w-full bg-[#121212] border border-[#262626] text-white p-3 min-h-[100px] resize-none focus:border-[#E50914] focus:outline-none"
                  placeholder="What's your focus for this event?"
                />
              </div>

              <button
                onClick={handleCreate}
                disabled={creating}
                className="w-full py-4 bg-[#E50914] text-white font-['Barlow_Condensed'] font-bold uppercase tracking-widest hover:bg-[#B80710] transition-colors disabled:opacity-50"
                data-testid="create-event-btn"
              >
                {creating ? "Creating..." : "Activate Event Mode"}
              </button>
            </div>
          </div>
        ) : (
          // No Active Event
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-[#262626] rounded-full flex items-center justify-center mx-auto mb-6">
              <Calendar className="w-8 h-8 text-[#71717A]" />
            </div>
            <h2 className="font-['Barlow_Condensed'] text-2xl font-bold uppercase text-white mb-4">
              No Active Event
            </h2>
            <p className="text-[#A1A1AA] max-w-md mx-auto mb-8">
              Event Mode helps you prepare for competitions, trials, transformations, and other focused goals 
              with enhanced tracking and accountability.
            </p>
            <button
              onClick={() => setShowForm(true)}
              className="px-8 py-4 bg-[#E50914] text-white font-['Barlow_Condensed'] font-bold uppercase tracking-widest hover:bg-[#B80710] transition-colors"
              data-testid="start-event-btn"
            >
              Create Event
            </button>

            {/* Event Types */}
            <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
              {EVENT_TYPES.map(type => (
                <div key={type.value} className="mavr-card">
                  <p className="text-white font-semibold">{type.label}</p>
                  <p className="text-[#71717A] text-sm">{type.desc}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
