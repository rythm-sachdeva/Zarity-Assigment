Below is the updated API documentation, including variable types, installation instructions, and commands for testing:

---

# **API Documentation**

## **Model: Patient**

| **Field**       | **Type**            | **Description**                                                                            |
|------------------|---------------------|--------------------------------------------------------------------------------------------|
| `patient_id`     | `IntegerField`      | ID of the patient. Must be a positive integer.                                             |
| `test_name`      | `CharField`         | Name of the test. Choices: `GLUCOSE` (Blood Glucose), `HB` (Hemoglobin), `CHOL` (Cholesterol). |
| `value`          | `DecimalField`      | The value of the test result. Maximum 8 digits with 2 decimal places.                      |
| `unit`           | `CharField`         | Unit of the test result. Max length: 10 characters.                                        |
| `test_date`      | `DateTimeField`     | Auto-generated timestamp when the test record is created.                                  |
| `is_abnormal`    | `BooleanField`      | Indicates if the test result is abnormal (`true` or `false`).                              |


---

## **1. POST `/api/tests/` - Create a New Test Record**

### **Description**
Create a new test record for a patient.

### **Request**
- **Method**: POST  
- **URL**: `/api/tests/`

### **Headers**
```http
Content-Type: application/json
```

### **Request Body (JSON)**
```json
{
    "patient_id": 123,
    "test_name": "GLUCOSE",
    "value": 110.5,
    "unit": "mg/dL",
    "is_abnormal": false
}
```

### **Response**
#### **Success**
- **Status Code**: 201 Created  
- **Response Body**:
```json
{
    "id": 1,
    "patient_id": 123,
    "test_name": "GLUCOSE",
    "value": 110.5,
    "unit": "mg/dL",
    "is_abnormal": false,
    "test_date": "2024-12-18T10:00:00Z"
}
```
#### **Error**
- **Status Code**: 400 Bad Request  
- **Response Body** (example):
```json
{
     "patient_id": [
    "This field is required."
  ]
}
```

---

## **2. GET `/api/tests/?patient_id=123` - Get All Tests for a Patient**

### **Description**
Retrieve all test records for a specific patient.

### **Request**
- **Method**: GET  
- **URL**: `/api/tests/?patient_id=123`

### **Response**
#### **Success**
- **Status Code**: 200 OK  
- **Response Body**:
```json
[
    {
        "id": 1,
        "patient_id": 123,
        "test_name": "GLUCOSE",
        "value": 110.5,
        "unit": "mg/dL",
        "is_abnormal": false,
        "test_date": "2024-12-18T10:00:00Z"
    },
    {
        "id": 2,
        "patient_id": 123,
        "test_name": "HB",
        "value": 13.2,
        "unit": "g/dL",
        "is_abnormal": false,
        "test_date": "2024-12-18T11:00:00Z"
    }
]
```

#### **Error**
- **Status Code**: 400 Bad Request  
- **Response Body** (example):
```json
{
    "message": "No Patient Id was passed in the query parameters"
}
```
---

## **3. GET `/api/tests/stats/` - Get Basic Statistics for Each Test Type**

### **Description**
Retrieve basic statistics (min, max, avg) for each test type.

### **Response**
#### **Success**
- **Status Code**: 200 OK  
- **Response Body**:
```json
{
   "test_stats": {
    "GLUCOSE": {
      "min_value": 12.0,
      "max_value": 40.0,
      "avg_value": 23.3333333333333,
      "total_tests": 3,
      "abnormal_count": 0
    },
    "HB": {
      "min_value": 6.0,
      "max_value": 11.0,
      "avg_value": 9.06666666666667,
      "total_tests": 3,
      "abnormal_count": 1
    }
  }
}
```

---

## **Installation Instructions**

1. **Clone the Repository**
```bash
git clone https://github.com/rythm-sachdeva/Zarity-Assigment.git
cd Laboratory
```

2. **Set Up Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv/Scripts/activate     # For Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Up the Database**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Run the Development Server**
```bash
python manage.py runserver
```

6. **Access the API**
Visit `http://localhost:8000/api/tests/` in your browser or use tools like Postman.

---

## **Testing the Application**

**Run Unit Tests**
```bash
python manage.py test
```
---

### **Error Codes**
| **Status Code** | **Meaning**                    |
|------------------|--------------------------------|
| 201 Created      | Successfully created a record |
| 200 OK           | Successfully retrieved data   |
| 400 Bad Request  | Invalid request parameters    |
| 500 Internal Error | Server-side issue           |

--- 

### Notes:
- Update the `requirements.txt` file with all necessary packages (e.g., `Django`, `djangorestframework`).
- Ensure tests cover all possible edge cases for better reliability.