"""Incident Service - CRUD operations for incidents."""

from models.incident import Incident
from core.event_manager import EventManager
from ai.classifier import IncidentClassifier
from services.database_service import DatabaseService

_global_db = None
_global_classifier = None
_global_event_manager = None


def _get_service():
    global _global_db, _global_classifier, _global_event_manager
    if _global_db is None:
        _global_db = DatabaseService()
        _global_classifier = IncidentClassifier()
        _global_event_manager = EventManager()
    return _global_db, _global_classifier, _global_event_manager


def _trigger_event(event_name: str, data: dict):
    _, _, events = _get_service()
    events.trigger(event_name, data)


def create_incident(title: str, description: str, category: str = "Друго") -> str:
    """Create a new incident with AI priority prediction."""
    db, classifier, events = _get_service()

    incident = Incident(
        id=None,
        title=title,
        description=description,
        category=category,
        status="Open",
        priority="Low"
    )

    old_priority = incident.priority
    new_priority = classifier.predict_priority(incident)
    incident.priority = new_priority

    incident_id = db.insert_incident(incident)

    _trigger_event("on_incident_created", incident.to_dict())

    if old_priority != new_priority:
        _trigger_event("on_priority_changed", {
            "id": incident.id,
            "old_priority": old_priority,
            "new_priority": new_priority
        })

    if new_priority == "High":
        _trigger_event("on_critical_detected", {
            "id": incident.id,
            "title": incident.title,
            "priority": new_priority
        })

    return f"Инцидент '{title}' беше създаден с ID: {incident_id}, приоритет: {new_priority}"


def list_incidents() -> str:
    """List all incidents."""
    db, _, _ = _get_service()
    incidents = db.select_all_incidents()

    if not incidents:
        return "Няма регистрирани инциденти."

    headers = ["ID", "Заглавие", "Категория", "Приоритет", "Статус"]
    col_widths = [4, 20, 15, 10, 12]

    lines = []
    lines.append("".join(h.ljust(w) for h, w in zip(headers, col_widths)))
    lines.append("-" * sum(col_widths))

    for inc in incidents:
        lines.append(
            f"{str(inc.id):<{col_widths[0]}}"
            f"{inc.title[:18]:<{col_widths[1]}}"
            f"{inc.category[:13]:<{col_widths[2]}}"
            f"{inc.priority:<{col_widths[3]}}"
            f"{inc.status:<{col_widths[4]}}"
        )

    return "\n".join(lines)


def list_incidents_by_priority(priority: str) -> str:
    """List incidents filtered by priority."""
    db, _, _ = _get_service()
    incidents = db.select_incidents_by_filter(lambda i: i.priority == priority)

    if not incidents:
        return f"Няма инциденти с приоритет {priority}."

    priority_bulgarian = {"High": "Висок", "Medium": "Среден", "Low": "Нисък"}

    headers = ["ID", "Зазвание", "Категория", "Статус"]
    col_widths = [4, 25, 15, 12]

    lines = [f"Инциденти с приоритет {priority_bulgarian.get(priority, priority)}:"]
    lines.append("".join(h.ljust(w) for h, w in zip(headers, col_widths)))
    lines.append("-" * sum(col_widths))

    for inc in incidents:
        lines.append(
            f"{str(inc.id):<{col_widths[0]}}"
            f"{inc.title[:23]:<{col_widths[1]}}"
            f"{inc.category[:13]:<{col_widths[2]}}"
            f"{inc.status:<{col_widths[3]}}"
        )

    return "\n".join(lines)


def delete_incident(incident_id: str) -> str:
    """Delete an incident by ID."""
    db, _, _ = _get_service()
    try:
        inc_id = int(incident_id)
    except ValueError:
        return "Невалидно ID."

    if db.delete_incident(inc_id):
        return f"Инцидент с ID {inc_id} беше изтрит."
    return f"Инцидент с ID {inc_id} не съществува."


def update_incident_status(incident_id: str, status: str) -> str:
    """Update incident status."""
    db, _, _ = _get_service()
    try:
        inc_id = int(incident_id)
    except ValueError:
        return "Невалидно ID."

    status_map = {
        "отворен": "Open",
        "затворен": "Closed",
        "в работа": "In Progress",
        "open": "Open",
        "closed": "Closed",
        "in progress": "In Progress"
    }

    db_status = status_map.get(status.lower(), status)

    valid_statuses = ["Open", "In Progress", "Closed"]
    if db_status not in valid_statuses:
        return f"Невалиден статус. Използвайте: {', '.join(valid_statuses)}"

    incident = db.select_incident(inc_id)
    if not incident:
        return f"Инцидент с ID {inc_id} не съществува."

    incident.update_status(db_status)
    return f"Статусът на инцидент {inc_id} беше обновен на {db_status}."


def close_incident(incident_id: str) -> str:
    """Close an incident."""
    db, _, events = _get_service()
    try:
        inc_id = int(incident_id)
    except ValueError:
        return "Невалидно ID."

    incident = db.select_incident(inc_id)
    if not incident:
        return f"Инцидент с ID {inc_id} не съществува."

    incident.close_incident()

    events.trigger("on_incident_closed", {
        "id": incident.id,
        "title": incident.title,
        "status": incident.status
    })

    return f"Инцидент {inc_id} беше затворен."


def show_incident(incident_id: str) -> str:
    """Show detailed incident info."""
    db, _, _ = _get_service()
    try:
        inc_id = int(incident_id)
    except ValueError:
        return "Невалидно ID."

    incident = db.select_incident(inc_id)
    if not incident:
        return f"Инцидент с ID {inc_id} не съществува."

    priority_bg = {"High": "Висок", "Medium": "Среден", "Low": "Нисък"}
    status_bg = {"Open": "Отворен", "In Progress": "В работа", "Closed": "Затворен"}

    return (
        f"Детайли за инцидент {incident.id}:\n"
        f"  Зазвание: {incident.title}\n"
        f"  Описание: {incident.description}\n"
        f"  Категория: {incident.category}\n"
        f"  Приоритет: {priority_bg.get(incident.priority, incident.priority)} ({incident.priority})\n"
        f"  Статус: {status_bg.get(incident.status, incident.status)} ({incident.status})\n"
        f"  Създаден: {incident.created_at}\n"
        f"  Техник: {incident.assigned_technician or 'Не е назначен'}"
    )


def get_incident_by_id(incident_id: int):
    """Get incident by ID (internal use)."""
    db, _, _ = _get_service()
    return db.select_incident(incident_id)