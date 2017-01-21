# coding=utf-8

from sqlalchemy import (Table, Column, Integer, String, Unicode, DateTime, 
                        Date, Numeric, Boolean, ForeignKey, ForeignKeyConstraint)
from sqlalchemy.orm import mapper, relationship, backref

from .junctures import Juncture
 
class Activity(Juncture):

    __tablename__ = 'activities'

    activity_id = Column(Integer, ForeignKey('junctures.juncture_id'), 
           primary_key=True)
    manager=Column(Unicode)
    created_by=Column(Unicode)
    created_on=Column(DateTime)
    updated_on=Column(DateTime)
    title=Column(Unicode)
    description=Column(Unicode)
    excerpt=Column(Unicode)
    start_date=Column(Date)
    end_date=Column(Date)
    capacity=Column(Integer) # 0 for unlimited
    price=Column(Numeric(precision=10, scale=2, asdecimal=True))
    location=Column(Unicode)
    equipment=Column(Unicode)
    audience=Column(Unicode) # preschool, sixth grade, etc
    etag=Column(Unicode)
    external_registration=Column(Boolean) # external registration possible
    external_registration_link=Column(Unicode)
    open_for_registration=Column(Boolean)
    status=Column(Unicode) # draft, published, archived

    # relationships
    """ 
    There's no direct relationships between activities and schedule exceptions,
    but it would still be nice to have a broad view of an activity's schedule
    exception. For this, we can direct the mapper to load exceptions through the
    intermediary schedules table and use 'viewonly=True' to tell it that the 
    relationship is for convenience. Without 'viewonly', it might try to unset
    some keys on insert or delete.

    see http://docs.sqlalchemy.org/en/latest/orm/relationships.html
    """
    schedules=relationship(
        'Schedule', backref='activity', cascade="save-update, merge, delete")
    schedule_exceptions=relationship(
        'ScheduleException', secondary='schedules',
        primaryjoin='Activity.activity_id==Schedule.item_id',
        secondaryjoin='Schedule.schedule_id==ScheduleException.schedule_id',
        # since there are no foreign keys explicitly declared between
        # activities and schedules, I need to be specific about this 
        # relationship.
        foreign_keys='[Schedule.item_id, ScheduleException.schedule_id]',
        viewonly=True)

    __mapper_args__ = {'polymorphic_identity':'activities'}

    #images = relationship('Image')
