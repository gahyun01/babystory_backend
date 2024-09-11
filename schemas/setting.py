from typing import Optional, List
from datetime import datetime

from model.post import *
from schemas.pagination import *

class SettingOverviewOutputData(BaseModel):
    mateCount: int
    friendCount: int
    myStoryCount: int

class SettingOverviewOutputService(BaseModel):
    status: int
    message: str
    data: SettingOverviewOutputData

class FriendsParent(BaseModel):
    parent_id: str
    nickname: str
    photoId: Optional[str]
    description: Optional[str]
    isMate: bool

class MyFriendsOutputService(BaseModel):
    paginationInfo: PaginationInfo
    parents: List[FriendsParent]

class MyFriendsOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    parents: List[FriendsParent]

class Post(BaseModel):
    post_id: int
    title: str
    createTime: Optional[datetime]
    pHeart: Optional[int]
    pScript: Optional[int]
    pView: Optional[int]
    pComment: Optional[int]
    hashList: Optional[str]
    contentPreview: str
    photo_id: Optional[str]

class MyViewsPostOutputService(BaseModel):
    paginationInfo: PaginationInfo
    post: list[Post]

class MyViewsPostOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    post: list[Post]

class MyScriptsPostOutputService(BaseModel):
    paginationInfo: PaginationInfo
    post: list[Post]

class MyScriptsPostOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    post: list[Post]

class MyLikesPostOutputService(BaseModel):
    paginationInfo: PaginationInfo
    post: list[Post]

class MyLikesPostOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    post: list[Post]

class MyStoriesPost(BaseModel):
    post_id: int
    title: str
    createTime: Optional[datetime]
    pHeart: Optional[int]
    pScript: Optional[int]
    pView: Optional[int]
    pComment: Optional[int]
    hashList: Optional[str]
    contentPreview: str
    photo_id: Optional[str]

class MyStoriesOutputService(BaseModel):
    paginationInfo: PaginationInfo
    post: list[MyStoriesPost]

class MyStoriesOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    post: list[MyStoriesPost]

class MatesParent(BaseModel):
    parent_id: str
    nickname: str
    photoId: Optional[str]
    description: Optional[str]

class MyMatesOutputService(BaseModel):
    paginationInfo: PaginationInfo
    parents: list[MatesParent]

class MyMatesOutput(BaseModel):
    status: str
    message: str
    paginationInfo: PaginationInfo
    parents: list[MatesParent]