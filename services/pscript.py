from fastapi import HTTPException
from typing import Optional, List, Set
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from db import get_db_session

from model.pscript import PScriptTable
from schemas.pscript import *
from error.exception.customerror import *



class PScriptService:

    # 스크립트 관리
    def managePScript(self, managePScriptInput: ManagePScriptInput, parent_id:str) -> ManagePScriptOutput:
        """
        스크립트 관리
        --input
            - managePScriptInput.post_id: 게시물 아이디
        --output
            - PScript: 스크립트 딕셔너리
        """
        db = get_db_session()

        pscript = db.query(PScriptTable).filter(
            PScriptTable.post_id == managePScriptInput.post_id,
            PScriptTable.parent_id == parent_id
        ).first()

        if pscript is None:
            new_pscript = PScriptTable(
                post_id=managePScriptInput.post_id,
                parent_id = parent_id,
                createTime = datetime.now()
            )

            try:
                db.add(new_pscript)
                db.commit()
                db.refresh(new_pscript)
                return {'hasCreated': True, 'message': 'Success to create pscript', 'pscript': new_pscript}
            
            except Exception as e:
                db.rollback()
                raise e

        else:
            try:
                db.delete(pscript)
                db.commit()
                return {'hasCreated': False, 'message': 'Success to delete pscript', 'pscript': pscript}
            
            except Exception as e:
                db.rollback()


    # 스크립트 생성
    def createPScript(self, createPScriptInput: CreatePScriptInput, parent_id: str) -> Optional[PScript]:
        """
        스크립트 생성
        --input
            - createScriptInput.post_id: 게시물 아이디
            - createScriptInput.parent_id: 스크립트한 부모 아이디
        --output
            - Script: 스크립트 딕셔너리
        """
        db = get_db_session()

        pscript = PScriptTable(
            post_id=createPScriptInput.post_id,
            parent_id=parent_id,
            createTime=datetime.now()
        )

        db.add(pscript)
        db.commit()
        db.refresh(pscript)

        return pscript


    # 스크립트 삭제
    def deletePScript(self, deletePScriptInput: DeletePScriptInput, parent_id: str) -> Optional[PScript]:
        """
        스크립트 삭제
        --input
            - deletePScriptInput.post_id: 게시물 아이디
            - deletePScriptInput.parent_id: 스크립트한 부모 아이디
        --output
            - PScript: 스크립트 딕셔너리
        """
        db = get_db_session()

        post_id = [int(num.strip()) for num in deletePScriptInput.post_id.split(",")]

        pscripts = []
        for i in post_id:
            pscript = db.query(PScriptTable).filter(
                PScriptTable.post_id == i,
                PScriptTable.parent_id == parent_id
            ).first()

            # pscript가 없을 경우 CustomException을 발생시킵니다.
            if pscript is None:
                raise CustomException("PScript not found")

            db.delete(pscript)
            db.commit()

            pscripts.append(pscript)

        return pscripts
    

    # 스크립트 조회
    def hasScript(self, post_id: int, parent_id: str) -> HasScriptOutput:
        """
        스크립트 조회
        --input
            - post_id: 게시물 아이디
        --output
            - status: 상태 코드
            - message: 메시지
            - state: 스크립트 상태
        """
        db = get_db_session()

        pscript = db.query(PScriptTable).filter(
            PScriptTable.post_id == post_id,
            PScriptTable.parent_id == parent_id
        ).first()
        
        return True if pscript else False