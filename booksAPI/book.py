
import json

from fastapi import FastAPI, Path, Query, Body, HTTPException


app = FastAPI()

def load_data():
    with open("books.json", "r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("books.json", "w") as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return "This is a reliable and functional book server."


@app.get("/books")
def viewBooksList():
    data = load_data()
    return data

@app.get("/books/{book_id}")
def viewBooksById(book_id: str = Path(..., description="Book id", example=1)):
    data = load_data()
    
    if book_id in data:
        return data[book_id]
    else:
        raise HTTPException(status_code=404, detail="Book not found")



@app.get("/books/sort")
def viewBooksById(sorted_by: str = Query(..., description="Sort by pages, rating"), order: str = Query('asc', description="Choose asc or desc order")):
    valid_fields = ["pages", "rating"]
    if sorted_by not in valid_fields:
        raise HTTPException(status_code=404, detail=f"Invalid sort field. Select from {valid_fields}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=404, detail="Invalid order. Choose 'asc' or 'desc'.")
    
    sort_order = True if order == 'desc' else False

    data = load_data()
    sorted_data = list(data.values())
    sorted_data.sort(key=lambda x: x[sorted_by], reverse=sort_order)
    return sorted_data



@app.post("/create_books")
def createBook(book: dict = Body()):
    data = load_data()

    data.append(book)

    save_data(data)

    return "Book created successfully."
