from fastapi import status, UploadFile
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..database import User, Contract
from ..schemas import user
from ..helpers.auth import verify_password, hash_password
from ..helpers.oauth2 import signJWT, decodeJWT
from email.mime.text import MIMEText
import uuid
import logging
import smtplib
from ..helpers.upload import upload_file


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def send_verification_email(self, email: str, verification_code: str):
        # Cấu hình máy chủ SMTP và gửi email
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "huyhg2521@gmail.com"
        sender_password = "huy20052001"

        msg = MIMEText(
            f"Click this link to verify your email: http://example.com/verify/{verification_code}"
        )
        msg["Subject"] = "Email Verification"
        msg["From"] = sender_email
        msg["To"] = email

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                await server.sendmail(sender_email, [email], msg.as_string())
        except Exception as e:
            print(f"Error sending email: {str(e)}")

    def get_user_in_access_token(self, access_token: str):
        token = decodeJWT(access_token)

        if "user_id" not in token and not token["user_id"]:
            raise HTTPException(status_code=401, detail="Token Invalid")

        return token["user_id"]

    async def generate_tokens(self, user_id):
        access_token = signJWT(user_id=user_id, expires=1800)
        refresh_token = signJWT(user_id=user_id, expires=172800)
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def get_user_by_email(self, email: str) -> user.UserSchema:
        found_user = self.db.query(User).filter(User.email == email).first()
        return found_user

    async def get_user_by_id(self, user_id: str) -> user.UserSchema:
        found_user = self.db.query(User).filter(User.id == user_id).first()
        return found_user

    async def user_login(self, user_obj: user.UserLoginSchema):
        found_user = await self.get_user_by_email(email=user_obj.email)

        if found_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(user_obj.password, found_user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return await self.generate_tokens(found_user.id)

    async def user_sign_up(self, user_obj: user.UserCreateSchema):
        found_user = await self.get_user_by_email(email=user_obj.email)

        if found_user:
            raise HTTPException(status_code=400, detail="Email is exist!!")

        self.db.add(
            User(
                id=uuid.uuid4(),
                username=user_obj.username,
                phonenumber=user_obj.phonenumber,
                email=user_obj.email,
                password=hash_password(user_obj.password),
                system_role=user_obj.system_role,
            )
        )

        self.db.commit()

        # characters = string.ascii_letters + string.digits
        # verify_code = "".join(secrets.choice(characters) for _ in range(8))
        # await self.send_verification_email(
        #     email=user_obj.email, verification_code=verify_code
        # )

        return {}

    async def user_refresh_token(self, access_token: str):
        user_id = self.get_user_in_access_token(access_token)
        return await self.generate_tokens(user_id)

    async def get(self, access_token: str, username: str | None):
        if username:
            found_user = self.db.query(User).filter(User.username == username).first()
        else:
            user_id = self.get_user_in_access_token(access_token)
            found_user = self.db.query(User).filter(User.id == user_id).first()

        return found_user

    async def gets(self):
        found_users = self.db.query(User).all()
        return found_users

    async def update_avatar(self, avatar: UploadFile, user_id: str):
        found_user = await self.get_user_by_id(user_id)

        if not found_user:
            raise HTTPException(status_code=404, detail="User not found")

        upload_file(
            folder_name=f"data/avatar/users",
            allowed_image_types=["image/png", "image/jpeg", "image/jpg"],
            endpoint_path=user_id,
            file_upload=avatar,
        )

        found_user.avatar = f"users/{user_id}/avatar"
        self.db.commit()

        return found_user

    async def update_user(self, user_id: str, user_update: user.UserUpdateSchema):
        found_user = await self.get_user_by_id(user_id)

        if not found_user:
            raise HTTPException(status_code=404, detail="User not found")

        user_update_record = user_update.model_dump(exclude_unset=True)

        for key, value in user_update_record.items():
            setattr(found_user, key, value)

        self.db.commit()
        self.db.refresh(found_user)
        return found_user

    async def delete_user(self, email: str, user_id: str):
        found_user_query = await self.get_user_by_email(email)

        self.db.query(Contract).filter(Contract.user_id == user_id).delete()

        if not found_user_query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Email not found!!"
            )

        self.db.delete(found_user_query)
        self.db.commit()
        return {"message": f"Xoá gmail : {email} thành công."}
