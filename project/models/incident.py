"""Incident model for AI Incident Management System."""

from datetime import datetime
from typing import Optional


class Incident:
    """Represents an incident in the system.

    Attributes:
        id: Unique identifier for the incident
        title: Short title of the incident
        description: Detailed description of the incident
        category: Category of the incident (e.g., 'Hardware', 'Software', 'Network')
        created_at: Timestamp when the incident was created
        status: Current status of the incident ('Open', 'In Progress', 'Closed')
        priority: Priority level ('Low', 'Medium', 'High')
        assigned_technician: ID of the technician assigned to this incident
    """

    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        category: str,
        created_at: Optional[datetime] = None,
        status: str = "Open",
        priority: str = "Low",
        assigned_technician: Optional[int] = None
    ):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.created_at = created_at or datetime.now()
        self.status = status
        self.priority = priority
        self.assigned_technician = assigned_technician

    def update_status(self, new_status: str) -> None:
        """Update the status of the incident.

        Args:
            new_status: New status to set ('Open', 'In Progress', 'Closed')
        """
        valid_statuses = ["Open", "In Progress", "Closed"]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        self.status = new_status

    def assign_technician(self, technician_id: int) -> None:
        """Assign a technician to this incident.

        Args:
            technician_id: ID of the technician to assign
        """
        self.assigned_technician = technician_id
        if self.status == "Open":
            self.status = "In Progress"

    def close_incident(self) -> None:
        """Close the incident and set status to Closed."""
        self.status = "Closed"

    def to_dict(self) -> dict:
        """Convert incident to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "status": self.status,
            "priority": self.priority,
            "assigned_technician": self.assigned_technician
        }

    def __repr__(self) -> str:
        return f"Incident(id={self.id}, title='{self.title}', status='{self.status}', priority='{self.priority}')"