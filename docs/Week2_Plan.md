Here is a **focused, execution-ready plan for Week 2** of project *“AI система за управление на инциденти”*. This assumes Week 1 covered basic setup (project structure, DB schema, core classes skeletons).

---

# 📅 **Week 2 Plan – Core Backend + Database Integration**

## 🎯 **Primary Goal**

Move from structure → **working backend system with persistent storage and basic logic**.

By the end of Week 2, you should have:

* Fully implemented **DatabaseService**
* Functional **IncidentManager**
* Working **CRUD operations**
* Initial **event system**
* Data flowing between **models ↔ DB ↔ services**

---

# 🔧 **1. Database Layer (Critical Foundation)**

## ✅ Tasks

### 1.1 Implement `DatabaseService`

File: `services/database_service.py`

**Objective:** Abstract all DB operations.

**Concrete steps:**

* Implement SQLite connection handling
* Add query execution wrapper
* Ensure safe commits and closing

**Methods to implement:**

```python
connect()
insert(query, params)
update(query, params)
delete(query, params)
select(query, params)
```

**Important design decisions:**

* Use **parameterized queries** (avoid SQL injection)
* Return results as **dict-like structures** (not raw tuples)

---

### 1.2 Database Initialization Script

If not done in Week 1:

* Auto-create tables if they don't exist:

  * `incidents`
  * `technicians`
  * `history`

Add:

```python
CREATE TABLE IF NOT EXISTS ...
```

---

### 1.3 Test DB Layer

Write a quick test script in `main.py`:

* Insert dummy incident
* Fetch it
* Update it
* Delete it

👉 If this fails, everything else will fail.

---

# 🧠 **2. Models Implementation**

## ✅ Tasks

### 2.1 Complete `Incident` class

File: `models/incident.py`

**Add real logic (not placeholders):**

Methods:

```python
update_status(new_status)
assign_technician(technician_id)
close_incident()
```

**Behavior rules:**

* `close_incident()` → sets:

  * status = "Closed"
* `assign_technician()`:

  * update both object + DB
* Track `created_at`

---

### 2.2 Complete `Technician` class

File: `models/technician.py`

Methods:

```python
take_incident(incident_id)
finish_task(incident_id)
```

**Logic:**

* Maintain `active_tasks`
* Prevent overload (optional enhancement)

---

# ⚙️ **3. IncidentManager (Core Business Logic)**

File: `services/incident_manager.py`

## ✅ Tasks

### 3.1 Implement CRUD operations

```python
create_incident()
delete_incident()
get_all()
filter_by_priority(priority)
```

---

### 3.2 `create_incident()` – IMPORTANT

This is your **main pipeline entry point**.

Steps:

1. Receive raw input
2. (TEMP) Assign default priority OR stub AI
3. Insert into DB
4. Trigger event → `on_incident_created`

---

### 3.3 Filtering & Query Logic

Implement:

* Get all incidents
* Filter:

  * by priority
  * by status

---

# ⚡ **4. Event System (Observer Pattern)**

File: `services/event_manager.py`

## ✅ Tasks

### 4.1 Implement EventManager

```python
subscribe(event_name, callback)
trigger(event_name, data)
```

---

### 4.2 Add Core Events

Implement triggering for:

* `on_incident_created`
* `on_priority_changed`

---

### 4.3 Example Use Case

When incident is created:

```python
event_manager.trigger("on_incident_created", incident)
```

Optional:

* Print log
* Save to history table

---

# 🗂️ **5. History Tracking (Optional but Strong Bonus)**

## ✅ Tasks

* On every important action:

  * Insert into `history` table

Examples:

* Incident created
* Status updated
* Technician assigned

---

# 🧪 **6. Integration Testing (VERY IMPORTANT)**

## ✅ Build a test flow in `main.py`

Simulate real usage:

### Scenario:

1. Create 3–5 incidents
2. Assign technician
3. Update status
4. Filter high priority
5. Close incident

---

### Expected Outcome:

* Data persists in SQLite
* No crashes
* Correct state transitions

---

# 🧱 **7. AI Preparation (Light – NOT full model yet)**

## ✅ Tasks

### 7.1 Prepare `classifier.py`

DO NOT fully train yet.

Instead:

* Create class structure
* Stub methods:

```python
train_model()
predict_priority(data)
evaluate_model()
```

---

### 7.2 Temporary Logic

Inside `predict_priority()`:

Use simple rule-based logic:

```python
if system_down == "Yes":
    return "High"
elif users > 10:
    return "Medium"
else:
    return "Low"
```

👉 This allows system integration BEFORE ML is ready.

---

# 📊 **8. Data Handling**

## ✅ Tasks

* Load `incidents.csv`
* Inspect structure
* Prepare for Week 3 ML training

---

# 🧭 **Deliverables by End of Week 2**

You should have:

✅ Working SQLite integration
✅ Fully functional CRUD system
✅ IncidentManager controlling logic
✅ Event system working
✅ Models with real behavior
✅ Test scenario proving system works
✅ Stub AI classifier integrated

---

# ⚠️ **Common Pitfalls to Avoid**

* ❌ Mixing DB logic inside models → keep it in `DatabaseService`
* ❌ Hardcoding values → use parameters
* ❌ Skipping testing → bugs will stack
* ❌ Overengineering AI too early
* ❌ Ignoring edge cases (e.g., closing already closed incident)

