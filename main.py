from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db
from models import (
    CrewMember,
    EmergencyAlert,
    MapPoint,
    Message,
    Mission,
    MissionLog,
    MissionLogType,
    Notification,
    NotificationType,
    Task,
)
from schemas import (
    CrewBase,
    CrewResponse,
    CrewUpdate,
    EmergencyAlertBase,
    EmergencyAlertResponse,
    MapPointBase,
    MapPointResponse,
    MapPointUpdate,
    MessageBase,
    MessageResponse,
    MessageStatusUpdate,
    MissionLogBase,
    MissionLogResponse,
    MissionResponse,
    MissionUpdate,
    NotificationBase,
    NotificationResponse,
    TaskBase,
    TaskResponse,
    TaskUpdate,
    TriggerEmergency,
)

app = FastAPI(
    title="MarsLink API",
    description="API REST do MarsLink integrada ao Supabase PostgreSQL.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "MarsLink API online", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "marslink-api"}


@app.get("/mission", response_model=MissionResponse)
def get_mission(db: Session = Depends(get_db)):
    mission = db.query(Mission).first()

    if not mission:
        raise HTTPException(status_code=404, detail="Missão não encontrada")

    return mission


@app.put("/mission", response_model=MissionResponse)
def update_mission(payload: MissionUpdate, db: Session = Depends(get_db)):
    mission = db.query(Mission).first()

    if not mission:
        raise HTTPException(status_code=404, detail="Missão não encontrada")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(mission, key, value)

    db.commit()
    db.refresh(mission)

    return mission


@app.get("/messages", response_model=list[MessageResponse])
def get_messages(db: Session = Depends(get_db)):
    return db.query(Message).order_by(Message.created_at.asc()).all()


@app.post("/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_message(payload: MessageBase, db: Session = Depends(get_db)):
    message = Message(**payload.model_dump())
    db.add(message)
    db.flush()

    db.add(
        MissionLog(
            time=message.time,
            type=MissionLogType.message,
            title="Mensagem registrada",
            description=message.content,
            responsible=message.sender,
        )
    )

    db.add(
        Notification(
            title="Nova mensagem registrada",
            description=message.content,
            time=message.time,
            type=NotificationType.message,
            unread=True,
        )
    )

    db.commit()
    db.refresh(message)

    return message


@app.patch("/messages/{message_id}/status", response_model=MessageResponse)
def update_message_status(
    message_id: int,
    payload: MessageStatusUpdate,
    db: Session = Depends(get_db),
):
    message = db.get(Message, message_id)

    if not message:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")

    message.status = payload.status
    db.commit()
    db.refresh(message)

    return message


@app.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(message_id: int, db: Session = Depends(get_db)):
    message = db.get(Message, message_id)

    if not message:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")

    db.delete(message)
    db.commit()


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.created_at.desc()).all()


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskBase, db: Session = Depends(get_db)):
    task = Task(**payload.model_dump())
    db.add(task)
    db.flush()

    db.add(
        MissionLog(
            time="Agora",
            type=MissionLogType.task,
            title="Tarefa criada",
            description=task.title,
            responsible=task.responsible,
        )
    )

    db.add(
        Notification(
            title="Nova tarefa da missão",
            description=task.title,
            time="Agora",
            type=NotificationType.task,
            unread=True,
        )
    )

    db.commit()
    db.refresh(task)

    return task


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    db.delete(task)
    db.commit()


@app.get("/crew", response_model=list[CrewResponse])
def get_crew(db: Session = Depends(get_db)):
    return db.query(CrewMember).order_by(CrewMember.id.asc()).all()


@app.post("/crew", response_model=CrewResponse, status_code=status.HTTP_201_CREATED)
def create_crew_member(payload: CrewBase, db: Session = Depends(get_db)):
    member = CrewMember(**payload.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)

    return member


@app.put("/crew/{member_id}", response_model=CrewResponse)
def update_crew_member(
    member_id: int,
    payload: CrewUpdate,
    db: Session = Depends(get_db),
):
    member = db.get(CrewMember, member_id)

    if not member:
        raise HTTPException(status_code=404, detail="Tripulante não encontrado")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(member, key, value)

    db.commit()
    db.refresh(member)

    return member


@app.delete("/crew/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_crew_member(member_id: int, db: Session = Depends(get_db)):
    member = db.get(CrewMember, member_id)

    if not member:
        raise HTTPException(status_code=404, detail="Tripulante não encontrado")

    db.delete(member)
    db.commit()


@app.get("/notifications", response_model=list[NotificationResponse])
def get_notifications(db: Session = Depends(get_db)):
    return db.query(Notification).order_by(Notification.created_at.desc()).all()


@app.post("/notifications", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
def create_notification(payload: NotificationBase, db: Session = Depends(get_db)):
    notification = Notification(**payload.model_dump())
    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


@app.patch("/notifications/{notification_id}/read", response_model=NotificationResponse)
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.get(Notification, notification_id)

    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")

    notification.unread = False
    db.commit()
    db.refresh(notification)

    return notification


@app.patch("/notifications/read-all", response_model=list[NotificationResponse])
def read_all_notifications(db: Session = Depends(get_db)):
    notifications = db.query(Notification).all()

    for notification in notifications:
        notification.unread = False

    db.commit()

    return db.query(Notification).order_by(Notification.created_at.desc()).all()


@app.delete("/notifications/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.get(Notification, notification_id)

    if not notification:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")

    db.delete(notification)
    db.commit()


@app.get("/emergency-alerts", response_model=list[EmergencyAlertResponse])
def get_emergency_alerts(db: Session = Depends(get_db)):
    return db.query(EmergencyAlert).order_by(EmergencyAlert.id.asc()).all()


@app.post(
    "/emergency-alerts",
    response_model=EmergencyAlertResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_emergency_alert(payload: EmergencyAlertBase, db: Session = Depends(get_db)):
    alert = EmergencyAlert(**payload.model_dump())
    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


@app.post("/emergency-alerts/trigger")
def trigger_emergency_alert(payload: TriggerEmergency, db: Session = Depends(get_db)):
    description = payload.description or "Alerta crítico enviado para a Terra."

    db.add(
        MissionLog(
            time="Agora",
            type=MissionLogType.emergency,
            title=payload.title,
            description=description,
            responsible=payload.responsible,
        )
    )

    db.add(
        Notification(
            title=f"Emergência: {payload.title}",
            description=description,
            time="Agora",
            type=NotificationType.warning,
            unread=True,
        )
    )

    db.commit()

    return {
        "message": "Alerta registrado e colocado na fila de comunicação",
        "status": "queued",
    }


@app.delete("/emergency-alerts/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_emergency_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.get(EmergencyAlert, alert_id)

    if not alert:
        raise HTTPException(status_code=404, detail="Alerta não encontrado")

    db.delete(alert)
    db.commit()


@app.get("/mission-logs", response_model=list[MissionLogResponse])
def get_mission_logs(db: Session = Depends(get_db)):
    return db.query(MissionLog).order_by(MissionLog.created_at.desc()).all()


@app.post(
    "/mission-logs",
    response_model=MissionLogResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_mission_log(payload: MissionLogBase, db: Session = Depends(get_db)):
    log = MissionLog(**payload.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)

    return log


@app.delete("/mission-logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mission_log(log_id: int, db: Session = Depends(get_db)):
    log = db.get(MissionLog, log_id)

    if not log:
        raise HTTPException(status_code=404, detail="Log não encontrado")

    db.delete(log)
    db.commit()


@app.get("/map-points", response_model=list[MapPointResponse])
def get_map_points(db: Session = Depends(get_db)):
    return db.query(MapPoint).order_by(MapPoint.id.asc()).all()


@app.post(
    "/map-points",
    response_model=MapPointResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_map_point(payload: MapPointBase, db: Session = Depends(get_db)):
    point = MapPoint(**payload.model_dump())
    db.add(point)
    db.commit()
    db.refresh(point)

    return point


@app.put("/map-points/{point_id}", response_model=MapPointResponse)
def update_map_point(
    point_id: int,
    payload: MapPointUpdate,
    db: Session = Depends(get_db),
):
    point = db.get(MapPoint, point_id)

    if not point:
        raise HTTPException(status_code=404, detail="Ponto do mapa não encontrado")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(point, key, value)

    db.commit()
    db.refresh(point)

    return point


@app.delete("/map-points/{point_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_map_point(point_id: int, db: Session = Depends(get_db)):
    point = db.get(MapPoint, point_id)

    if not point:
        raise HTTPException(status_code=404, detail="Ponto do mapa não encontrado")

    db.delete(point)
    db.commit()