from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List



app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: bool 




tasks_db = []


@app.get("/tasks", response_class=HTMLResponse)
def get_tasks(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks_db})

@app.get("/tasks/{task_id}", response_class=HTMLResponse)
def get_task_html(request: Request, task_id: int):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task good found")
    return templates.TemplateResponse("index.html", {"request": request, "task": task})


@app.post("/tasks", response_model=Task, response_class=HTMLResponse)
def create_task(task: Task, request: Request):
    
    new_task = {"id": len(tasks_db) + 1, **task.__dict__}
    tasks_db.append(new_task)
    
    return templates.TemplateResponse("index.html", {"request": request, "task": new_task})


@app.put("/tasks/{task_id}", response_model=Task, response_class=HTMLResponse)
def update_task(task_id: int, updated_task: Task, request: Request):
    task_index = next((i for i, t in enumerate(tasks_db) if t["id"] == task_id), None)
    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task_dict = updated_task.__dict__
    tasks_db[task_index] = {tasks_db[task_index], updated_task_dict}
    return templates.TemplateResponse("index.html", {"request": request, "task": tasks_db[task_index]})


@app.delete("/tasks/{task_id}", response_class=HTMLResponse)
def delete_task(task_id: int, request: Request):

    task_index = next((i for i, t in enumerate(tasks_db) if t["id"] == task_id), None)
    if task_index is None:
        raise HTTPException(status_code=404, detail="Task not found")

    deleted_task = tasks_db.pop(task_index)
    
    return templates.TemplateResponse("index.html", {"request": request, "task_id": task_id})








#pip install fastapi uvicorn[standard]
#uvicorn main:app --reload
