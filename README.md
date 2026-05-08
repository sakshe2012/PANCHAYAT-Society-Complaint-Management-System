# PANCHAYAT – Voice-Based Society Complaint Management System

## 📌 Project Overview
PANCHAYAT is a voice-enabled web application designed to help society members report local community problems easily. Users can submit complaints using voice input, which is converted into text, while administrators can manage and resolve issues through a centralized dashboard.

---

## 🎯 Features

### 👤 User Features
- User Registration & Login
- Submit Complaints
- Voice-to-Text Complaint Input
- Track Complaint Status
- View Submitted Complaints

### 🛠️ Admin Features
- Admin Login
- View All Complaints
- Update Complaint Status
- Manage Complaints Efficiently

---

## 🎤 Voice-Based System
The application uses speech recognition technology to convert user voice input into text automatically, making complaint registration faster and more accessible.

---

## 🏗️ Technologies Used

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### Database
- SQLite

---

## 🗄️ Database Tables

### Users Table
| Field | Description |
|------|-------------|
| id | User ID |
| username | Username |
| password | Password |
| role | User/Admin |

### Complaints Table
| Field | Description |
|------|-------------|
| id | Complaint ID |
| user_id | User Reference |
| title | Complaint Title |
| description | Complaint Description |
| location | Complaint Location |
| status | Complaint Status |

---

## 🔄 System Workflow

1. User logs into the system
2. User records complaint using voice input
3. Voice is converted into text
4. Complaint is submitted and stored in database
5. Admin views complaints
6. Admin updates complaint status
7. User tracks complaint progress

---

## 📷 Modules
- Authentication Module
- Complaint Management Module
- Voice Recognition Module
- Admin Dashboard

---

## 🚀 Future Enhancements
- AI-based complaint categorization
- Email/SMS notifications
- Image upload support
- Analytics dashboard
- GPS-based location tracking

---

## 💡 Project Goal
The main goal of PANCHAYAT is to provide a simple and accessible digital platform for solving society-level problems efficiently using voice-enabled technology.

---

## 👨‍💻 Developed Using
- Flask Framework
- SQLite Database
- Web Speech API

---

## 📜 License
This project is developed for educational and academic purposes.
