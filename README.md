# ☀️ CRMSolar: Solar Energy Sales Management System

Welcome to the **CRMSolar** repository — a **Customer Relationship Management (CRM)** system built with **Django**, designed to optimize the **sales and installation process of solar energy projects**.

The project follows a modular architecture to ensure **separation of concerns**, **scalability**, and **maintainability**.

---

## 🛠️ Technologies Used

- **Framework:** Django 
- **Language:** Python  
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **Auditing/Logging:** `django-simple-history` (Used exclusively for change logs and auditing)

---

## 🚀 Setup and Installation Guide

Follow these steps to set up and run the project locally:

### 1️⃣ Clone the Repository

```bash
git clone [YOUR_REPOSITORY_URL]
cd crm-solar
```

### 2️⃣ Configure the Virtual Environment

Create and activate a virtual environment to isolate project dependencies.

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows
```

### 3️⃣ Install Dependencies

Install all required Python libraries using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4️⃣ Project Initialization (Django Setup)

Initialize the base Django project structure and prepare the database.

#### Create Project Files (if missing)

```bash
django-admin startproject crm_solar_root .
```

#### Generate Migration Files

```bash
python manage.py makemigrations clients core energy sales
```

#### Apply Migrations

```bash
python manage.py migrate
```

#### Create Superuser

```bash
python manage.py createsuperuser
```

---

### 5️⃣ Start the Server

```bash
python manage.py runserver
```

The system will be accessible at:  
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🧱 Architecture and Modules

The project is divided into independent Django applications, each with specific responsibilities:

| Application | Responsibility | Key Models |
|--------------|----------------|-------------|
| **core** | Central logic, authentication, dashboard, and abstract models (e.g., `TimeStampedUserModel`) | `login_view`, `sales_dashboard_view` |
| **clients** | Client information management (companies and contacts) | `Company`, `Address` |
| **energy** | Energy delivery point management | `CPE` (Energy Point Code) |
| **sales** | Sales funnel management | `Opportunity`, `OpportunityStatus` |

---

## 🔑 Main Routes

| Route | Description | Authentication |
|--------|--------------|----------------|
| `/` | Main Sales Dashboard (filtered by assigned user) | ✅ |
| `/login/` | User Authentication | ❌ |
| `/logout/` | End user session | ✅ |
| `/admin/` | Django Admin Panel | ✅ (Superuser) |

---

## 🤝 Contributions

Contributions are welcome!  
Follow the standard Git workflow:

1. Create a new branch  
   ```bash
   git checkout -b feature/new-feature-name
   ```
2. Make your changes  
3. Commit your modifications  
   ```bash
   git commit -am 'Feat: short description of the change'
   ```
4. Push your branch to the remote repository  
   ```bash
   git push origin feature/new-feature-name
   ```
5. Open a Pull Request

---

👨‍💻 **Developed by:** Nelson Almeida  
📅 **Version:** 1.0  
📦 **License:** MIT
