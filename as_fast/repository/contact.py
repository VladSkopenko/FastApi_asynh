from sqlalchemy import select, or_, and_, extract
from sqlalchemy.ext.asyncio import AsyncSession

from as_fast.database.models import Contact
from as_fast.schemas.contact import ContactSchema

from datetime import datetime, timedelta


async def get_contacts(limit: int, offset: int, db: AsyncSession):
    search = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(search)
    return contacts.scalars().all()


async def get_contacts_by(first_name: str = None, second_name: str = None, email_add: str = None, db: AsyncSession = None):
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

    contact = await db.execute(search)
    print(type(contact.scalars().all()))
    return contact.scalars().all()


async def get_contact(user_id: int, db: AsyncSession):
    search = select(Contact).filter_by(id=user_id)
    contact = await db.execute(search)
    return contact.scalar_one_or_none()


# async def get_contacts_birth(limit: int, db: AsyncSession):
#     current_date = datetime.now().date()
#     end_date = current_date + timedelta(days=limit)
#
#     search = select(Contact).filter(Contact.birth_date >= current_date, Contact.birth_date <= end_date)
#     result = await db.execute(search)
#
#     return result.scalars().all()
async def get_contacts_birth(limit: int, db: AsyncSession):
    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=limit)

    search = select(Contact).filter(
        or_(
            and_(
                extract('month', Contact.birth_date) == current_date.month,
                extract('day', Contact.birth_date) >= current_date.day
            ),
            and_(
                extract('month', Contact.birth_date) == end_date.month,
                extract('day', Contact.birth_date) <= end_date.day
            ),
            and_(
                extract('month', Contact.birth_date) == (current_date.month + 1) % 12,
                extract('day', Contact.birth_date) <= end_date.day
            )
        )
    )

    result = await db.execute(search)
    return result.scalars().all()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactSchema, db: AsyncSession):
    search = select(Contact).filter_by(id=contact_id)
    result = await db.execute(search)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.second_name = body.second_name
        contact.email_add = body.email_add
        contact.phone_num = body.phone_num
        contact.birth_date = body.birth_date
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    search = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(search)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact
