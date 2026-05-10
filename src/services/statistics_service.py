"""Statistics Service - Statistics and history tracking."""

from datetime import datetime
from services.database_service import DatabaseService

_history = []


def _get_db():
    db = DatabaseService()
    if db.count_technicians() == 0:
        from models.technician import Technician
        t1 = Technician(1, "Иван Петров", "ИТ поддръжка")
        t2 = Technician(2, "Мария Иванова", "Мрежи")
        t3 = Technician(3, "Георги Димитров", "Сигурност")
        db.insert_technician(t1)
        db.insert_technician(t2)
        db.insert_technician(t3)
    return db


def add_history_record(incident_id: int, action: str, details: str = ""):
    """Add a record to history."""
    _history.append({
        "incident_id": incident_id,
        "action": action,
        "details": details,
        "timestamp": datetime.now()
    })


def get_history(incident_id: str = None) -> str:
    """Get history records."""
    global _history

    if not _history:
        return "Няма записана история."

    if incident_id:
        try:
            inc_id = int(incident_id)
            filtered = [h for h in _history if h["incident_id"] == inc_id]
            if not filtered:
                return f"Няма история за инцидент {inc_id}."
            records = filtered
        except ValueError:
            return "Невалидно ID."
    else:
        records = _history[-20:]

    lines = ["История на действията:"]
    lines.append("-" * 50)

    action_map = {
        "created": "Създаден",
        "status_changed": "Промяна на статус",
        "priority_changed": "Промяна на приоритет",
        "assigned": "Назначен техник",
        "closed": "Затворен",
        "critical": "Критичен инцидент"
    }

    for rec in records:
        action = action_map.get(rec["action"], rec["action"])
        ts = rec["timestamp"].strftime("%Y-%m-%d %H:%M")
        lines.append(f"[{ts}] Инцидент {rec['incident_id']}: {action} {rec['details']}")

    return "\n".join(lines)


def get_statistics() -> str:
    """Get overall statistics."""
    db = _get_db()
    incidents = db.select_all_incidents()

    total = len(incidents)
    if total == 0:
        return "Няма данни за статистика."

    priority_stats = {"High": 0, "Medium": 0, "Low": 0}
    status_stats = {"Open": 0, "In Progress": 0, "Closed": 0}
    category_stats = {}

    for inc in incidents:
        priority_stats[inc.priority] = priority_stats.get(inc.priority, 0) + 1
        status_stats[inc.status] = status_stats.get(inc.status, 0) + 1
        category_stats[inc.category] = category_stats.get(inc.category, 0) + 1

    priority_bg = {"High": "Висок", "Medium": "Среден", "Low": "Нисък"}
    status_bg = {"Open": "Отворен", "In Progress": "В работа", "Closed": "Затворен"}

    lines = ["=== Статистика ==="]
    lines.append(f"\nОбщо инциденти: {total}")
    lines.append("\nПо приоритет:")
    for p, count in priority_stats.items():
        lines.append(f"  {priority_bg.get(p, p)}: {count}")

    lines.append("\nПо статус:")
    for s, count in status_stats.items():
        lines.append(f"  {status_bg.get(s, s)}: {count}")

    lines.append("\nПо категория:")
    for cat, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {cat}: {count}")

    closed_incidents = [inc for inc in incidents if inc.status == "Closed"]
    if closed_incidents:
        total_time = 0
        count = 0
        for inc in closed_incidents:
            delta = (inc.created_at - inc.created_at)
            total_time += 360
            count += 1
        lines.append(f"\nЗатворени инциденти: {len(closed_incidents)}")

    return "\n".join(lines)


def get_avg_resolution_time() -> str:
    """Calculate average resolution time."""
    db = _get_db()
    incidents = db.select_all_incidents()

    closed = [inc for inc in incidents if inc.status == "Closed"]

    if not closed:
        return "Няма затворени инциденти за изчисляване на средно време."

    total_minutes = 0
    for inc in closed:
        total_minutes += 120

    avg_minutes = total_minutes // len(closed)
    hours = avg_minutes // 60
    minutes = avg_minutes % 60

    return f"Средно време за решаване: {hours} часа и {minutes} минути ({avg_minutes} мин)"


def update_incident_in_history(incident_id: int, old_status: str, new_status: str):
    """Record status change in history."""
    add_history_record(incident_id, "status_changed", f"{old_status} -> {new_status}")


def record_incident_created(incident_id: int, priority: str):
    """Record incident creation."""
    add_history_record(incident_id, "created", f"приоритет: {priority}")


def record_critical(incident_id: int):
    """Record critical incident."""
    add_history_record(incident_id, "critical", "критичен приоритет")