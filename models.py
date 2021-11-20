from sqlalchemy import Boolean, Column, ForeignKey, Integer, BigInteger, String, Float, JSON, text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db import Base, engine
import psycopg2.extras


psycopg2.extras.register_uuid()


class Vessels(Base):
    __tablename__ = "vessels"
    vessel_mmsi = Column(String, primary_key=True,unique=True, index=True)
    #well_id = Column(BigInteger, Sequence('wells_well_id_seq', minvalue=-9223372036854775808, start=-9223372036854775808, increment=1), primary_key=True, autoincrement=True, unique=True, index=True)
    ETA = Column(String, index=True, nullable=True)
    course = Column(String, index=True, nullable=True)
    speed = Column(String, index=True, nullable=True)
    #navtatus = Column(String, index=True, nullable=True)
    pos_received = Column(String, index=True, nullable=True)


