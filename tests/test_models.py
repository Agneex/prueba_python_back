from sqlalchemy import select

from app.db.models import ImplicitFunction, User


async def test_function_belongs_to_owner(db_session):
    user = User(username="ana", email="ana@example.com", hashed_password="x")
    db_session.add(user)
    await db_session.flush()

    function = ImplicitFunction(
        owner_id=user.id,
        name="Esfera",
        expression="x**2 + y**2 + z**2 - 1",
        domain=[[-1.5, 1.5], [-1.5, 1.5], [-1.5, 1.5]],
    )
    db_session.add(function)
    await db_session.commit()

    stored = await db_session.scalar(select(ImplicitFunction).where(ImplicitFunction.owner_id == user.id))

    assert stored is not None
    assert stored.resolution == 64
    assert stored.version == 1
    assert stored.domain[0] == [-1.5, 1.5]
