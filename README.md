# Academix API

This project provides a backend API to manage student-related data efficiently. The API interacts with a **MongoDB Cloud Cluster** for storage and is deployed on **Render**. The project is designed for ease of use, with **Swagger Documentation** included for seamless testing and exploration.

## Features
- Perform CRUD operations on student records.
- JSON-based data exchange.
- Hosted on a cloud platform for remote accessibility.
- Comprehensive Swagger Documentation.

---

## Technologies Used
- **Framework**: FastAPI
- **Database**: MongoDB 
- **Deployment Platform**: Render
- **API Documentation**: Swagger UI

---

## Deployment Details

The API is hosted on Render and can be accessed via the following links:

- **Swagger Documentation**: [Academix API Swagger Docs](https://academixapi.onrender.com/docs)

Swagger provides detailed insights into the available endpoints and allows testing the API directly.

---

## API Endpoints

### Base URL: `https://academixapi.onrender.com`

| Method | Endpoint        | Description                   |
|--------|-----------------|-------------------------------|
| GET    | `/students`     | Fetch all student records     |
| GET    | `/students/:id` | Fetch a student by ID         |
| POST   | `/students`     | Add a new student             |
| PUT    | `/students/:id` | Update student details by ID  |
| DELETE | `/students/:id` | Delete a student by ID        |

---
