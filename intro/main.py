from http.client import HTTPException
import json

from fastapi import FastAPI, Path, Query


app = FastAPI()

def load_data():
    with open("student.json", "r") as f:
        data = json.load(f)
    return data

@app.get("/")
def hello():
    return "This is a student server."

@app.get("/about")
def about():
    return "Fully functional student server with FastAPI."

@app.get("/view")
def viewStudents():
    data = load_data()
    return data

@app.get("/view/{student_id}")
def viewStudentById(student_id: str = Path(..., description="Student id", example="s001")):
    data = load_data()
    
    if student_id in data:
        return data[student_id]
    else:
        raise HTTPException(status_code=404, detail="Student not found")



@app.get("/sort")
def viewStudentById(sorted_by: str = Query(..., description="Sort by age, roll, english_marks, math_marks, science_marks"), order: str = Query('asc', description="Choose asc or desc order")):
    valid_fields = ["age", "roll", "english_marks", "math_marks", "science_marks"]
    if sorted_by not in valid_fields:
        raise HTTPException(status_code=404, detail=f"Invalid sort field. Select from {valid_fields}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=404, detail="Invalid order. Choose 'asc' or 'desc'.")
    
    sort_order = True if order == 'desc' else False

    data = load_data()
    sorted_data = list(data.values())
    sorted_data.sort(key=lambda x: x[sorted_by], reverse=sort_order)
    return sorted_data