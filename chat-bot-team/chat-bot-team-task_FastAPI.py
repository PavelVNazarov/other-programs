from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

app = FastAPI()

# Создаем словарь с задачами
schedule: Dict[str, List[str]] = {}

class Task(BaseModel):
    colleague_name: str
    task: str

class Colleague(BaseModel):
    name: str

@app.get("/")
def read_root():
    return {"message": "Привет! Я твой бот-помощник для управления задачами."}

@app.get("/tasks")
def get_all_tasks():
    return schedule

@app.get("/tasks/{colleague_name}")
def get_tasks_by_colleague(colleague_name: str):
    tasks = schedule.get(colleague_name)
    if tasks is None:
        raise HTTPException(status_code=404, detail="Коллега не найден")
    return {colleague_name: tasks}

@app.post("/tasks/add", response_model=Dict[str, List[str]])
def add_task(task: Task):
    if task.colleague_name not in schedule:
        schedule[task.colleague_name] = []
    schedule[task.colleague_name].append(task.task)
    return schedule

@app.post("/colleagues/add", response_model=Dict[str, List[str]])
def add_colleague(colleague: Colleague):
    if colleague.name not in schedule:
        schedule[colleague.name] = []
    return schedule

@app.delete("/tasks/{colleague_name}/{task_item}")
def delete_task(colleague_name: str, task_item: str):
    if colleague_name in schedule:
        try:
            schedule[colleague_name].remove(task_item)
            return schedule
        except ValueError:
            raise HTTPException(status_code=404, detail="Задача не найдена")
    else:
        raise HTTPException(status_code=404, detail="Коллега не найден")

# Объяснение кода:
# FastAPI: Используется для создания веб-приложения.
# schedule: Словарь для хранения задач. Ключами являются имена коллег, значениями — списки задач.
# Pydantic: Модели Task и Colleague используются для валидации входящих данных.
# Метод get_all_tasks позволяет получить все задачи.
# Метод get_tasks_by_colleague позволяет увидеть задачи для конкретного коллеги.
# add_task и add_colleague позволяют добавлять задачи и коллег соответственно.
# delete_task позволяет удалить задачу для конкретного коллеги.
# Запуск приложения:
# Убедитесь, что у Вас установлен FastAPI и Uvicorn:
# pip install fastapi[all]
# Сохраните код в файл, например, app.py.
# Запустите приложение:
# uvicorn app:app --reload
# Откройте браузер и перейдите на http://127.0.0.1:8000/docs, чтобы увидеть документацию API и тестировать его.
# Теперь Ваше приложение FastAPI готово для работы. Вы можете управлять задачами коллег через API-запросы!
