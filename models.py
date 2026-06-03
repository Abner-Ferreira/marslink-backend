from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, Integer, String, Text

from database import Base


def enum_values(enum_class):
    return [item.value for item in enum_class]


class MissionStatus(str, Enum):
    active = "active"
    warning = "warning"
    critical = "critical"


class MessageStatus(str, Enum):
    sending = "sending"
    in_transit = "in_transit"
    received = "received"
    confirmed = "confirmed"


class MessageDirection(str, Enum):
    sent = "sent"
    received = "received"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class TaskStatus(str, Enum):
    pending = "Pendente"
    in_progress = "Em andamento"
    done = "Concluída"


class NotificationType(str, Enum):
    message = "message"
    task = "task"
    system = "system"
    warning = "warning"


class EmergencyPriority(str, Enum):
    medium = "medium"
    high = "high"
    critical = "critical"


class MissionLogType(str, Enum):
    message = "message"
    task = "task"
    health = "health"
    system = "system"
    emergency = "emergency"


class MapPointType(str, Enum):
    base = "base"
    sample = "sample"
    solar = "solar"
    antenna = "antenna"
    danger = "danger"


class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(160), nullable=False)
    sol = Column(Integer, nullable=False, default=1)
    status = Column(
        SQLEnum(MissionStatus, values_callable=enum_values),
        nullable=False,
        default=MissionStatus.active,
    )
    location = Column(String(180), nullable=False)
    communication_window = Column(String(20), nullable=False)
    latency = Column(String(40), nullable=False)
    oxygen = Column(Integer, nullable=False, default=100)
    energy = Column(Integer, nullable=False, default=100)
    temperature = Column(String(30), nullable=False)
    external_condition = Column(String(120), nullable=False, default="Estável")
    communication_status = Column(String(120), nullable=False, default="Janela aberta")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String(120), nullable=False)
    content = Column(Text, nullable=False)
    time = Column(String(20), nullable=False)
    status = Column(
        SQLEnum(MessageStatus, values_callable=enum_values),
        nullable=False,
        default=MessageStatus.sending,
    )
    direction = Column(
        SQLEnum(MessageDirection, values_callable=enum_values),
        nullable=False,
        default=MessageDirection.received,
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(220), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(
        SQLEnum(TaskPriority, values_callable=enum_values),
        nullable=False,
        default=TaskPriority.medium,
    )
    responsible = Column(String(120), nullable=False)
    due = Column(String(80), nullable=False)
    status = Column(
        SQLEnum(TaskStatus, values_callable=enum_values),
        nullable=False,
        default=TaskStatus.pending,
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class CrewMember(Base):
    __tablename__ = "crew"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    role = Column(String(120), nullable=False)
    bpm = Column(Integer, nullable=False)
    oxygen = Column(Integer, nullable=False)
    temperature = Column(String(30), nullable=False)
    pressure = Column(String(30), nullable=False)
    status = Column(String(40), nullable=False, default="OK")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(220), nullable=False)
    description = Column(Text, nullable=False)
    time = Column(String(20), nullable=False)
    type = Column(
        SQLEnum(NotificationType, values_callable=enum_values),
        nullable=False,
        default=NotificationType.system,
    )
    unread = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class EmergencyAlert(Base):
    __tablename__ = "emergency_alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(220), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(
        SQLEnum(EmergencyPriority, values_callable=enum_values),
        nullable=False,
        default=EmergencyPriority.high,
    )


class MissionLog(Base):
    __tablename__ = "mission_logs"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(String(20), nullable=False)
    type = Column(
        SQLEnum(MissionLogType, values_callable=enum_values),
        nullable=False,
        default=MissionLogType.system,
    )
    title = Column(String(220), nullable=False)
    description = Column(Text, nullable=False)
    responsible = Column(String(120), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class MapPoint(Base):
    __tablename__ = "map_points"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(160), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(
        SQLEnum(MapPointType, values_callable=enum_values),
        nullable=False,
        default=MapPointType.base,
    )
    status = Column(String(120), nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)