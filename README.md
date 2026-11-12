# Patient Record Management API

A RESTful Patient Record Management System API built using **Python, FastAPI, and Pydantic**. This project allows users to create, view, update, delete, and sort patient records.

## Features

- **Create Patient:** Add new patient records.
- **View All Patients:** Retrieve all registered patients.
- **View Individual Patient:** Search for a patient using their unique ID.
- **Update Patient:** Update existing patient information.
- **Delete Patient:** Remove patient records.
- **Sort Patients:** Sort patients by height, weight, or BMI in ascending or descending order.
- **BMI Calculation:** Automatically calculate BMI using height and weight.
- **Health Verdict:** Categorize patients as underweight, normal, overweight, or obese.
- **Data Validation:** Validate patient information using Pydantic.
- **Error Handling:** Handle errors using FastAPI's HTTPException.

## Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- JSON (File Handling)

## Project Structure

```text
patient-management-system/
│
├── main.py
├── patients.json
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/patient-management-system.git
```

### 2. Navigate to the project directory

```bash
cd patient-management-system
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
uvicorn main:app --reload
```

The application will run at:

http://127.0.0.1:8000

## API Documentation

FastAPI provides interactive API documentation.

Open the following URL after running the application:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/about` | API information |
| GET | `/view` | View all patients |
| GET | `/patient/{patient_id}` | View a specific patient |
| GET | `/sort` | Sort patient records |
| POST | `/create` | Create a patient |
| PUT | `/edit/{patient_id}` | Update patient details |
| DELETE | `/delete/{patient_id}` | Delete a patient |

### Sorting Examples

Sort patients by height:

```text
/sort?sort_by=height&order=asc
```

Sort patients by weight:

```text
/sort?sort_by=weight&order=desc
```

Sort patients by BMI:

```text
/sort?sort_by=bmi&order=asc
```

## BMI Calculation

BMI is calculated using the formula:

**BMI = Weight (kg) / Height (m)²**

The system automatically generates a BMI verdict:

- Underweight: BMI below 18.5
- Normal: BMI from 18.5 to below 25
- Overweight: BMI from 25 to below 30
- Obese: BMI of 30 or above

## Data Storage

Patient records are stored in a JSON file (`patients.json`). The application uses Python's JSON module to read and write patient information.

**Note:** This project uses JSON file storage for learning purposes and is not intended for production use with real patient data.

## Learning Outcomes

Through this project, I practised:

- Building REST APIs using FastAPI.
- Understanding HTTP methods and status codes.
- Working with Pydantic models and data validation.
- Implementing CRUD operations.
- Handling query parameters and path parameters.
- Using HTTPException for error handling.
- Working with JSON file handling.
- Implementing sorting using Python's lambda function.

## Future Improvements

- Integrate MySQL database.
- Implement user authentication.
- Add role-based access control.
- Improve API security and data management.

---

**Developed as a Python and FastAPI learning project.**2