"""DatabaseService - SQLite-based Persistence Layer.

This module provides SQLite storage for incidents and technicians.
"""

from typing import List, Optional, Dict, Any, Callable
from models.incident import Incident
from models.technician import Technician
import db


class DatabaseService:
    """Database service for storing incidents and technicians using SQLite.

    Methods:
        insert_incident: Add new incident
        update_incident: Modify existing incident
        delete_incident: Remove incident
        select_incident: Query single incident
        select_all_incidents: Query all incidents
        select_incidents_by_filter: Query with filter
        insert_technician: Add new technician
        select_technician: Query single technician
        select_all_technicians: Query all technicians
    """

    def __init__(self):
        """Initialize the database service."""
        db.initialize_database()

    def insert_incident(self, incident: Incident) -> int:
        """Insert a new incident into the database."""
        result = db.execute(
            """INSERT INTO incidents (title, description, category, status, priority, assigned_technician)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (incident.title, incident.description, incident.category,
             incident.status, incident.priority, incident.assigned_technician)
        )
        return result if result else -1

    def update_incident(self, incident_id: int, updates: Dict[str, Any]) -> bool:
        """Update an existing incident."""
        if not updates:
            return False

        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [incident_id]

        result = db.execute(
            f"UPDATE incidents SET {set_clause} WHERE id = ?",
            tuple(values)
        )
        return result is not None

    def delete_incident(self, incident_id: int) -> bool:
        """Delete an incident from the database."""
        result = db.execute("DELETE FROM incidents WHERE id = ?", (incident_id,))
        return result is not None

    def select_incident(self, incident_id: int) -> Optional[Incident]:
        """Select a single incident by ID."""
        row = db.fetch_one("SELECT * FROM incidents WHERE id = ?", (incident_id,))
        if row:
            return self._row_to_incident(row)
        return None

    def select_all_incidents(self) -> List[Incident]:
        """Select all incidents from the database."""
        rows = db.fetch_all("SELECT * FROM incidents ORDER BY created_at DESC")
        return [self._row_to_incident(row) for row in rows]

    def select_incidents_by_filter(self, filter_func: Callable[[Incident], bool]) -> List[Incident]:
        """Select incidents matching a filter function."""
        all_incidents = self.select_all_incidents()
        return [inc for inc in all_incidents if filter_func(inc)]

    def insert_technician(self, technician: Technician) -> int:
        """Insert a new technician into the database."""
        result = db.execute(
            "INSERT INTO technicians (name, department) VALUES (?, ?)",
            (technician.name, technician.department)
        )
        return result if result else -1

    def select_technician(self, technician_id: int) -> Optional[Technician]:
        """Select a single technician by ID."""
        row = db.fetch_one("SELECT * FROM technicians WHERE id = ?", (technician_id,))
        if row:
            return self._row_to_technician(row)
        return None

    def select_all_technicians(self) -> List[Technician]:
        """Select all technicians from the database."""
        rows = db.fetch_all("SELECT * FROM technicians")
        return [self._row_to_technician(row) for row in rows]

    def update_technician(self, technician_id: int, updates: Dict[str, Any]) -> bool:
        """Update an existing technician."""
        if not updates:
            return False

        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [technician_id]

        result = db.execute(
            f"UPDATE technicians SET {set_clause} WHERE id = ?",
            tuple(values)
        )
        return result is not None

    def count_incidents(self) -> int:
        """Get total number of incidents."""
        row = db.fetch_one("SELECT COUNT(*) as cnt FROM incidents")
        return row['cnt'] if row else 0

    def count_technicians(self) -> int:
        """Get total number of technicians."""
        row = db.fetch_one("SELECT COUNT(*) as cnt FROM technicians")
        return row['cnt'] if row else 0

    def _row_to_incident(self, row) -> Incident:
        """Convert database row to Incident object."""
        return Incident(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            category=row['category'],
            created_at=row['created_at'],
            status=row['status'],
            priority=row['priority'],
            assigned_technician=row['assigned_technician']
        )

    def _row_to_technician(self, row) -> Technician:
        """Convert database row to Technician object."""
        return Technician(
            id=row['id'],
            name=row['name'],
            department=row['department'],
            active_tasks=[]
        )

    def add_history(self, incident_id: int, action: str, details: str = ""):
        """Add a history record."""
        db.execute(
            "INSERT INTO history (incident_id, action, details) VALUES (?, ?, ?)",
            (incident_id, action, details)
        )

    def get_history(self, incident_id: int = None) -> List[Dict]:
        """Get history records."""
        if incident_id:
            rows = db.fetch_all(
                "SELECT * FROM history WHERE incident_id = ? ORDER BY timestamp DESC",
                (incident_id,)
            )
        else:
            rows = db.fetch_all(
                "SELECT * FROM history ORDER BY timestamp DESC LIMIT 50"
            )
        return [{'incident_id': r['incident_id'], 'action': r['action'],
                 'details': r['details'], 'timestamp': r['timestamp']} for r in rows]