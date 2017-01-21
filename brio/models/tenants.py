# coding=utf8

from sqlalchemy import (Column, Integer, String, Unicode, DateTime, 
                        Date, Numeric, Boolean, ForeignKey)

from brio.startup import db

class Tenant(db.Base): 

    __tablename__ = 'tenants'

    tenant_id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    organization = (Unicode)
    email = (Unicode)
    telephone = (Unicode)
