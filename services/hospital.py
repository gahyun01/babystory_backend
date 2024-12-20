from fastapi import HTTPException, UploadFile
from typing import Optional, List
from sqlalchemy import text
from sqlalchemy.orm import joinedload
from constants.path import *
from sqlalchemy.exc import SQLAlchemyError

from datetime import datetime
from sqlalchemy import func
import os

from schemas.hospital import *
from model.hospital import *
from model.diary import *
from db import get_db_session
from error.exception.customerror import *


class HospitalService:

    # 산모수첩 생성
    def createHospital(self, parent_id: str, createHospitalInput: CreateHospitalInput) -> Hospital:
        """
        산모수첩 생성
        - input
            - parent_id (str): 부모 아이디
            - createHospitalInput (CreateHospitalInput): 산모수첩 생성 정보
        - output
            - hospital (Hospital): 산모수첩 딕셔너리
        """

        db = get_db_session()
        print("createHospitalInput: ", createHospitalInput)

        diary = db.query(DiaryTable).filter(
            DiaryTable.diary_id == createHospitalInput.diary_id,
            DiaryTable.parent_id == parent_id,
            DiaryTable.deleteTime == None).first()

        if diary is None:
            print("Diary does not exist")
            raise CustomException("Diary does not exist")

        if diary.born != 0:
            print("This diary is not a maternity diary")
            raise CustomException("This diary is not a maternity diary")

        createTime = datetime.strptime(
            createHospitalInput.createTime, "%Y-%m-%d")

        hospitals = db.query(HospitalTable).filter(
            HospitalTable.diary_id == createHospitalInput.diary_id,
            func.date(HospitalTable.createTime) == createTime,
            HospitalTable.deleteTime == None).first()

        if hospitals is not None:
            print("Hospital already exists")
            raise CustomException("Hospital already exists")

        next = None
        if createHospitalInput.next_day:
            next = datetime.strptime(
                createHospitalInput.next_day, "%Y-%m-%d, %H:%M")

        hospital = HospitalTable(
            diary_id=createHospitalInput.diary_id,
            baby_id=diary.baby_id,
            createTime=createTime,
            parent_kg=createHospitalInput.parent_kg,
            bpressure=createHospitalInput.bpressure,
            baby_kg=createHospitalInput.baby_kg,
            baby_cm=createHospitalInput.baby_cm,
            special=createHospitalInput.special,
            next_day=next
        )

        try:
            db.add(hospital)
            db.commit()
            db.refresh(hospital)
        except Exception as e:
            db.rollback()
            raise HTTPException("Failed to create hospital")

        return hospital

    # 범위 대한 전체 산모수첩 조회

    def getRangeHospital(self, parent_id: str,
                         diary_id: int, start: str, end: str) -> List[Hospital]:
        """
        다이어리에 대한 전체 산모수첩 조회
        - input
            - parent_id (str): 부모 아이디
            - diary_id (int): 다이어리 아이디
            - start (str): 시작 날짜
            - end (str): 끝 날짜
        - output
            - hospitals (List[GetHospitalOutput]): 산모수첩 딕셔너리 리스트
        """

        db = get_db_session()

        diary = db.query(DiaryTable).filter(
            DiaryTable.diary_id == diary_id,
            DiaryTable.parent_id == parent_id,
            DiaryTable.deleteTime == None).first()

        if diary is None:
            raise CustomException("Diary does not exist")

        if diary.born != 0:
            raise CustomException("This diary is not a maternity diary")

        start = datetime.strptime(start, "%Y-%m-%d")
        end = datetime.strptime(end, "%Y-%m-%d")

        hospital = db.query(HospitalTable).filter(
            HospitalTable.diary_id == diary_id,
            func.date(HospitalTable.createTime) >= start,
            func.date(HospitalTable.createTime) <= end,
            HospitalTable.deleteTime == None).all()

        hospitals = []

        if hospital is None:
            return hospitals

        for h in hospital:
            specials = {}
            if any(special_string in h.special for special_string in [" /seq ", " /split "]):
                special = h.special.split(" /seq ")
                for s in special:
                    key, value = s.split(" /split ")
                    specials[key] = value

            hospitals.append({
                'hospital_id': h.hospital_id,
                'diary_id': h.diary_id,
                'baby_id': h.baby_id,
                'createTime': h.createTime,
                'modifyTime': h.modifyTime,
                'parent_kg': h.parent_kg,
                'bpressure': h.bpressure,
                'baby_kg': h.baby_kg,
                'baby_cm': h.baby_cm,
                'special': specials,
                'next_day': h.next_day
            })
        hospitals.reverse()
        return hospitals

    # 모든 산모수첩 조회
    def getAllHospital(self, parent_id: str, diary_id: int) -> List[Hospital]:
        """
        모든 산모수첩 조회
        - input
            - parent_id (str): 부모 아이디
        - output
            - hospitals (List[GetHospitalOutput]): 산모수첩 딕셔너리 리스트
        """

        db = get_db_session()

        diary = db.query(DiaryTable).filter(
            DiaryTable.diary_id == diary_id,
            DiaryTable.parent_id == parent_id).first()

        if diary is None or diary.deleteTime is not None:
            raise CustomException("Diary does not exist")

        if diary.born != 0:
            raise CustomException("This diary is not a maternity diary")

        print(f"diary_id: {diary_id}")
        hospitals = []
        hospital = db.query(HospitalTable).filter(
            HospitalTable.diary_id == diary_id,
            HospitalTable.deleteTime == None).all()

        if hospital is None:
            return hospitals

        for h in hospital:
            specials = {}
            try:
                if any(special_string in h.special for special_string in [" /seq ", " /split "]):
                    special = h.special.split(" /seq ")
                    for s in special:
                        key, value = s.split(" /split ")
                        specials[key] = value
            except:
                pass

            hospitals.append({
                'hospital_id': h.hospital_id,
                'diary_id': h.diary_id,
                'baby_id': h.baby_id,
                'createTime': h.createTime,
                'modifyTime': h.modifyTime,
                'parent_kg': h.parent_kg,
                'bpressure': h.bpressure,
                'baby_kg': h.baby_kg,
                'baby_cm': h.baby_cm,
                'special': specials,
                'next_day': h.next_day
            })
        return hospitals

    # 하나의 산모수첩 조회

    def getHospital(self, parent_id: str, hospital_id: int) -> Hospital:
        """
        하나의 산모수첩 조회
        - input
            - parent_id (str): 부모 아이디
            - hospital_id (int): 산모수첩 아이디
        - output
            - hospital (Hospital): 산모수첩 딕셔너리
        """

        db = get_db_session()

        diary = db.execute(text(
            f"SELECT * FROM diary \
            WHERE diary_id = (SELECT diary_id FROM hospital WHERE hospital_id = {hospital_id}) \
            AND parent_id = '{parent_id}'")).fetchone()

        if diary is None or diary[7] is not None:
            raise CustomException("Diary does not exist")

        h = db.query(HospitalTable).filter(
            HospitalTable.hospital_id == hospital_id,
            HospitalTable.deleteTime == None).first()

        specials = {}
        if any(special_string in h.special for special_string in [" /seq ", " /split "]):
            special = h.special.split(" /seq ")
            for s in special:
                key, value = s.split(" /split ")
                specials[key] = value

        hospital = {
            'hospital_id': h.hospital_id,
            'diary_id': h.diary_id,
            'baby_id': h.baby_id,
            'createTime': h.createTime,
            'modifyTime': h.modifyTime,
            'parent_kg': h.parent_kg,
            'bpressure': h.bpressure,
            'baby_kg': h.baby_kg,
            'baby_cm': h.baby_cm,
            'special': specials,
            'next_day': h.next_day
        }
        print(hospital)

        if hospital is None:
            raise HTTPException("Hospital does not exist")

        return hospital

    # 산모수첩 수정

    def updateHospital(self, parent_id: str,
                       updateHospitalInput: UpdateHospitalInput) -> Hospital:

        db = get_db_session()

        diary = db.execute(text(
            f"SELECT * FROM diary \
            WHERE diary_id = (SELECT diary_id FROM hospital WHERE hospital_id = {updateHospitalInput.hospital_id}) \
            AND parent_id = '{parent_id}'")).fetchone()

        if diary is None:
            raise CustomException("Diary does not exist")

        hospital = db.query(HospitalTable).filter(
            HospitalTable.hospital_id == updateHospitalInput.hospital_id).first()

        if hospital is None:
            raise CustomException("Hospital does not exist")

        for key in ['parent_kg', 'bpressure', 'baby_kg', 'baby_cm', 'special', 'next_day']:
            hospital.__setattr__(
                key, updateHospitalInput.__getattribute__(key))

        try:
            db.add(hospital)
            db.commit()
            db.refresh(hospital)
        except Exception as e:
            db.rollback()
            raise HTTPException("Failed to update hospital")

        return hospital

    # 산모수첩 삭제

    def deleteHospital(self, parent_id: str, hospital_id: int) -> bool:
        """
        산모수첩 삭제
        - input
            - parent_id (str): 부모 아이디
            - hospital_id (int): 산모수첩 아이디
        - output
            - bool: True
        """

        db = get_db_session()

        diary = db.execute(text(f"SELECT * FROM diary \
            WHERE diary_id = (SELECT diary_id FROM hospital WHERE hospital_id = {hospital_id}) \
            AND parent_id = '{parent_id}'")).fetchone()

        if diary is None:
            raise CustomException("Diary does not exist")

        hospital = db.query(HospitalTable).filter(
            HospitalTable.hospital_id == hospital_id).first()

        if hospital is None:
            raise CustomException("Hospital does not exist")

        hospital.deleteTime = datetime.now()
        try:
            db.add(hospital)
            db.commit()
            db.refresh(hospital)
        except Exception as e:
            db.rollback()
            raise e

        return True
