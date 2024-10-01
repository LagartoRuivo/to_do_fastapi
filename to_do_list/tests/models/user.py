from sqlalchemy import select

from to_do_list.db.models import User


def test_create_user(session):
    user = User(
        username='Zecatatu',
        email='zequinha123@gmail.com',
        password='xesque',
    )
    session.add(user)
    session.commit()

    user_on_db = session.scalar(
        select(User).where(User.email == 'zequinha123@gmail.com')
    )

    assert user == user_on_db
