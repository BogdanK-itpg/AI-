# AI Incident Management System

AI-powered CLI chatbot system for managing IT incidents with automatic priority classification using keyword-based rules. Supports Bulgarian and English language input.

## Features

- **AI Priority Classification** - Automatically classifies incidents as High, Medium, or Low based on description keywords
- **CLI Chatbot Interface** - Natural language commands in Bulgarian
- **Event System** - Notifies on incident creation, priority changes, and critical incidents
- **SQLite Persistence** - All data stored locally
- **Technician Management** - Assign and track technicians
- **Statistics & History** - View statistics and action history

## Project Structure

```
src/
├── main.py                 # Entry point
├── db.py                   # SQLite database wrapper
├── schema.sql              # Database schema
├── intents.json            # NLU intent patterns
├── chatbot/
│   ├── chatbot.py          # Chatbot facade
│   ├── nlu.py              # Natural language understanding
│   └── router.py           # Intent routing
├── models/
│   ├── incident.py         # Incident model
│   └── technician.py       # Technician model
├── services/
│   ├── incident_service.py # Incident CRUD
│   ├── technician_service.py
│   ├── statistics_service.py
│   ├── database_service.py # Database operations
│   └── incident_manager.py # Business logic
├── core/
│   └── event_manager.py    # Event system
└── ai/
    └── classifier.py       # AI priority classifier
```

## Usage

```bash
cd src
python main.py
```

## Commands

- `създай инцидент [title] описание [description] категория [category]` - Create incident
- `покажи инциденти` - List all incidents
- `покажи инциденти с приоритет висок/среден/нисък` - Filter by priority
- `затвори инцидент [id]` - Close incident
- `покажи техници` - List technicians
- `назначи техник [id] за инцидент [id]` - Assign technician
- `покажи статистика` - View statistics
- `покажи история` - View action history
- `помощ` - Show commands
- `изход` - Exit