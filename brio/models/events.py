# coding=utf-8

from sqlalchemy import (Table, Column, Integer, String, Unicode, DateTime, 
                        Date, Numeric, Boolean, ForeignKey)
from sqlalchemy.orm import relationship, backref

from .junctures import Juncture

class Event(Juncture):
    __tablename__ = 'events'

    event_id=Column(Integer, ForeignKey('junctures.juncture_id'), 
                    primary_key=True)
    title=Column(Unicode)
    description=Column(Unicode)
    excerpt=Column(Unicode)
    start_date=Column(Date)
    end_date=Column(Date)
    capacity=Column(Integer) # 0 for unlimited
    price=Column(Numeric(precision=10, scale=2, asdecimal=True))
    manager=Column(Unicode)
    location=Column(Unicode)
    equipment=Column(Unicode)
    external_registration=Column(Boolean)
    external_registration_link=Column(Unicode)
    audience=Column(Unicode)
    open_for_registration=Column(Boolean)
    status=Column(Unicode)
    created_by=Column(Unicode)
    created_on=Column(DateTime)
    updated_on=Column(DateTime)
    etag=Column(Unicode)

    __mapper_args__ = {'polymorphic_identity':'events'}

    """ 
    There's no direct relationships between events and schedule exceptions,
    but it would still be nice to have a broad view of an event's schedule
    exception. For this, we can direct the mapper to load exceptions through the
    intermediary schedules table and use 'viewonly=True' to tell it that the 
    relationship is for convenience. Without 'viewonly', it might try to unset
    some keys on insert or delete.

    see http://docs.sqlalchemy.org/en/latest/orm/relationships.html
    """

    # relationships
    schedules=relationship(
        'Schedule', backref='event', cascade="save-update, merge, delete")
    schedule_exceptions=relationship( 
        'ScheduleException', secondary='schedules', 
        primaryjoin='Event.event_id==Schedule.item_id',
        # since there are no foreign keys explicitly declared between
        # events and schedules, I need to be specific about this 
        # relationship.
        #foreign_keys=['Schedule.item_id', 'ScheduleException.schedule_id'],
        foreign_keys='[Schedule.item_id, ScheduleException.schedule_id]',
        secondaryjoin='Schedule.schedule_id==ScheduleException.schedule_id',
        viewonly=True)
