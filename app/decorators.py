from functools import wraps

def commit_db(db):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                db.session.commit()
                return result
            except Exception as e:
                db.session.rollback()
                raise e
        return wrapper
    return decorator
