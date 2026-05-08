"""Technician model for AI Incident Management System."""

from typing import List, Optional


class Technician:
    """Represents a technician in the system.

    Attributes:
        id: Unique identifier for the technician
        name: Name of the technician
        department: Department the technician belongs to
        active_tasks: List of incident IDs currently assigned to this technician
    """

    def __init__(self, id: int, name: str, department: str, active_tasks: Optional[List[int]] = None):
        self.id = id
        self.name = name
        self.department = department
        self.active_tasks = active_tasks or []

    def take_incident(self, incident_id: int) -> None:
        """Assign an incident to this technician.

        Args:
            incident_id: ID of the incident to take
        """
        if incident_id not in self.active_tasks:
            self.active_tasks.append(incident_id)

    def finish_task(self, incident_id: int) -> None:
        """Mark an incident as completed and remove from active tasks.

        Args:
            incident_id: ID of the incident to complete
        """
        if incident_id in self.active_tasks:
            self.active_tasks.remove(incident_id)

    def get_task_count(self) -> int:
        """Get the number of active tasks assigned to this technician."""
        return len(self.active_tasks)

    def to_dict(self) -> dict:
        """Convert technician to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "active_tasks": self.active_tasks
        }

    def __repr__(self) -> str:
        return f"Technician(id={self.id}, name='{self.name}', department='{self.department}', active_tasks={len(self.active_tasks)})"