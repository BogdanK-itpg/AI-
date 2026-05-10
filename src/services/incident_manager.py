"""IncidentManager - Service Layer for Incident Management.

This module provides the business logic layer for managing incidents,
including creation, deletion, retrieval, and filtering operations.
"""

from typing import List, Optional
from models.incident import Incident
from core.event_manager import EventManager
from ai.classifier import IncidentClassifier


class IncidentManager:
    """Service for managing incidents in the system.

    Responsibilities:
    - Create new incidents
    - Delete existing incidents
    - Retrieve all incidents
    - Filter incidents by priority
    - Trigger appropriate events during operations

    Events triggered:
    - on_incident_created: When a new incident is created
    - on_priority_changed: When priority changes after classification
    - on_critical_detected: When priority is classified as 'High'
    """

    def __init__(self, db_service, classifier: IncidentClassifier, event_manager: EventManager):
        """Initialize the IncidentManager.

        Args:
            db_service: Database service for persistence
            classifier: AI classifier for priority prediction
            event_manager: Event manager for triggering events
        """
        self._db = db_service
        self._classifier = classifier
        self._events = event_manager

    def create_incident(self, incident: Incident) -> int:
        """Create a new incident in the system.

        Triggers:
        - on_incident_created event after insertion
        - on_priority_changed if AI changes initial priority
        - on_critical_detected if priority is 'High'

        Args:
            incident: Incident object to create

        Returns:
            ID of the created incident
        """
        old_priority = incident.priority
        new_priority = self._classifier.predict_priority(incident)
        incident.priority = new_priority

        incident_id = self._db.insert_incident(incident)

        self._events.trigger("on_incident_created", incident.to_dict())

        if old_priority != new_priority:
            self._events.trigger("on_priority_changed", {
                "id": incident.id,
                "old_priority": old_priority,
                "new_priority": new_priority
            })

        if new_priority == "High":
            self._events.trigger("on_critical_detected", {
                "id": incident.id,
                "title": incident.title,
                "priority": new_priority
            })

        return incident_id

    def delete_incident(self, incident_id: int) -> bool:
        """Delete an incident from the system.

        Args:
            incident_id: ID of the incident to delete

        Returns:
            True if deletion successful, False otherwise
        """
        return self._db.delete_incident(incident_id)

    def get_all(self) -> List[Incident]:
        """Get all incidents from the system.

        Returns:
            List of all incident objects
        """
        return self._db.select_all_incidents()

    def get_by_id(self, incident_id: int) -> Optional[Incident]:
        """Get a specific incident by ID.

        Args:
            incident_id: ID of the incident to retrieve

        Returns:
            Incident object or None if not found
        """
        return self._db.select_incident(incident_id)

    def filter_by_priority(self, priority: str) -> List[Incident]:
        """Filter incidents by priority level.

        Args:
            priority: Priority level to filter by ('Low', 'Medium', 'High')

        Returns:
            List of incidents matching the priority
        """
        return self._db.select_incidents_by_filter(
            lambda inc: inc.priority == priority
        )

    def filter_by_status(self, status: str) -> List[Incident]:
        """Filter incidents by status.

        Args:
            status: Status to filter by ('Open', 'In Progress', 'Closed')

        Returns:
            List of incidents matching the status
        """
        return self._db.select_incidents_by_filter(
            lambda inc: inc.status == status
        )

    def filter_by_category(self, category: str) -> List[Incident]:
        """Filter incidents by category.

        Args:
            category: Category to filter by

        Returns:
            List of incidents matching the category
        """
        return self._db.select_incidents_by_filter(
            lambda inc: inc.category == category
        )

    def get_statistics(self) -> dict:
        """Get statistics about incidents in the system.

        Returns:
            Dictionary with counts by priority and status
        """
        all_incidents = self.get_all()
        stats = {
            "total": len(all_incidents),
            "by_priority": {"Low": 0, "Medium": 0, "High": 0},
            "by_status": {"Open": 0, "In Progress": 0, "Closed": 0}
        }

        for inc in all_incidents:
            if inc.priority in stats["by_priority"]:
                stats["by_priority"][inc.priority] += 1
            if inc.status in stats["by_status"]:
                stats["by_status"][inc.status] += 1

        return stats