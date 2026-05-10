## Име на проекта
**AI система за управление на инциденти**

---

## 1. Идея на проекта
Системата има за цел да подпомага фирми и IT екипи при обработка на инциденти (проблеми, аварии, заявки), като използва изкуствен интелект за автоматично определяне на приоритет.

Вместо служител ръчно да преценява спешността, системата анализира данните за инцидента и го класифицира като:
- Low Priority
- Medium Priority
- High Priority

Това позволява:
- по-бърза реакция
- автоматизация
- по-добро разпределяне на задачи
- по-малко човешки грешки

---

## 2. Основни класове

### Incident
Представя един инцидент.

**Полета:**
- id  
- title  
- description  
- category  
- created_at  
- status  
- priority  
- assigned_technician  

**Методи:**
- update_status()  
- assign_technician()  
- close_incident()  

---

### Technician
Представя служител, който решава инциденти.

**Полета:**
- id  
- name  
- department  
- active_tasks  

**Методи:**
- take_incident()  
- finish_task()  

---

### IncidentClassifier
AI клас за определяне на приоритет.

**Методи:**
- train_model()  
- predict_priority()  
- evaluate_model()  

---

### IncidentManager
Управлява всички инциденти.

**Методи:**
- create_incident()  
- delete_incident()  
- get_all()  
- filter_by_priority()  

---

### EventManager
Система за събития.

**Методи:**
- subscribe()  
- trigger()  

---

### DatabaseService
Работи с базата данни.

**Методи:**
- connect()  
- insert()  
- update()  
- delete()  
- select()  

---

## 3. Структура на проекта

```

incident_ai_project/
│
├── main.py
├── models/
│   ├── incident.py
│   ├── technician.py
│
├── services/
│   ├── database_service.py
│   ├── incident_manager.py
│   ├── event_manager.py
│
├── ai/
│   └── classifier.py
│
├── data/
│   └── incidents.csv
│
└── database/
└── incidents.db

```

---

## 4. База данни

Ще се използва **SQLite**.

### Таблица: incidents

| поле          | тип     |
|--------------|--------|
| id           | INTEGER |
| title        | TEXT    |
| description  | TEXT    |
| category     | TEXT    |
| priority     | TEXT    |
| status       | TEXT    |
| created_at   | TEXT    |
| technician_id| INTEGER |

---

### Таблица: technicians

| поле       | тип     |
|-----------|--------|
| id        | INTEGER |
| name      | TEXT    |
| department| TEXT    |

---

### Таблица: history

| поле        | тип     |
|------------|--------|
| id         | INTEGER |
| incident_id| INTEGER |
| action     | TEXT    |
| timestamp  | TEXT    |

---

## 5. AI подход

Ще се използва класификация чрез Machine Learning.

**Входни данни:**
- категория на проблема  
- ключови думи в описанието  
- време на създаване  
- брой засегнати потребители  
- дали системата е спряла  

**Изход:**
- Low  
- Medium  
- High  

**Подходящи модели:**
- Decision Tree  
- Random Forest  
- Logistic Regression  

---

## 6. Примерни данни

| title                | category  | users_affected | system_down | priority |
|---------------------|----------|----------------|------------|----------|
| Printer not working | Hardware | 1              | No         | Low      |
| Server offline      | Network  | 50             | Yes        | High     |
| Slow internet       | Network  | 10             | No         | Medium   |
| Email issue         | Software | 3              | No         | Low      |
| Database crashed    | Database | 100            | Yes        | High     |

---

## 7. Събития в системата

- on_incident_created  
- on_priority_changed  
- on_critical_detected  

---

## 8. LINQ / заявки / анализ

- списък с High Priority инциденти  
- брой инциденти по категория  
- средно време за решаване  
- най-натоварен техник  
- отворени инциденти  

