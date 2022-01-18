from pydantic import BaseModel
import datetime
from typing import Optional, Dict, List, Union

class Update(BaseModel):
    classId: int
    faceStatus: bool
    tabStatus: bool
    faces: int
    studentId: int

class host(BaseModel):
    name: str
    class_no: int


class classInfo(BaseModel):
    course_name: str
    period: int
    present: list

class createClass(BaseModel):
    host: host
    date: datetime.datetime
    department: str
    name: str
    class_info: classInfo
    created_at: datetime.datetime
    session: dict
    ended_at: datetime.datetime
