from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from database import engine, Base, SessionLocal
import models, schemas, auth

Base.metadata.create_all(bind=engine)
with engine.begin() as connection:
    user_columns = [row[1] for row in connection.execute(text("PRAGMA table_info(users)"))]
    if user_columns and "is_admin" not in user_columns:
        connection.execute(text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0"))
        connection.execute(text("UPDATE users SET is_admin = 1 WHERE id = 3"))
    task_columns = [row[1] for row in connection.execute(text("PRAGMA table_info(tasks)"))]
    if task_columns and "owner_id" not in task_columns:
        connection.execute(text("ALTER TABLE tasks ADD COLUMN owner_id INTEGER"))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=auth.hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created", "user_id": new_user.id}

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = auth.create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer", "user": {"id": db_user.id, "username": db_user.username, "email": db_user.email}}

@app.post("/admin/login")
def admin_login(credentials: schemas.AdminLogin, db: Session = Depends(get_db)):
    admin_identifier = str(credentials.admin_id)
    admin = db.query(models.User).filter(models.User.email == admin_identifier).first()
    if not admin and admin_identifier.isdigit():
        admin = db.query(models.User).filter(models.User.id == int(admin_identifier)).first()
    if not admin or not admin.is_admin or not auth.verify_password(credentials.password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid admin ID or password")
    token = auth.create_access_token({"sub": str(admin.id), "role": "admin"})
    return {"access_token": token, "token_type": "bearer", "user": {"id": admin.id, "username": admin.username, "email": admin.email}}

@app.get("/me")
def current_user(db: Session = Depends(get_db), user_id: int = Depends(auth.get_current_user_id)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username, "email": user.email}

@app.get("/users")
def list_users(db: Session = Depends(get_db), user_id: int = Depends(auth.get_current_user_id)):
    users = db.query(models.User).all()
    return [{"id": u.id, "username": u.username, "email": u.email} for u in users]

@app.get("/users/{member_id}")
def get_user(member_id: int, db: Session = Depends(get_db), user_id: int = Depends(auth.get_current_user_id)):
    user = db.query(models.User).filter(models.User.id == member_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Member not found")
    tasks = db.query(models.Task).filter(models.Task.owner_id == member_id).all()
    return {"id": user.id, "username": user.username, "email": user.email,
            "stats": {"tasks": len(tasks), "completed": len([t for t in tasks if t.status == "done"]),
                       "in_progress": len([t for t in tasks if t.status == "in_progress"])}}

@app.get("/search")
def search(q: str = "", db: Session = Depends(get_db), user_id: int = Depends(auth.get_current_user_id)):
    query = q.strip().lower()
    projects = db.query(models.Project).all()
    tasks = db.query(models.Task).all()
    users = db.query(models.User).all()
    return {"projects": [{"id": p.id, "name": p.name, "description": p.description} for p in projects if query in p.name.lower() or query in (p.description or "").lower()],
            "tasks": [{"id": t.id, "title": t.title, "status": t.status} for t in tasks if query in t.title.lower()],
            "members": [{"id": u.id, "username": u.username, "email": u.email} for u in users if query in u.username.lower() or query in u.email.lower()]}

@app.get("/admin/users")
def admin_users(db: Session = Depends(get_db), admin_id: int = Depends(auth.get_current_admin_id)):
    return [{"id": u.id, "username": u.username, "email": u.email, "is_admin": bool(u.is_admin)} for u in db.query(models.User).all()]

@app.put("/admin/users/{member_id}")
def admin_update_user(member_id: int, update: schemas.AdminUserUpdate, db: Session = Depends(get_db), admin_id: int = Depends(auth.get_current_admin_id)):
    user = db.query(models.User).filter(models.User.id == member_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Member not found")
    duplicate = db.query(models.User).filter(models.User.email == update.email, models.User.id != member_id).first()
    if duplicate:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.username, user.email, user.is_admin = update.username, update.email, update.is_admin
    if update.password:
        user.hashed_password = auth.hash_password(update.password)
    db.commit(); db.refresh(user)
    return {"id": user.id, "username": user.username, "email": user.email, "is_admin": bool(user.is_admin)}

@app.delete("/admin/users/{member_id}")
def admin_delete_user(member_id: int, db: Session = Depends(get_db), admin_id: int = Depends(auth.get_current_admin_id)):
    if member_id == admin_id:
        raise HTTPException(status_code=400, detail="You cannot delete the active admin account")
    user = db.query(models.User).filter(models.User.id == member_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(user); db.commit(); return {"message": "Member deleted"}

@app.put("/admin/projects/{project_id}")
@app.post("/admin/projects/{project_id}")
def admin_update_project(project_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db), admin_id: int = Depends(auth.get_current_admin_id)):
    item = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not item: raise HTTPException(status_code=404, detail="Project not found")
    item.name, item.description = project.name, project.description; db.commit(); db.refresh(item); return item

@app.delete("/admin/projects/{project_id}")
def admin_delete_project(project_id: int, db: Session = Depends(get_db), admin_id: int = Depends(auth.get_current_admin_id)):
    item = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not item: raise HTTPException(status_code=404, detail="Project not found")
    db.query(models.Task).filter(models.Task.project_id == project_id).delete(); db.delete(item); db.commit(); return {"message": "Project deleted"}

@app.post("/admin/tasks")
def admin_create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), admin_id: int = Depends(auth.get_current_admin_id)):
    item = models.Task(title=task.title, status=task.status, project_id=task.project_id, owner_id=task.owner_id or admin_id)
    db.add(item); db.commit(); db.refresh(item); return item

@app.put("/admin/tasks/{task_id}")
@app.post("/admin/tasks/{task_id}")
def admin_update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), admin_id: int = Depends(auth.get_current_admin_id)):
    item = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not item: raise HTTPException(status_code=404, detail="Task not found")
    item.title, item.status, item.project_id = task.title, task.status, task.project_id
    if task.owner_id is not None: item.owner_id = task.owner_id
    db.commit(); db.refresh(item); return item

@app.delete("/admin/tasks/{task_id}")
def admin_delete_task(task_id: int, db: Session = Depends(get_db), admin_id: int = Depends(auth.get_current_admin_id)):
    item = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not item: raise HTTPException(status_code=404, detail="Task not found")
    db.delete(item); db.commit(); return {"message": "Task deleted"}

@app.post("/projects")
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), user_id: int = Depends(auth.get_current_user_id)):
    new_project = models.Project(name=project.name, description=project.description)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@app.get("/projects")
def list_projects(db: Session = Depends(get_db), user_id: int = Depends(auth.get_current_user_id)):
    return db.query(models.Project).all()

@app.post("/tasks")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), user_id: int = Depends(auth.get_current_user_id)):
    new_task = models.Task(title=task.title, status=task.status, project_id=task.project_id, owner_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks")
def list_tasks(db: Session = Depends(get_db), user_id: int = Depends(auth.get_current_user_id)):
    return db.query(models.Task).all()

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db), user_id: int = Depends(auth.get_current_user_id)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = task.title
    db_task.status = task.status
    db.commit()
    db.refresh(db_task)
    return db_task
