"""init

Revision ID: 864c0b53fb31
Revises:
Create Date: 2026-01-03 10:10:35.125056

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "864c0b53fb31"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.String(length=255),
            primary_key=True,
        ),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password_hash", sa.Text(), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("company", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=20)),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.CheckConstraint("role IN ('EMPLOYEE', 'ADMIN')", name="ck_users_role"),
    )

    op.create_table(
        "employees",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("user_id", sa.String(), nullable=False, unique=True),
        sa.Column("job_title", sa.String(length=100)),
        sa.Column("department", sa.String(length=100)),
        sa.Column("address", sa.Text()),
        sa.Column("date_of_joining", sa.Date(), nullable=False),
        sa.Column("profile_picture_url", sa.Text()),
        sa.Column("check_in_time", sa.Time()),
        sa.Column("check_out_time", sa.Time()),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "attendance_records",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("employee_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("work_date", sa.Date(), nullable=False),
        sa.Column("check_in", sa.TIMESTAMP(timezone=True)),
        sa.Column("check_out", sa.TIMESTAMP(timezone=True)),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"], ondelete="CASCADE"),
        sa.CheckConstraint(
            "status IN ('PRESENT', 'ABSENT', 'HALF_DAY', 'LEAVE')",
            name="ck_attendance_records_status",
        ),
        sa.UniqueConstraint(
            "employee_id", "work_date", name="uq_attendance_employee_date"
        ),
    )

    op.create_table(
        "leave_types",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=50), nullable=False, unique=True),
        sa.Column("is_paid", sa.Boolean(), nullable=False),
    )

    op.create_table(
        "leave_requests",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("employee_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("leave_type_id", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("remarks", sa.Text()),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("reviewed_by", sa.String()),
        sa.Column("review_comment", sa.Text()),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("reviewed_at", sa.TIMESTAMP(timezone=True)),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["leave_type_id"], ["leave_types.id"]),
        sa.ForeignKeyConstraint(["reviewed_by"], ["users.id"]),
        sa.CheckConstraint(
            "status IN ('PENDING', 'APPROVED', 'REJECTED')",
            name="ck_leave_requests_status",
        ),
    )

    op.create_table(
        "salary_structures",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("employee_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("base_salary", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column(
            "allowances",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "deductions",
            sa.Numeric(precision=12, scale=2),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column("effective_from", sa.Date(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"], ondelete="CASCADE"),
        sa.UniqueConstraint(
            "employee_id",
            "effective_from",
            name="uq_salary_structures_employee_effective_from",
        ),
    )

    op.create_table(
        "salary_slips",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("employee_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("month", sa.Date(), nullable=False),
        sa.Column("gross_salary", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("net_salary", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column(
            "generated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.ForeignKeyConstraint(["employee_id"], ["employees.id"]),
        sa.UniqueConstraint(
            "employee_id", "month", name="uq_salary_slips_employee_month"
        ),
    )

    op.create_index(
        "idx_attendance_employee_date",
        "attendance_records",
        ["employee_id", "work_date"],
    )
    op.create_index(
        "idx_leave_employee_status", "leave_requests", ["employee_id", "status"]
    )
    op.create_index("idx_salary_employee", "salary_slips", ["employee_id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("idx_salary_employee", table_name="salary_slips")
    op.drop_index("idx_leave_employee_status", table_name="leave_requests")
    op.drop_index("idx_attendance_employee_date", table_name="attendance_records")
    op.drop_table("salary_slips")
    op.drop_table("salary_structures")
    op.drop_table("leave_requests")
    op.drop_table("attendance_records")
    op.drop_table("leave_types")
    op.drop_table("employees")
    op.drop_table("users")
