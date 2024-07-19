def session_decorator(session, auto_close_session=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                session.commit()

                return result

            except Exception as e:
                session.rollback()
                raise e
            finally:
                if auto_close_session:
                    session.close()

        return wrapper
    return decorator

