from datetime import datetime

from pydantic import BaseModel

from models import (
    EmergencyPriority,
    MapPointType,
    MessageDirection,
    MessageStatus,
    MissionLogType,
    MissionStatus,
    NotificationType,
    TaskPriority,
    TaskStatus,
)


class MissionBase(BaseModel):
    name: str
    sol: int
    status: MissionStatus
    location: str
    communication_window: str
    latency: str
    oxygen: int
    energy: int
    temperature: str
    external_condition: str
    communication_status: str


class MissionUpdate(BaseModel):
    name: str | None = None
    sol: int | None = None
    status: MissionStatus | None = None
    location: str | None = None
    communication_window: str | None = None
    latency: str | None = None
    oxygen: int | None = None
    energy: int | None = None
    temperature: str | None = None
    external_condition: str | None = None
    communication_status: str | None = None


class MissionResponse(MissionBase):
    id: int

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    sender: str
    content: str
    time: str
    status: MessageStatus = MessageStatus.sending
    direction: MessageDirection = MessageDirection.received


class MessageStatusUpdate(BaseModel):
    status: MessageStatus


class MessageResponse(MessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    description: str
    priority: TaskPriority
    responsible: str
    due: str
    status: TaskStatus


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: TaskPriority | None = None
    responsible: str | None = None
    due: str | None = None
    status: TaskStatus | None = None


class TaskResponse(TaskBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CrewBase(BaseModel):
    name: str
    role: str
    bpm: int
    oxygen: int
    temperature: str
    pressure: str
    status: str = "OK"


class CrewUpdate(BaseModel):
    name: str | None = None
    role: str | None = None
    bpm: int | None = None
    oxygen: int | None = None
    temperature: str | None = None
    pressure: str | None = None
    status: str | None = None


class CrewResponse(CrewBase):
    id: int

    class Config:
        from_attributes = True


class NotificationBase(BaseModel):
    title: str
    description: str
    time: str
    type: NotificationType
    unread: bool = True


class NotificationResponse(NotificationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class EmergencyAlertBase(BaseModel):
    title: str
    description: str
    priority: EmergencyPriority


class EmergencyAlertResponse(EmergencyAlertBase):
    id: int

    class Config:
        from_attributes = True


class TriggerEmergency(BaseModel):
    title: str
    description: str | None = None
    responsible: str = "Tripulação"


class MissionLogBase(BaseModel):
    time: str
    type: MissionLogType
    title: str
    description: str
    responsible: str


class MissionLogResponse(MissionLogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MapPointBase(BaseModel):
    name: str
    description: str
    type: MapPointType
    status: str
    x: float
    y: float


class MapPointUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    type: MapPointType | None = None
    status: str | None = None
    x: float | None = None
    y: float | None = None


class MapPointResponse(MapPointBase):
    id: int

    class Config:
        from_attributes = True
