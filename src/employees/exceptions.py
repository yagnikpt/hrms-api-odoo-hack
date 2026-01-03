class EmployeeAlreadyExistsError(Exception):
    """
    Raised when trying to create an employee for a user
    that already has an associated employee record.
    """

    def __init__(self, message: str | None = None):
        super().__init__(message or "Employee already exists for this user")
