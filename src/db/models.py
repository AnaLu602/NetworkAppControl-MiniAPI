from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from .database import Base


class StreamConfig(Base):
    __tablename__ = "streamconfig"

    id = Column(Integer, primary_key=True, index=True)
    numberofStreams = Column(Integer)
    tputTotalDown = Column(Integer)
    tputTotalUp = Column(Integer)
