# HRMS API - Dayflow

A comprehensive Human Resource Management System (HRMS) API built with FastAPI, featuring employee management, attendance tracking, payroll, and leave management.

## Features

- **User Management** - Authentication and authorization with JWT tokens
- **Employee Management** - Employee profiles with job details
- **Attendance Tracking** - Check-in/check-out with automatic working hours calculation
- **Payroll Management** - Salary structures and slip generation
- **Leave Management** - Leave requests and approvals

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Migrations**: Alembic
- **Package Management**: UV

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hrms-api-odoo-hack
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   uv pip install -e .
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/hrms_db
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn src.main:app --reload
   ```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI) will be at `http://localhost:8000/docs`

## API Endpoints

### Authentication

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=yourpassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Attendance Management

All attendance endpoints require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <your-access-token>
```

#### Employee Endpoints

##### Check In
```http
POST /api/v1/attendance/check-in
Authorization: Bearer <token>
Content-Type: application/json

{}
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "employee_id": "123e4567-e89b-12d3-a456-426614174001",
  "work_date": "2026-01-03",
  "check_in": "2026-01-03T09:00:00+00:00",
  "check_out": null,
  "status": "PRESENT",
  "created_at": "2026-01-03T09:00:00+00:00"
}
```

**Error Cases:**
- `400 Bad Request` - Already checked in today
- `400 Bad Request` - Employee profile not found
- `401 Unauthorized` - Invalid or missing token

##### Check Out
```http
POST /api/v1/attendance/check-out
Authorization: Bearer <token>
Content-Type: application/json

{}
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "employee_id": "123e4567-e89b-12d3-a456-426614174001",
  "work_date": "2026-01-03",
  "check_in": "2026-01-03T09:00:00+00:00",
  "check_out": "2026-01-03T17:30:00+00:00",
  "status": "PRESENT",
  "created_at": "2026-01-03T09:00:00+00:00"
}
```

**Note:** If working hours < 4 hours, status automatically changes to `HALF_DAY`

**Error Cases:**
- `400 Bad Request` - No check-in record found
- `400 Bad Request` - Already checked out today

##### Get My Attendance History
```http
GET /api/v1/attendance/me
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "employee_id": "123e4567-e89b-12d3-a456-426614174001",
    "work_date": "2026-01-03",
    "check_in": "2026-01-03T09:00:00+00:00",
    "check_out": "2026-01-03T17:30:00+00:00",
    "status": "PRESENT",
    "created_at": "2026-01-03T09:00:00+00:00"
  },
  {
    "id": "123e4567-e89b-12d3-a456-426614174002",
    "employee_id": "123e4567-e89b-12d3-a456-426614174001",
    "work_date": "2026-01-02",
    "check_in": "2026-01-02T09:15:00+00:00",
    "check_out": "2026-01-02T13:00:00+00:00",
    "status": "HALF_DAY",
    "created_at": "2026-01-02T09:15:00+00:00"
  }
]
```

#### Admin Endpoints

All admin endpoints require admin role. Returns `403 Forbidden` for non-admin users.

##### View Employee Attendance (with Working Hours)
```http
GET /api/v1/attendance/employees/{employee_id}?start_date=2026-01-01&end_date=2026-01-31
Authorization: Bearer <admin-token>
```

**Query Parameters:**
- `start_date` (optional) - Start date in YYYY-MM-DD format. Defaults to 30 days before end_date
- `end_date` (optional) - End date in YYYY-MM-DD format. Defaults to today

**Response:**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "employee_id": "123e4567-e89b-12d3-a456-426614174001",
    "work_date": "2026-01-03",
    "check_in": "2026-01-03T09:00:00+00:00",
    "check_out": "2026-01-03T17:30:00+00:00",
    "status": "PRESENT",
    "created_at": "2026-01-03T09:00:00+00:00",
    "working_hours": 8.5
  }
]
```

##### View All Employees Attendance by Date
```http
GET /api/v1/attendance/daily/2026-01-03
Authorization: Bearer <admin-token>
```

**Response:**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "employee_id": "123e4567-e89b-12d3-a456-426614174001",
    "work_date": "2026-01-03",
    "check_in": "2026-01-03T09:00:00+00:00",
    "check_out": "2026-01-03T17:30:00+00:00",
    "status": "PRESENT",
    "created_at": "2026-01-03T09:00:00+00:00"
  },
  {
    "id": "123e4567-e89b-12d3-a456-426614174003",
    "employee_id": "123e4567-e89b-12d3-a456-426614174004",
    "work_date": "2026-01-03",
    "check_in": "2026-01-03T08:45:00+00:00",
    "check_out": null,
    "status": "PRESENT",
    "created_at": "2026-01-03T08:45:00+00:00"
  }
]
```

##### Manually Update Attendance
```http
PUT /api/v1/attendance/{attendance_id}
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "check_in": "2026-01-03T09:00:00+00:00",
  "check_out": "2026-01-03T17:00:00+00:00",
  "status": "PRESENT"
}
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "employee_id": "123e4567-e89b-12d3-a456-426614174001",
  "work_date": "2026-01-03",
  "check_in": "2026-01-03T09:00:00+00:00",
  "check_out": "2026-01-03T17:00:00+00:00",
  "status": "PRESENT",
  "created_at": "2026-01-03T09:00:00+00:00"
}
```

**Error Cases:**
- `404 Not Found` - Attendance record not found
- `403 Forbidden` - User is not an admin

### Attendance Status Types

- `PRESENT` - Employee checked in and worked full day (≥ 4 hours)
- `HALF_DAY` - Employee worked less than 4 hours
- `ABSENT` - Employee did not check in
- `LEAVE` - Employee on approved leave

## Database Schema

### attendance_records

| Column      | Type      | Description                        |
|-------------|-----------|-----------------------------------|
| id          | UUID      | Primary key                       |
| employee_id | UUID      | Foreign key to employees table    |
| work_date   | Date      | Date of attendance                |
| check_in    | Timestamp | Check-in time (UTC)               |
| check_out   | Timestamp | Check-out time (UTC)              |
| status      | String    | PRESENT/ABSENT/HALF_DAY/LEAVE     |
| created_at  | Timestamp | Record creation timestamp         |

**Constraints:**
- Unique constraint on (employee_id, work_date) - One record per employee per day
- Index on (employee_id, work_date) for fast queries

## Development

### Running Tests
```bash
pytest
```

### Creating New Migration
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Code Quality
```bash
# Format code
black src/

# Lint code
ruff check src/
```

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the repository.
