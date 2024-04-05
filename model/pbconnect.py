# 유저와 아이를 연결하는 테이블 정의

from sqlalchemy import Column,String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import DB_Base
import uuid

from model.parent import Parent
from model.baby import Baby

# +-----------+--------------+------+-----+---------+----------------+
# | Field     | Type         | Null | Key | Default | Extra          |
# +-----------+--------------+------+-----+---------+----------------+
# | pbc_id    | int(11)      | NO   | PRI | NULL    | auto_increment |
# | parent_id | varchar(255) | NO   | MUL | NULL    |                |
# | baby_id   | varchar(255) | NO   | MUL | NULL    |                |
# +-----------+--------------+------+-----+---------+----------------+
# CREATE TABLE pbconnect (
#     pbc_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
#     parent_id VARCHAR(255) NOT NULL,
#     baby_id VARCHAR(255) NOT NULL,
#     FOREIGN KEY (parent_id) REFERENCES parent(parent_id),
#     FOREIGN KEY (baby_id) REFERENCES baby(baby_id)
# );

