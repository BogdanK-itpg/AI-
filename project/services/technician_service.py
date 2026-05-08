"""Technician Service - CRUD operations for technicians."""

from models.technician import Technician
from services.database_service import DatabaseService

_global_db = None


def _get_service():
    global _global_db
    if _global_db is None:
        _global_db = DatabaseService()
        t1 = Technician(1, "Иван Петров", "ИТ поддръжка")
        t2 = Technician(2, "Мария Иванова", "Мрежи")
        t3 = Technician(3, "Георги Димитров", "Сигурност")
        _global_db.insert_technician(t1)
        _global_db.insert_technician(t2)
        _global_db.insert_technician(t3)
    return _global_db


def add_technician(name: str, department: str) -> str:
    """Add a new technician."""
    db = _get_service()
    tech_id = db.count_technicians() + 1
    technician = Technician(tech_id, name, department)
    db.insert_technician(technician)
    return f"Техник '{name}' беше добавен с ID: {tech_id}, отдел: {department}"


def list_technicians() -> str:
    """List all technicians."""
    db = _get_service()
    techs = db.select_all_technicians()

    if not techs:
        return "Няма регистрирани техници."

    headers = ["ID", "Име", "Отдел", "Активни задачи"]
    col_widths = [4, 20, 20, 15]

    lines = []
    lines.append("".join(h.ljust(w) for h, w in zip(headers, col_widths)))
    lines.append("-" * sum(col_widths))

    for tech in techs:
        lines.append(
            f"{str(tech.id):<{col_widths[0]}}"
            f"{tech.name:<{col_widths[1]}}"
            f"{tech.department:<{col_widths[2]}}"
            f"{len(tech.active_tasks):<{col_widths[3]}}"
        )

    return "\n".join(lines)


def assign_technician(technician_id: str, incident_id: str) -> str:
    """Assign a technician to an incident."""
    db = _get_service()

    try:
        tech_id = int(technician_id)
        inc_id = int(incident_id)
    except ValueError:
        return "Невалидно ID."

    technician = db.select_technician(tech_id)
    if not technician:
        return f"Техник с ID {tech_id} не съществува."

    incident = db.select_incident(inc_id)
    if not incident:
        return f"Инцидент с ID {inc_id} не съществува."

    incident.assign_technician(tech_id)
    technician.take_incident(inc_id)

    return f"Техник {technician.name} (ID: {tech_id}) беше назначен за инцидент {inc_id}"


def get_technician_by_id(technician_id: int):
    """Get technician by ID (internal use)."""
    db = _get_service()
    return db.select_technician(technician_id)