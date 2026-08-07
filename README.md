# 🛡️ SentinelShield AI

> AI-Powered Financial Security Operations Center (Financial SOC)

SentinelShield AI is an AI-powered cybersecurity platform designed for banks and financial institutions. It continuously monitors financial transactions and user activities, detects suspicious behavior using AI, calculates dynamic risk scores, provides explainable AI insights, and assists security teams in responding to cyber threats in real time.

---

## 📌 Problem Statement

Financial institutions face increasing cybersecurity threats such as:

- Fraudulent transactions
- Account takeover attacks
- Phishing
- Brute-force login attempts
- Insider threats
- Suspicious user behavior

Traditional systems often detect these threats only after financial damage has occurred.

SentinelShield AI provides real-time monitoring, intelligent threat detection, and automated incident response.

---

# 🚀 Solution

SentinelShield AI acts as a Financial Security Operations Center (SOC).

Every login and transaction is analyzed by the AI Risk Engine to:

- Detect suspicious activities
- Calculate dynamic risk scores
- Explain AI decisions
- Recommend security actions
- Alert both customers and administrators

---

# 👥 User Roles

## 👤 Customer Portal

Bank customers can:

- View Security Dashboard
- View Recent Transactions
- Monitor Login History
- Manage Trusted Devices
- Receive Fraud Alerts
- View Security Score
- Report Suspicious Activity
- Manage Account Security

---

## 🛡️ Admin SOC Dashboard

Security analysts can:

- Monitor live transactions
- Detect fraud
- View AI explanations
- Manage incidents
- Freeze or unlock accounts
- Analyze risk trends
- Monitor global threats
- Simulate cyber attacks
- Generate security reports

---

# ✨ Features

## Authentication

- JWT Authentication
- Role-Based Access Control
- Secure Login
- Protected Routes

---

## AI Fraud Detection

Detects:

- High-value transactions
- Impossible travel
- VPN logins
- Unknown devices
- Failed login attempts
- Unusual login times

---

## AI Risk Engine

Calculates a dynamic risk score based on suspicious events.

Example:

| Event | Score |
|--------|------:|
| High Transaction | +30 |
| Unknown Device | +15 |
| Foreign Country | +20 |
| VPN | +10 |
| Failed Login | +15 |
| Unusual Login Time | +10 |

---

## Explainable AI

Instead of simply saying:

```
Fraud Detected
```

The system explains why.

Example:

```
Fraud Probability

97%

Reasons

✔ High Transaction Amount

✔ VPN

✔ Unknown Device

✔ Foreign Country
```

---

## Incident Response

Risk Level | Action
-----------|----------------------------
Low | Log Event
Medium | Notify Customer
High | Block Transaction
Critical | Freeze Account & Alert Admin

---

## Cyber Attack Simulator

Simulates realistic attacks.

Example:

- High Transaction
- VPN Login
- Unknown Device
- Foreign Country

AI automatically:

- Calculates Risk Score
- Generates Alert
- Blocks Transaction
- Updates Dashboard

---

# 🏗️ Project Architecture

```
Customer

↓

Login

↓

Spring Boot Backend

↓

AI Risk Engine

↓

Threat Detection

↓

Risk Score

↓

Incident Response

↓

PostgreSQL

↓

Admin SOC Dashboard
```

---

# 🛠️ Technology Stack

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Shadcn UI
- Framer Motion
- Axios
- React Router
- Recharts
- Lucide Icons

---

## Backend (Planned)

- Spring Boot
- Spring Security
- JWT
- PostgreSQL
- REST API

---

## AI Service (Planned)

- Python
- FastAPI
- Scikit-learn
- SHAP (Explainable AI)

---

## Database

- PostgreSQL

---

# 📂 Project Structure

```
src/

components/

layouts/

pages/

admin/

Dashboard

Users

Transactions

Threat Detection

Incidents

Risk Analytics

Threat Intelligence

Reports

Settings

user/

Dashboard

Transactions

Devices

Alerts

Login History

Profile

Settings

services/

hooks/

types/

utils/
```

---

# ▶️ Getting Started

## Clone Repository

```bash
git clone https://github.com/harini281/sentinelshield-ai.git
```

## Navigate

```bash
cd sentinelshield-ai
```

## Install Dependencies

```bash
npm install
```

## Start Development Server

```bash
npm run dev
```

The application will be available at:

```
http://localhost:5173
```

---

# 🔐 Demo Accounts

## Admin

Email

```
admin@sentinel.ai
```

Password

```
sentinel
```

---

## Customer

Email

```
user@sentinel.ai
```

Password

```
sentinel
```

---

# 🎯 Future Improvements

- Real AI Fraud Detection Model
- Isolation Forest
- Random Forest
- SHAP Explainability
- Real-time WebSocket Alerts
- Email Notifications
- SMS Alerts
- Mobile Application
- Docker Deployment
- Cloud Deployment

---

# 👨‍💻 Team

**Project Name**

SentinelShield AI

AI-Powered Financial Security Operations Center

Developed for an AI in Finance Hackathon.

We haven't deployed our prototype yet. This Git repository contains all the project files. You can clone the repository, run the project locally, and it should work as expected.



---

# 📄 License

This project is developed for educational and hackathon purposes.
