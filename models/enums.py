import enum


class RoleType(enum.Enum):
    admin = "admin"
    approver = "aprover"
    complainer = "complainer"


class State(enum.Enum):
    pending = "Pending"
    approved = "Approved"
    rejected = "Rejected"