import os
import uuid

from constant import TEMP_FILE_FOLDER
from models import complaint
from models.enums import RoleType, State
from db import database
from services.s3 import S3Service
from services.ses import SESService
from utils.helpers import decode_photo



s3 = S3Service()
ses = SESService()


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        q = complaint.select()
        if user["role"] == RoleType.complainer:
            q = q.where(complaint.c.complainer_id == user["id"])
        elif user["role"] == RoleType.approver:
            q = q.where(complaint.c.status == State.pending)
        return await database.fetch_all(q)
    
    @staticmethod
    async def create_complaint(complaint_data, user):
        complaint_data["complainer_id"] = user["id"]
        encoded_photo = complaint_data.pop("encoded_photo")
        extension = complaint_data.pop("extension")
        name = f"{uuid.uuid4()}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, name)
        decode_photo(path, encoded_photo)
        complaint_data["photo_url"] = s3.upload(path, name, extension)
        os.remove(path)
        id_ = await database.execute(complaint.insert().values(complaint_data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))
    
    @staticmethod
    async def delete(complaint_id):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))


    @staticmethod
    async def approve(id_):
        await database.execute(complaint.update().where(complaint.c.id == id_).values(status=State.approved))
        ses.send_mail("Complaint Approved!", ["robertarthur318@gmail.com"], 
                      "Congrats your claim is approved, check your bank account for your refund")


    @staticmethod
    async def reject(id_):
        await database.execute(complaint.update().where(complaint.c.id == id_).values(status=State.rejected))
        

    
    
    
