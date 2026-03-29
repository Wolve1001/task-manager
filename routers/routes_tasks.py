from fastapi import APIRouter
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
from task_service.tasks_today import *
from task_service.add_tasks import *
from task_service.delete_tasks import *
from task_service.update_tasks import *

router = APIRouter()
scheduler = BackgroundScheduler()

class Task(BaseModel):
    task_name: str
    due_date: date
    recurring: str = None
    notify_at: datetime = None
    category: str = None

# tested and passed
@router.get("/tasks/today/{user_name}")
def tasks_today(user_name: str, sort: str = None):
    return task_today(user_name, sort)

# tested and passed
@router.get("/tasks/notifications/{user_name}")
def task_by_notifications(user_name: str, notify_at: datetime, sort: str = None):
    return task_by_notification(user_name, notify_at, sort)

@router.get("/tasks/categories/{user_name}")
def task_by_categories(user_name: str, category: str, sort: str = None):
    return task_by_category(user_name, category, sort)

# tested and passed
@router.post("/tasks/add/{user_name}")
def add_tasks(user_name: str, task: Task):
    return add_task(user_name, task.task_name, task.due_date, task.recurring, task.notify_at, task.category)

# tested and passed
@router.delete("/tasks/delete/{task_id}")
def delete_tasks(task_id: int):
    return delete_task(task_id)

# tested and passed
@router.delete("/tasks/deactivate/{task_id}")
def deactivate_tasks(task_id: int):
    return deactivate_task(task_id)

@router.put("/tasks/update/{task_id}")
def update_tasks(task_id: int, task_name: str, due_date: date = None, recurring: str = None):
    return update_task(task_id, task_name, due_date, recurring)

@router.put("/tasks/mark_done/{task_id}")
def mark_tasks_done(task_id: int):
    return mark_task_done(task_id)

@router.put("/tasks/recurring")
def recurring_tasks():
    return recurring_task()