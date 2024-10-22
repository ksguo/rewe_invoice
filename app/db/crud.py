from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
import logging

logger = logging.getLogger(__name__)


def create_record(db: Session, model, **kwargs):
    """
    creates a record in the database with the given model and parameters.
    """
    new_record = model(**kwargs)
    try:
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return new_record
    except Exception as e:
        db.rollback()
        logger.error("Failed to create record: %s", e)
        raise


def read_records(
    db: Session, model, filters=None, order_by=None, limit=None, offset=None
):
    """
    reads records from the database based on filters, order, limit, and offset.
    """
    query = db.query(model)
    if filters:
        for key, value in filters.items():
            condition = getattr(model, key) == value
            query = query.filter(condition)
            logger.debug(f"Filtering on: {condition}")
    if order_by:
        query = query.order_by(order_by)
    if limit is not None:
        query = query.limit(limit)
    if offset is not None:
        query = query.offset(offset)
    logger.info(f"Final query: {query}")
    return query.all()


def update_record(db: Session, model, record_id, **kwargs):
    """
    updates a record identified by record_id with the given keyword arguments.
    """
    primary_key = inspect(model).primary_key[0].name
    try:
        record = (
            db.query(model).filter(getattr(model, primary_key) == record_id).first()
        )
        if record:
            for key, value in kwargs.items():
                setattr(record, key, value)
            db.commit()
            db.refresh(record)
        return record
    except Exception as e:
        db.rollback()
        logger.error("Failed to update record: %s", e)
        raise


def delete_record(db: Session, model, record_id):
    """
    deletes a record identified by record_id from the database.
    """
    primary_key = inspect(model).primary_key[0].name
    try:
        record = (
            db.query(model).filter(getattr(model, primary_key) == record_id).first()
        )
        if record:
            db.delete(record)
            db.commit()
        return record
    except Exception as e:
        db.rollback()
        logger.error("Failed to delete record: %s", e)
        raise
