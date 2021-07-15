from db import Session
from model import Job, Test
from contextlib import contextmanager


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create(obj):
    with get_session() as session:
        session.add(obj)


def create_job(name, status, branch, user, commit,
               start_time, end_time, duration,
               circleci_url):
    job = Job(name=name, status=status, branch=branch,
              user=user, commit=commit, start_time=start_time,
              end_time=end_time, duration=duration, circleci_url=circleci_url)
    create(job)
    return job


def create_test(job_id, name, classname, status, duration):
    test = Test(job_id=job_id, name=name, classname=classname,
                status=status, duration=duration)
    create(test)
    return test
