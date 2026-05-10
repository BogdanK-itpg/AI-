"""Router module for Incident Management Chatbot.

Handles intent routing and delegates to appropriate services.
"""

from typing import Optional, Dict
from .nlu import _load_intents
import services.incident_service as incidents
import services.technician_service as technicians
import services.statistics_service as stats


CATEGORIES = {
    "Инциденти": ["create_incident", "list_incidents", "list_incidents_by_priority", "delete_incident", "update_incident_status", "close_incident", "show_incident"],
    "Техници": ["list_technicians", "add_technician", "assign_technician"],
    "Статистика": ["statistics", "avg_resolution_time", "history"],
}


def handle_intent(intent: str, params: Optional[Dict[str, str]]) -> str:
    """Route intent to appropriate service and return presentation string."""

    if intent == 'help':
        help_lines = ["Налични команди:"]
        intents = _load_intents()
        intent_tags = {i.get('tag') for i in intents if i.get('tag')}

        for category, tags in CATEGORIES.items():
            cmds = []
            for tag in tags:
                if tag in intent_tags:
                    for i in intents:
                        if i.get('tag') == tag:
                            examples = i.get('examples', [])
                            if examples:
                                cmds.append(f"- {examples[0]}")
                            break
            if cmds:
                help_lines.append(f"\n{category}:")
                help_lines.extend(cmds)

        help_lines.append("\n\nДруги:")
        help_lines.append("- изход (затвори чатбота)")
        help_lines.append("- помощ (покажи тази помощ)")

        return "\n".join(help_lines)

    if intent == 'exit':
        return 'exit'

    # --- Incidents ---
    if intent == 'create_incident':
        if not params or 'title' not in params or 'description' not in params:
            return "Недостатъчни параметри. Формат: създай инцидент [title] описание [description] категория [category]"
        return incidents.create_incident(
            params.get('title'),
            params.get('description'),
            params.get('category', 'Друго')
        )

    if intent == 'list_incidents':
        return incidents.list_incidents()

    if intent == 'list_incidents_by_priority':
        priority = params.get('priority', '').lower()
        if priority in ['висок', 'high', 'high priority']:
            priority = 'High'
        elif priority in ['среден', 'medium', 'medium priority']:
            priority = 'Medium'
        elif priority in ['нисък', 'low', 'low priority']:
            priority = 'Low'
        else:
            return "Невалиден приоритет. Използвайте: висок, среден или нисък"
        return incidents.list_incidents_by_priority(priority)

    if intent == 'delete_incident':
        if not params or 'id' not in params:
            return "Укажете ID на инцидента. Формат: изтрий инцидент [id]"
        return incidents.delete_incident(params['id'])

    if intent == 'update_incident_status':
        if not params or 'id' not in params or 'status' not in params:
            return "Недостатъчни параметри. Формат: смени статус на инцидент [id] на [status]"
        return incidents.update_incident_status(params['id'], params['status'])

    if intent == 'close_incident':
        if not params or 'id' not in params:
            return "Укажете ID на инцидента. Формат: затвори инцидент [id]"
        return incidents.close_incident(params['id'])

    if intent == 'show_incident':
        if not params or 'id' not in params:
            return "Укажете ID на инцидента. Формат: покажи инцидент [id]"
        return incidents.show_incident(params['id'])

    # --- Technicians ---
    if intent == 'list_technicians':
        return technicians.list_technicians()

    if intent == 'add_technician':
        if not params or 'name' not in params or 'department' not in params:
            return "Недостатъчни параметри. Формат: добави техник [name] отдел [department]"
        return technicians.add_technician(params['name'], params['department'])

    if intent == 'assign_technician':
        if not params or 'technician_id' not in params or 'incident_id' not in params:
            return "Недостатъчни параметри. Формат: назначи техник [technician_id] за инцидент [incident_id]"
        return technicians.assign_technician(params['technician_id'], params['incident_id'])

    # --- Statistics ---
    if intent == 'statistics':
        return stats.get_statistics()

    if intent == 'avg_resolution_time':
        return stats.get_avg_resolution_time()

    if intent == 'history':
        incident_id = params.get('id') if params else None
        return stats.get_history(incident_id)

    return "Не разбирам командата. Напишете 'помощ'."