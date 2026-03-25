from fastapi import FastAPI
from routers import routes_tasks
from apscheduler.schedulers.background import BackgroundScheduler
from task_service.update_tasks import recurring_task

app = FastAPI()
scheduler = BackgroundScheduler()

app.include_router(routes_tasks.router)

@app.on_event("startup")
def start_scheduler():
    scheduler.start()
    scheduler.add_job(recurring_task, "interval", hours=24)

@app.on_event("shutdown")
def shutdown_schceduler():
    scheduler.shutdown()