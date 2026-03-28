# MAVR - Athlete Operating System

## Original Problem Statement
Build a production-ready MVP for a SaaS athlete ecosystem called MAVR. MAVR is a SaaS athlete operating system for Indian users from beginner to professional. The core product is the dashboard and athlete engine with personalized diet plans, workout programs, daily checklists, readiness scoring, streak tracking, progression analytics, and event mode.

## Architecture

### Tech Stack
- **Frontend**: React 18 with Tailwind CSS, Shadcn UI components
- **Backend**: FastAPI with modular service architecture
- **Database**: MongoDB with proper indexing
- **AI**: GPT-5.2 via Emergent LLM Key (hybrid rule-based + AI)
- **Auth**: JWT with httpOnly cookies

### Backend Modules
```
/app/backend/
├── models/          # Pydantic models
│   ├── user.py      # User, Profile, Athlete Level
│   ├── diet.py      # Diet plans, meals, foods
│   ├── workout.py   # Workout plans, exercises
│   ├── tracking.py  # Check-ins, readiness, streaks
│   ├── event_commerce.py  # Events, clothing, products
│   └── notification.py    # Notifications
├── services/        # Business logic
│   ├── classification_service.py  # Rule-based athlete classification
│   ├── calorie_service.py         # TDEE, BMR, macro calculations
│   ├── diet_engine.py             # Diet plan generation
│   ├── workout_engine.py          # Workout plan generation
│   ├── readiness_engine.py        # Readiness scoring
│   ├── streak_engine.py           # Streak management
│   ├── ai_service.py              # AI personalization layer
│   ├── notification_service.py    # Email/WhatsApp abstractions
│   ├── payment_service.py         # Razorpay abstraction
│   └── clothing_engine.py         # Body stage recommendations
└── server.py        # Main FastAPI application with routes
```

### Frontend Pages
```
/app/frontend/src/pages/
├── Landing.js       # Marketing page
├── Login.js         # Auth - login
├── Register.js      # Auth - register
├── Onboarding.js    # 6-step onboarding wizard
├── Dashboard.js     # Main command center
├── DietPlan.js      # Daily diet plan view
├── WorkoutPlan.js   # Daily workout plan view
├── Checkin.js       # Morning/Workout/Night check-ins
├── Progression.js   # Analytics & charts
├── EventMode.js     # Event preparation
├── Admin.js         # Admin dashboard
└── Profile.js       # User profile
```

## User Personas
1. **Beginner Athlete**: New to fitness, needs guidance on basics
2. **Intermediate Athlete**: 1-2 years training, wants structured progression
3. **Advanced Athlete**: 3+ years, needs periodization and event prep
4. **Professional**: Competition-level, needs peak performance tools

## Core Requirements (Static)
1. JWT-based authentication
2. Multi-step onboarding assessment
3. Rule-based athlete classification (beginner/intermediate/advanced/pro)
4. Personalized diet plans based on Indian foods and budget
5. Structured workout programs based on equipment and goals
6. Daily check-in system (morning/workout/night)
7. Readiness scoring with push/maintain/recover guidance
8. Streak tracking with milestone achievements
9. Progression analytics with weight trends
10. Event mode for focused preparation
11. Admin dashboard with analytics

## What's Been Implemented (2026-03-28)

### Backend (100% Complete)
- [x] Auth system (JWT with refresh tokens)
- [x] User registration and login
- [x] Onboarding endpoint with classification
- [x] Diet engine with Indian food database
- [x] Workout engine with gym/home exercises
- [x] Morning/Workout/Night check-in endpoints
- [x] Readiness score calculation
- [x] Streak management
- [x] Progression tracking
- [x] Weekly reports with AI insights
- [x] Event mode CRUD
- [x] Admin endpoints (users, analytics)
- [x] AI integration (GPT-5.2 for personalized guidance)
- [x] Payment abstraction (Razorpay-ready)
- [x] Email abstraction (Resend-ready)
- [x] WhatsApp abstraction (Meta API-ready)

### Frontend (100% Complete)
- [x] Landing page with branding
- [x] Login/Register pages
- [x] 6-step onboarding wizard
- [x] Dashboard command center
- [x] Daily checklist with tick-boxes
- [x] Diet plan view with meal expansion
- [x] Workout plan view with exercise details
- [x] Check-in forms (all 3 types)
- [x] Progression charts with recharts
- [x] Event mode creation/view
- [x] Admin panel with tabs
- [x] Profile page

## Prioritized Backlog

### P0 (Critical - Next Sprint)
- [ ] Test full onboarding → dashboard flow with real user
- [ ] Add sample workout/diet data for demo
- [ ] Mobile responsive polish

### P1 (Important)
- [ ] Razorpay integration (when keys provided)
- [ ] Resend email integration (when keys provided)
- [ ] WhatsApp Meta API integration (when credentials)
- [ ] Exercise video links
- [ ] Strength progression tracking (1RM)

### P2 (Nice to Have)
- [ ] Social auth (Google OAuth)
- [ ] Dark/light theme toggle
- [ ] Push notifications
- [ ] Export data (CSV/PDF)
- [ ] Multi-language (Hindi)

## Next Tasks
1. Run full user flow test: Register → Onboard → Dashboard → Check-ins
2. Add sample data seeding for demo
3. Polish mobile responsiveness
4. Add loading skeletons
5. Implement clothing recommendation card on dashboard

## API Endpoints Summary
```
Auth:
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/me
POST /api/auth/refresh

Onboarding:
POST /api/onboarding/save
GET  /api/onboarding/profile

Dashboard:
GET  /api/dashboard

Diet:
GET  /api/diet/today
GET  /api/diet/history

Workout:
GET  /api/workout/today
POST /api/workout/log

Check-ins:
POST /api/checkin/morning
POST /api/checkin/workout
POST /api/checkin/night

Progression:
GET  /api/progression/summary

Events:
POST /api/event/create
GET  /api/event/active
POST /api/event/{id}/deactivate

Reports:
GET  /api/reports/weekly

Admin:
GET  /api/admin/users
GET  /api/admin/analytics
GET  /api/admin/user/{id}
```
