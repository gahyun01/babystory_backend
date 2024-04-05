# 유저간의 연결 테이블 정의

from sqlalchemy import Column,String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
import uuid

from model.parent import Parent

# +------------+--------------+------+-----+---------+-------+
# | Field      | Type         | Null | Key | Default | Extra |
# +------------+--------------+------+-----+---------+-------+
# | ppc_id     | int(11)      | NO   | PRI | NULL    |       |
# | parent_id1 | varchar(255) | NO   | MUL | NULL    |       |
# | parent_id2 | varchar(255) | NO   | MUL | NULL    |       |
# +------------+--------------+------+-----+---------+-------+
# CREATE TABLE ppconnect (
#     ppc_id INT PRIMARY KEY NOT NULL,
#     parent_id1 VARCHAR(255) NOT NULL,
#     parent_id2 VARCHAR(255) NOT NULL,
#     FOREIGN KEY (parent_id1) REFERENCES parent(parent_id),
#     FOREIGN KEY (parent_id2) REFERENCES parent(parent_id)
# );

class PPConnect(BaseModel):
    ppc_id: int
    parent_id1: str
    parent_id2: str

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))
    
    class Config:
        orm_mode = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)

class PPConnectTable(DB_Base):
    __tablename__ = 'ppconnect'
    ppc_id = Column(String(36), primary_key=True, default=uuid.uuid4)
    parent_id1 = Column(String(255), ForeignKey(
        'parent.parent_id', ondelete='SET NULL'))
    parent_id2 = Column(String(255), ForeignKey(
        'parent.parent_id', ondelete='SET NULL'))
    
    parent1 = relationship(Parent, backref='ppconnect', passive_deletes=True)
    parent2 = relationship(Parent, backref='ppconnect', passive_deletes=True)