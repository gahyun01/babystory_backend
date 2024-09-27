from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from model.post import *


# 게시물 생성
class CreatePostInput(BaseModel):
    reveal: int
    title: str
    content: str
    hashList: Optional[str] = None


class CreatePostOutput(BaseModel):
    post: Optional[Post] = None


# 게시물 사진
class UploadPhotoOutput(BaseModel):
    success: bool


# 모든 게시물 가져오기
class PostGetOupPut(BaseModel):
    post_id: int
    parent_id: str
    reveal: int
    title: str
    createTime: datetime
    modifyTime: Optional[datetime] = None
    pHeart: Optional[int] = None
    pView: Optional[int] = None
    pScript: Optional[int] = None
    pComment: Optional[int] = None
    hashList: Optional[str] = None
    content: str

# 게시물 수정


class UpdatePostInput(BaseModel):
    post_id: int
    reveal: int
    title: str
    content: str
    hashList: Optional[str] = None


class UpdatePostOutput(BaseModel):
    success: int
    post: Post


# 게시물 삭제
class DeletePostInput(BaseModel):
    post_id: int


class DeletePostOutput(BaseModel):
    success: int
    post: Optional[Post] = None
