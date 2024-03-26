from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from as_fast.database.models import Contact
from as_fast.schemas.contact import ContactSchema

from datetime import datetime, timedelta


async def get_users(limit: int, offset: int, db: AsyncSession):
    search = select(Contact).offset(offset).limit(limit)
    users = await db.execute(search)
    return users.scalars().all()


async def get_users_by(first_name: str = None, second_name: str = None, email_add: str = None, db: AsyncSession = None):
    search = select(Contact)
    if first_name and second_name and email_add:
        search = search.where(
            or_(Contact.first_name == first_name, Contact.second_name == second_name, Contact.email_add == email_add))

    elif first_name and second_name:
        search = search.where(
            or_(Contact.first_name == first_name, Contact.second_name == second_name, Contact.email_add == email_add))

    elif first_name and email_add:
        search = search.where(or_(Contact.first_name == first_name, Contact.email_add == email_add))

    elif second_name and email_add:
        search = search.where(or_(Contact.second_name == second_name, Contact.email_add == email_add))

    elif first_name:
        search = search.where(Contact.first_name == first_name)

    elif second_name:
        search = search.where(Contact.second_name == second_name)

    elif email_add:
        search = search.where(Contact.email_add == email_add)

    else:
        return []

    users = await db.execute(search)
    print(type(users.scalars().all()))
    return users.scalars().all()


async def get_user(user_id: int, db: AsyncSession):
    search = select(Contact).filter_by(id=user_id)
    user = await db.execute(search)
    return user.scalar_one_or_none()


async def get_users_birth(limit: int, db: AsyncSession):
    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=limit)

    search = select(Contact).filter(Contact.birth_date >= current_date, Contact.birth_date <= end_date)
    result = await db.execute(search)

    return result.scalars().all()


async def create_user(body: ContactSchema, db: AsyncSession):
    user = Contact(**body.model_dump(exclude_unset=True))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(user_id: int, body: ContactSchema, db: AsyncSession):
    search = select(Contact).filter_by(id=user_id)
    result = await db.execute(search)
    user = result.scalar_one_or_none()
    if user:
        user.first_name = body.first_name
        user.second_name = body.second_name
        user.email_add = body.email_add
        user.phone_num = body.phone_num
        user.birth_date = body.birth_date
        await db.commit()
        await db.refresh(user)
    return user


async def delete_user(user_id: int, db: AsyncSession):
    search = select(Contact).filter_by(id=user_id)
    user = await db.execute(search)
    user = user.scalar_one_or_none()
    if user:
        await db.delete(user)
        await db.commit()
    return user
