from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from . import models
from .. import schemas


def get_stream_config(db: Session, stream_config_id: int):
    return db.query(models.StreamConfig).filter(models.StreamConfig.id == stream_config_id).first()

def get_stream_configs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.StreamConfig).offset(skip).limit(limit).all()


def create_stream_config(db: Session, stream_config: schemas.StreamConfig):
    db_stream_config = models.StreamConfig(numberofStreams = stream_config["numberofStreams"], tputTotalDown = stream_config["tputTotalDown"], tputTotalUp = stream_config["tputTotalUp"])
    db.add(db_stream_config)
    db.commit()
    db.refresh(db_stream_config)
    return db_stream_config
