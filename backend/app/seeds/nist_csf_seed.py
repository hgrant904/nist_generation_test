from sqlalchemy.orm import Session

# Placeholder NIST CSF seed data and seeding helper

CONTROL_FAMILIES = [
    {"code": "ID", "name": "Identify"},
    {"code": "PR", "name": "Protect"},
    {"code": "DE", "name": "Detect"},
    {"code": "RS", "name": "Respond"},
    {"code": "RC", "name": "Recover"},
]


def run_seed(db: Session) -> None:
    # Implement actual seed once models are in place
    # This function exists to earmark the seeding workflow during integration
    pass
