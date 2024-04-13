from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
from typing import Optional


# 부모 테이블
# +---------------+--------------+------+-----+---------+-------+
# | Field         | Type         | Null | Key | Default | Extra |
# +---------------+--------------+------+-----+---------+-------+
# | parent_id     | varchar(255) | NO   | PRI | NULL    |       |
# | password      | varchar(255) | YES  |     | NULL    |       |
# | email         | varchar(255) | NO   |     | NULL    |       |
# | name          | varchar(50)  | YES  |     | NULL    |       |
# | nickname      | varchar(255) | NO   |     | NULL    |       |
# | signInMethod  | varchar(50)  | YES  |     | NULL    |       |
# | emailVerified | tinyint(1)   | YES  |     | NULL    |       |
# | photoId       | varchar(255) | YES  |     | NULL    |       |
# | description   | varchar(255) | YES  |     | NULL    |       |
# +---------------+--------------+------+-----+---------+-------+
# CREATE TABLE parent(
#     parent_id VARCHAR(255) PRIMARY KEY NOT NULL,
#     password VARCHAR(255) NOT NULL,
#     email VARCHAR(255) UNIQUE NOT NULL,
#     name VARCHAR(50) NOT NULL,
#     nickname VARCHAR(255) NOT NULL,
#     signInMethod VARCHAR(50) NOT NULL,
#     emailVerified VARCHAR(255) NOT NULL,
#     photoId VARCHAR(255),
#     description VARCHAR(255)
# );



class Parent(BaseModel):
    parent_id: str
    password: str
    email: str
    name: str
    nickname: str
    signInMethod: str
    emailVerified: str
    photoId: Optional[str]
    description: Optional[str]

    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))

    class Config:
        orm_mode = True
        use_enum_values = True

    def __init__(self, **kwargs):
        if '_sa_instance_state' in kwargs:
            kwargs.pop('_sa_instance_state')
        super().__init__(**kwargs)


class ParentTable(DB_Base):
    __tablename__ = 'parent'
    parent_id = Column(String(255), primary_key=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    nickname = Column(String(255), nullable=False)
    signInMethod = Column(String(50), nullable=False)
    emailVerified = Column(String(255), nullable=False)
    photoId = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)

    # Relationship to Baby
    # babies = relationship(BabyTable, backref='parents', passive_deletes=True)

# CREATE TABLE parent (
#     uid VARCHAR(255) UNIQUE NOT NULL,
#     email VARCHAR(255) NOT NULL,
#     nickname VARCHAR(255) NOT NULL,
#     signInMethod VARCHAR(50) DEFAULT 'email',
#     emailVerified BOOLEAN DEFAULT FALSE,
#     photoId TEXT,
#     description TEXT,
#     PRIMARY KEY (uid),
#     INDEX (email)
# );
