
import sys
import os
import uuid
from datetime import date
from fastapi.testclient import TestClient

# Add project root to sys.path
sys.path.append(os.getcwd())

from src.main import app
from src.db.session import SessionLocal
from src.users.models import User
from src.employees.models import Employee
from src.users import utils
from src.users.dependencies import get_current_user

# Setup
client = TestClient(app)
db = SessionLocal()

def create_test_user(email, role="EMPLOYEE"):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            full_name="Test User",
            password_hash=utils.get_password_hash("password"),
            role=role,
            company="Test Corp"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

def create_test_employee(user):
    employee = db.query(Employee).filter(Employee.user_id == user.id).first()
    if not employee:
        employee = Employee(
            id=uuid.uuid4(),
            user_id=user.id,
            job_title="Software Engineer",
            department="Engineering",
            base_salary=50000.0,
            date_of_joining=date.today()
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)
    return employee

def override_dependency(user):
    app.dependency_overrides[get_current_user] = lambda: user

def test_leave_flow():
    print("Setting up test data...")
    admin_email = f"admin_{uuid.uuid4()}@example.com"
    emp_email = f"emp_{uuid.uuid4()}@example.com"
    
    admin_user = create_test_user(admin_email, "ADMIN")
    emp_user = create_test_user(emp_email, "EMPLOYEE")
    employee_profile = create_test_employee(emp_user)
    
    print(f"Created Admin: {admin_user.email}")
    print(f"Created Employee: {emp_user.email}")

    # 1. Create Leave Type (as Admin)
    print("\n[1] Creating Leave Type as Admin...")
    override_dependency(admin_user)
    leave_type_name = f"Sick Leave {uuid.uuid4()}"
    response = client.post("/api/v1/leave/types", json={
        "name": leave_type_name,
        "is_paid": True
    })
    print(f"Response: {response.status_code} {response.json()}")
    assert response.status_code == 201
    leave_type_id = response.json()["id"]

    # 2. Get Leave Types
    print("\n[2] Fetching Leave Types...")
    response = client.get("/api/v1/leave/types")
    print(f"Response: {response.status_code} Count: {len(response.json())}")
    assert response.status_code == 200
    assert any(lt["id"] == leave_type_id for lt in response.json())

    # 3. Create Leave Request (as Employee)
    print("\n[3] Creating Leave Request as Employee...")
    override_dependency(emp_user)
    leave_data = {
        "leave_type_id": leave_type_id,
        "start_date": str(date.today()),
        "end_date": str(date.today()),
        "remarks": "Feeling unwell"
    }
    response = client.post("/api/v1/leave/requests", json=leave_data)
    print(f"Response: {response.status_code} {response.json()}")
    assert response.status_code == 201
    leave_request_id = response.json()["id"]
    assert response.json()["status"] == "PENDING"

    # 4. Approve Leave Request (as Admin)
    print("\n[4] Approving Leave Request as Admin...")
    override_dependency(admin_user)
    update_data = {
        "status": "APPROVED",
        "review_comment": "Get well soon"
    }
    response = client.patch(f"/api/v1/leave/requests/{leave_request_id}", json=update_data)
    print(f"Response: {response.status_code} {response.json()}")
    assert response.status_code == 200
    assert response.json()["status"] == "APPROVED"
    assert response.json()["reviewed_by"] == admin_user.id

    print("\nSUCCESS: Leave flow verification completed!")

if __name__ == "__main__":
    try:
        test_leave_flow()
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
