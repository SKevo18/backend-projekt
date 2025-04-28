from db import get_db
from db.orm import Setting as SettingModel
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session
from utils.settings import get_setting

from controllers.dependencies import get_admin_user


class Setting(BaseModel):
    key: str
    value: str

    class Config:
        from_attributes = True


class SaveSettingsRequest(BaseModel):
    smtp_host: str
    smtp_port: int
    email_sender: str
    email_password: str
    turnstile_site_key: str = ""
    turnstile_secret_key: str = ""


SETTINGS_CONTROLLER = APIRouter(prefix="/settings")


@SETTINGS_CONTROLLER.get("")
def get_settings(_=Depends(get_admin_user)):
    return {
        "smtp_host": get_setting("smtp_host"),
        "smtp_port": get_setting("smtp_port"),
        "email_sender": get_setting("email_sender"),
        "email_password": get_setting("email_password"),
        "turnstile_site_key": get_setting("turnstile_site_key"),
        "turnstile_secret_key": get_setting("turnstile_secret_key"),
    }


@SETTINGS_CONTROLLER.get("/turnstile-key")
def get_turnstile_key():
    return {"turnstile_site_key": get_setting("turnstile_site_key")}


@SETTINGS_CONTROLLER.post("/save")
def save_settings(
    req: SaveSettingsRequest, db: Session = Depends(get_db), _=Depends(get_admin_user)
):
    data = req.model_dump()

    insert_values = [{"key": k, "value": str(v)} for k, v in data.items()]
    stmt = insert(SettingModel).values(insert_values)
    update_stmt = stmt.on_duplicate_key_update(value=stmt.inserted.value)

    db.execute(update_stmt)
    db.commit()

    return {"message": "Settings saved successfully"}
