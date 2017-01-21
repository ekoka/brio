from sqlalchemy import (Column, Integer, String, Unicode, DateTime, 
                        Date, Time, Numeric, Boolean, ForeignKey)
from sqlalchemy.orm import relationship, backref

from junctures import db 


class Schedule(db.Base):
    __tablename__ = 'schedules'

    tenant_id = Column(Integer, ForeignKey('tenants.tenant_id'), nullable=False)
    schedule_id=Column(Integer, primary_key=True)
    # activities.id & events.id
    item_id=Column(None, ForeignKey('junctures.juncture_id'))
    start_date=Column(Date)
    end_date=Column(Date)
    start_time=Column(Time)
    end_time=Column(Time)
    recurrent=Column(Boolean)
    dow=Column(Integer)

    # relationships
    exceptions=relationship(
        'ScheduleException', primaryjoin='ScheduleException.schedule_id=='
        'Schedule.schedule_id', cascade="save-update, merge, delete", 
        backref='schedule', uselist=False)


class ScheduleException(db.Base):
    __tablename__ = 'schedules_exceptions'

    tenant_id = Column(Integer, ForeignKey('tenants.tenant_id'), nullable=False)
    schedule_exception_id=Column(Integer, primary_key=True)
    schedule_id=Column(None, ForeignKey('schedules.schedule_id'))
    reschedule_id=Column(None, ForeignKey('schedules.schedule_id'))
    type=Column(Unicode) # cancellation, postponement, etc
    date=Column(Date)

    # relationships
    # Schedule exceptions have 2 types of relationships with schedules: they are
    # generated from schedules and can also generate new schedules. One
    # relationship has already been defined in the mapping for Schedule. Another
    # should point specifically from exceptions to schedule for reschedulings.
    # It's defined in the ScheduleException mapping, we'll call the backref 
    # 'root_exception' as a way to mark that it's the exception that is the 
    # originating cause of th re-scheduling.
    reschedule=relationship(
        'Schedule', backref=backref('root_exception', uselist=False), 
        primaryjoin='ScheduleException.reschedule_id=='
        'Schedule.schedule_id', cascade='save-update, merge, delete',
        uselist=False)
