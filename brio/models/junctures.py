# coding=utf8

from sqlalchemy import Column, Integer, Unicode, ForeignKey

from brio.startup import db

class Juncture(db.Base):

    __tablename__ = 'junctures'

    tenant_id = Column(Integer, ForeignKey('tenants.tenant_id'), nullable=False)
    juncture_id = Column(Integer, primary_key=True)
    juncture_type = Column(Unicode)

    __mapper_args__ = {'polymorphic_on':'juncture_type'}
