import asyncio

from sqlalchemy import insert, select, update, delete

from models import User, Order
from database import async_session_maker

# ---------- USERS -------------


async def create_user(
        name: str,
        login: str,
        password: str,
        age: int,
        nickname: str = None,
        notes: str = None,
) -> tuple:
    # await asyncio.sleep(2)
    # print(9999999999)
    async with async_session_maker() as session:
        query = insert(User).values(
            name=name,
            login=login,
            password=password,
            age=age,
            nickname=nickname,
            notes=notes,
        ).returning(User.id, User.created_at, User.login)
        print(query)
        data = await session.execute(query)
        await session.commit()
        print(tuple(data))
        return tuple(data)


async def fetch_users(skip: int = 0, limit: int = 10) -> list[User]:
    async with async_session_maker() as session:
        query = select(User).offset(skip).limit(limit)
        result = await session.execute(query)
        print(query)
        # print(type(result.scalars().all()))
        print(result.scalars().all()[0].login)
        # print(result.scalars().all()[0].__dict__)
        return result.scalars().all()


async def get_user_by_id(user_id: int) -> User | None:
    async with async_session_maker() as session:
        query = select(User).filter_by(id=user_id)
        result = await session.execute(query)
        # print(result.scalar_one_or_none())
        return result.scalar_one_or_none()


async def update_user(user_id: int, values: dict):
    if not values:
        return
    async with async_session_maker() as session:
        query = update(User).where(User.id == user_id).values(**values)
        result = await session.execute(query)
        await session.commit()
        # print(tuple(result))
        print(query)


async def delete_user(user_id: int):
    async with async_session_maker() as session:
        query = delete(User).where(User.id == user_id)
        await session.execute(query)
        await session.commit()
        print(query)


# ---------- ORDERS -------------


async def create_order(
    quantity: int,
    price: float,
    customer: int,
) -> tuple:
    if await get_user_by_id(user_id=customer) is not None:
        async with async_session_maker() as session:
            query = insert(Order).values(
                quantity=quantity,
                price=price,
                customer=customer,
            ).returning(Order.id, Order.created_at)
            print(query)
            data = await session.execute(query)
            await session.commit()
            print(tuple(data))
            return tuple(data)
    else:
        return ()


async def fetch_orders(skip: int = 0, limit: int = 10) -> list[Order]:
    async with async_session_maker() as session:
        query = select(Order).offset(skip).limit(limit)
        result = await session.execute(query)
        # print(query)
        # print(type(result.scalars().all()))
        # print(result.scalars().all()[0].login)
        print(result.scalars().all()[0].__dict__)
        return result.scalars().all()


async def get_order_by_id(order_id: int) -> User | None:
    async with async_session_maker() as session:
        query = select(Order).filter_by(id=order_id)
        result = await session.execute(query)
        print(result.scalar_one_or_none().__dict__)
        return result.scalar_one_or_none()


async def update_order(order_id: int, values: dict):
    if not values:
        return
    async with async_session_maker() as session:
        query = update(Order).where(Order.id == order_id).values(**values)
        result = await session.execute(query)
        await session.commit()
        print(query)


async def delete_order(order_id: int):
    async with async_session_maker() as session:
        query = delete(Order).where(Order.id == order_id)
        await session.execute(query)
        await session.commit()
        print(query)


# ---------- MAIN -------------


async def main():
    await asyncio.gather(
        # create_user(
        #     name='Timur',
        #     login='login222667',
        #     password='1234',
        #     age=25,
        #     nickname='nickname',
        # ),
        # fetch_users(skip=1)
        # get_user_by_id(1),
        # update_user(1, {'name': 'Alex', 'age': 65})
        # delete_user(1)
        # create_order(
        #  quantity=2,
        #  price=3.56,
        #  customer=1,
        # )
        # fetch_orders()
        # get_order_by_id(4)
        # update_order(4, {'quantity': 7, 'price': 65})
        delete_order(4)
    )


asyncio.run(main())
