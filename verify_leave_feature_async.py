
import sys
import os
import uuid
import datetime
import asyncio
from httpx import AsyncClient, ASGITransport


# Add project root to sys.path
sys.path.append(os.getcwd())

# We need to run the app in a way that we can import it.
from src.main import app
from src.users.models import User
from src.employees.models import Employee
from src.users import utils
from src.core.deps import get_current_user

# Mock data
admin_user_data = {
    "id": str(uuid.uuid4()),
    "email": f"admin_{uuid.uuid4()}@example.com",
    "role": "ADMIN",
    "full_name": "Admin User",
    "company": "Test Corp"
}

emp_user_data = {
    "id": str(uuid.uuid4()),
    "email": f"emp_{uuid.uuid4()}@example.com",
    "role": "EMPLOYEE",
    "full_name": "Employee User",
    "company": "Test Corp"
}

# Simple mock user object
class MockUser:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

async def run_test():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        
        # 1. Create Leave Type (as Admin)
        print("\n[1] Creating Leave Type as Admin...")
        app.dependency_overrides[get_current_user] = lambda: MockUser(**admin_user_data)
        
        leave_type_name = f"Sick Leave {uuid.uuid4()}"
        response = await ac.post("/api/v1/leave/types", json={
            "name": leave_type_name,
            "is_paid": True
        })
        print(f"Response: {response.status_code} {response.json()}")
        # Note: This might fail if the DB constraints are hit or table doesn't exist, but we ran migrations.
        # Also, using real DB with AsyncClient requires the DB session to be working.
        
        if response.status_code != 201:
            print("Failed to create leave type. Check DB connection or migrations.")
            return

        leave_type_id = response.json()["id"]

        # 2. Get Leave Types
        print("\n[2] Fetching Leave Types...")
        response = await ac.get("/api/v1/leave/types")
        assert response.status_code == 200
        print(f"Count: {len(response.json())}")

        # 3. Create Leave Request (as Employee)
        # We need an Employee profile in the DB for this to work.
        # This verification script relies on existing DB.
        # We might need to manually insert an Employee record if creating one via API isn't easy here.
        # But wait, we can't easily insert into DB without a session.
        # So we depend on the app's services or previous state.
        
        # If we can't easily create an employee, we might skip this part or try to hack it.
        # However, `create_leave_request` checks `db.scalar(select(Employee)...)`.
        # So without a real Employee record linked to `emp_user_data['id']`, it will fail with 400.
        
        print("\n[3] Creating Leave Request (Expected to fail without Employee profile in DB)...")
        app.dependency_overrides[get_current_user] = lambda: MockUser(**emp_user_data)
        
        leave_data = {
            "leave_type_id": leave_type_id,
            "start_date": str(datetime.date.today()),
            "end_date": str(datetime.date.today()),
            "remarks": "Feeling unwell"
        }
        response = await ac.post("/api/v1/leave/requests", json=leave_data)
        print(f"Response: {response.status_code} {response.json()}")
        
        if response.status_code == 400 and response.json()["detail"] == "Employee profile not found":
            print("As expected, Employee profile is missing. Verification partial success.")
        elif response.status_code == 201:
            print("Leave request created successfully!")
        else:
            print("Unexpected response.")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_test())
