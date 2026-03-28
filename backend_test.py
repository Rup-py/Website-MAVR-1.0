#!/usr/bin/env python3
"""
MAVR Backend API Testing Suite
Tests all endpoints for the athlete operating system
"""
import requests
import json
import sys
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class MAVRAPITester:
    def __init__(self, base_url: str = "https://athlete-engine.preview.emergentagent.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.admin_token = None
        self.user_token = None
        self.user_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test result"""
        self.tests_run += 1
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
        if details:
            print(f"    {details}")
        if success:
            self.tests_passed += 1
        else:
            self.failed_tests.append(f"{name}: {details}")
        print()

    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                    headers: Optional[Dict] = None, expected_status: int = 200) -> tuple:
        """Make HTTP request and return success status and response"""
        url = f"{self.base_url}/api/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, headers=headers)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, headers=headers)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=headers)
            else:
                return False, {"error": f"Unsupported method: {method}"}

            success = response.status_code == expected_status
            try:
                response_data = response.json()
            except:
                response_data = {"text": response.text, "status_code": response.status_code}
            
            return success, response_data

        except Exception as e:
            return False, {"error": str(e)}

    def test_health_check(self):
        """Test basic health endpoints"""
        print("🔍 Testing Health Check Endpoints...")
        
        # Test root endpoint
        success, data = self.make_request("GET", "/")
        self.log_test("Root endpoint (/api/)", success, 
                     f"Response: {data.get('message', 'No message')}" if success else f"Error: {data}")
        
        # Test health endpoint
        success, data = self.make_request("GET", "/health")
        self.log_test("Health check (/api/health)", success,
                     f"Status: {data.get('status', 'Unknown')}" if success else f"Error: {data}")

    def test_admin_auth(self):
        """Test admin authentication"""
        print("🔍 Testing Admin Authentication...")
        
        # Admin login
        admin_data = {
            "email": "admin@mavr.com",
            "password": "MavrAdmin123!"
        }
        
        success, data = self.make_request("POST", "/auth/login", admin_data)
        if success and data.get("role") == "admin":
            self.admin_token = self.session.cookies.get("access_token")
            self.log_test("Admin login", True, f"Admin user: {data.get('name')}")
        else:
            self.log_test("Admin login", False, f"Failed: {data}")
            return False
        
        # Test admin /auth/me
        success, data = self.make_request("GET", "/auth/me")
        self.log_test("Admin /auth/me", success and data.get("role") == "admin",
                     f"Role: {data.get('role')}" if success else f"Error: {data}")
        
        return True

    def test_user_registration_and_auth(self):
        """Test user registration and authentication"""
        print("🔍 Testing User Registration & Authentication...")
        
        # Generate unique test user
        timestamp = datetime.now().strftime("%H%M%S")
        test_user = {
            "name": f"Test User {timestamp}",
            "email": f"testuser{timestamp}@mavr.com",
            "password": "TestPass123!"
        }
        
        # User registration
        success, data = self.make_request("POST", "/auth/register", test_user)
        if success:
            self.user_id = data.get("id")
            self.user_token = self.session.cookies.get("access_token")
            self.log_test("User registration", True, f"User ID: {self.user_id}")
        else:
            self.log_test("User registration", False, f"Error: {data}")
            return False
        
        # Test user /auth/me
        success, data = self.make_request("GET", "/auth/me")
        self.log_test("User /auth/me", success and data.get("role") == "user",
                     f"User: {data.get('name')}" if success else f"Error: {data}")
        
        # Test logout
        success, data = self.make_request("POST", "/auth/logout")
        self.log_test("User logout", success, "Logged out successfully" if success else f"Error: {data}")
        
        # Test login again
        login_data = {"email": test_user["email"], "password": test_user["password"]}
        success, data = self.make_request("POST", "/auth/login", login_data)
        if success:
            self.user_token = self.session.cookies.get("access_token")
            self.log_test("User login", True, f"Logged in as: {data.get('name')}")
        else:
            self.log_test("User login", False, f"Error: {data}")
            return False
        
        return True

    def test_onboarding_system(self):
        """Test onboarding and profile system"""
        print("🔍 Testing Onboarding System...")
        
        # Sample profile data
        profile_data = {
            "profile_data": {
                "age": 25,
                "gender": "male",
                "height_cm": 175.0,
                "weight_kg": 70.0,
                "target_weight_kg": 65.0,
                "goal": "fat_loss",
                "training_age_months": 12,
                "workout_frequency": 4,
                "preferred_workout_days": ["monday", "wednesday", "friday", "sunday"],
                "workout_setup": "gym",
                "available_equipment": ["barbell", "dumbbells", "bench"],
                "sleep_hours": 7.0,
                "stress_level": 5,
                "activity_level": "moderately_active",
                "diet_preference": "non_vegetarian",
                "meal_frequency": 4,
                "budget_level": "medium"
            }
        }
        
        # Save onboarding
        success, data = self.make_request("POST", "/onboarding/save", profile_data)
        if success:
            athlete_level = data.get("athlete_level")
            target_calories = data.get("target_calories")
            self.log_test("Onboarding save", True, 
                         f"Athlete level: {athlete_level}, Target calories: {target_calories}")
        else:
            self.log_test("Onboarding save", False, f"Error: {data}")
            return False
        
        # Get profile
        success, data = self.make_request("GET", "/onboarding/profile")
        self.log_test("Get profile", success, 
                     f"Profile exists: {bool(data)}" if success else f"Error: {data}")
        
        return True

    def test_dashboard_data(self):
        """Test dashboard data retrieval"""
        print("🔍 Testing Dashboard Data...")
        
        success, data = self.make_request("GET", "/dashboard")
        if success:
            user_info = data.get("user", {})
            profile_info = data.get("profile", {})
            checklist = data.get("checklist", {})
            self.log_test("Dashboard data", True, 
                         f"User: {user_info.get('name')}, Athlete level: {user_info.get('athlete_level')}")
        else:
            self.log_test("Dashboard data", False, f"Error: {data}")

    def test_diet_system(self):
        """Test diet plan system"""
        print("🔍 Testing Diet System...")
        
        # Get today's diet plan
        success, data = self.make_request("GET", "/diet/today")
        if success:
            meals_count = len(data.get("meals", []))
            target_calories = data.get("target_calories")
            self.log_test("Today's diet plan", True, 
                         f"Meals: {meals_count}, Target calories: {target_calories}")
        else:
            self.log_test("Today's diet plan", False, f"Error: {data}")
        
        # Get diet history
        success, data = self.make_request("GET", "/diet/history?days=7")
        self.log_test("Diet history", success, 
                     f"History entries: {len(data) if isinstance(data, list) else 0}" if success else f"Error: {data}")

    def test_workout_system(self):
        """Test workout plan system"""
        print("🔍 Testing Workout System...")
        
        # Get today's workout plan
        success, data = self.make_request("GET", "/workout/today")
        if success:
            if data.get("rest_day"):
                self.log_test("Today's workout plan", True, "Rest day scheduled")
            else:
                session = data.get("session", {})
                workout_name = session.get("name", "Unknown")
                duration = session.get("estimated_duration_mins", 0)
                self.log_test("Today's workout plan", True, 
                             f"Workout: {workout_name}, Duration: {duration} mins")
        else:
            self.log_test("Today's workout plan", False, f"Error: {data}")

    def test_checkin_system(self):
        """Test daily checkin system"""
        print("🔍 Testing Check-in System...")
        
        # Morning checkin
        morning_data = {
            "weight_kg": 69.5,
            "sleep_hours": 7.5,
            "sleep_quality": 8,
            "soreness_level": 3,
            "mood": 8,
            "energy": 7,
            "notes": "Feeling good today"
        }
        
        success, data = self.make_request("POST", "/checkin/morning", morning_data)
        if success:
            readiness = data.get("readiness", {})
            streak = data.get("streak", {})
            self.log_test("Morning checkin", True, 
                         f"Readiness score: {readiness.get('score')}, Streak: {streak.get('current_streak')}")
        else:
            self.log_test("Morning checkin", False, f"Error: {data}")
        
        # Workout checkin
        workout_data = {
            "workout_completed": True,
            "session_intensity": 8,
            "notes": "Great workout session"
        }
        
        success, data = self.make_request("POST", "/checkin/workout", workout_data)
        self.log_test("Workout checkin", success, 
                     "Workout logged" if success else f"Error: {data}")
        
        # Night checkin
        night_data = {
            "protein_target_hit": True,
            "water_target_hit": True,
            "steps_completed": True,
            "steps_count": 8500,
            "diet_adherence": 9,
            "calories_consumed": 2200,
            "reflections": "Good day overall"
        }
        
        success, data = self.make_request("POST", "/checkin/night", night_data)
        self.log_test("Night checkin", success, 
                     "Night checkin saved" if success else f"Error: {data}")

    def test_progression_system(self):
        """Test progression analytics"""
        print("🔍 Testing Progression System...")
        
        success, data = self.make_request("GET", "/progression/summary?days=30")
        if success:
            workout_rate = data.get("workout_completion_rate", 0)
            protein_rate = data.get("protein_adherence_rate", 0)
            self.log_test("Progression summary", True, 
                         f"Workout completion: {workout_rate}%, Protein adherence: {protein_rate}%")
        else:
            self.log_test("Progression summary", False, f"Error: {data}")

    def test_event_system(self):
        """Test event mode system"""
        print("🔍 Testing Event System...")
        
        # Create event
        event_data = {
            "event_name": "Summer Beach Body",
            "event_type": "personal",
            "event_date": (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"),
            "target_weight": 65.0,
            "notes": "Getting ready for summer"
        }
        
        success, data = self.make_request("POST", "/event/create", event_data)
        if success:
            event_id = data.get("event_id")
            self.log_test("Create event", True, f"Event ID: {event_id}")
        else:
            self.log_test("Create event", False, f"Error: {data}")
        
        # Get active event
        success, data = self.make_request("GET", "/event/active")
        self.log_test("Get active event", success, 
                     f"Event: {data.get('event_name', 'None')}" if success else f"Error: {data}")

    def test_admin_endpoints(self):
        """Test admin-only endpoints"""
        print("🔍 Testing Admin Endpoints...")
        
        # Switch to admin session
        if not self.admin_token:
            self.test_admin_auth()
        
        # Get users list
        success, data = self.make_request("GET", "/admin/users?limit=10")
        if success:
            users = data.get("users", [])
            total = data.get("total", 0)
            self.log_test("Admin get users", True, f"Users: {len(users)}, Total: {total}")
        else:
            self.log_test("Admin get users", False, f"Error: {data}")
        
        # Get analytics
        success, data = self.make_request("GET", "/admin/analytics")
        if success:
            total_users = data.get("total_users", 0)
            onboarded = data.get("onboarded_users", 0)
            self.log_test("Admin analytics", True, 
                         f"Total users: {total_users}, Onboarded: {onboarded}")
        else:
            self.log_test("Admin analytics", False, f"Error: {data}")

    def test_weekly_reports(self):
        """Test weekly reports"""
        print("🔍 Testing Weekly Reports...")
        
        success, data = self.make_request("GET", "/reports/weekly")
        if success:
            workouts = data.get("workouts_completed", 0)
            adherence = data.get("adherence_score", 0)
            self.log_test("Weekly report", True, 
                         f"Workouts: {workouts}, Adherence: {adherence}%")
        else:
            self.log_test("Weekly report", False, f"Error: {data}")

    def run_all_tests(self):
        """Run complete test suite"""
        print("🚀 Starting MAVR Backend API Tests")
        print("=" * 50)
        
        # Test sequence
        self.test_health_check()
        
        if self.test_admin_auth():
            self.test_admin_endpoints()
        
        if self.test_user_registration_and_auth():
            self.test_onboarding_system()
            self.test_dashboard_data()
            self.test_diet_system()
            self.test_workout_system()
            self.test_checkin_system()
            self.test_progression_system()
            self.test_event_system()
            self.test_weekly_reports()
        
        # Final results
        print("=" * 50)
        print(f"🏁 Test Results: {self.tests_passed}/{self.tests_run} passed")
        
        if self.failed_tests:
            print("\n❌ Failed Tests:")
            for failure in self.failed_tests:
                print(f"  - {failure}")
        
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        print(f"\n📊 Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 80  # Consider 80%+ as passing

def main():
    """Main test execution"""
    tester = MAVRAPITester()
    success = tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())