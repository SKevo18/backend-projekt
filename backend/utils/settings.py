from db import DB
from db.orm import Setting as SettingModel


def get_setting(key: str, default: str = "") -> str:
    try:
        with DB.get_session() as session:
            setting = session.query(SettingModel).filter_by(key=key).first()
            return setting.value if setting else default
    except Exception:
        return default
