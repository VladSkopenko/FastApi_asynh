from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from as_fast.database.db import get_db
from as_fast.repository import contact as repository_contacts
from as_fast.schemas.contact import ContactSchema, ContactResponse

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/", response_model=list[ContactResponse])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get("/birth_date", response_model=list[ContactResponse])
async def get_contacts_birth(limit: int = Query(7, ge=7, le=100),
                             db: AsyncSession = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_birth(limit, db)
    return contacts


@router.get("/search_by", response_model=list[ContactResponse])
async def get_contacts_by(first_name: str = Query(None, min_length=3, description="Frist name search query"),
                          second_name: str = Query(None, min_length=3, description="Second name search query"),
                          email_add: str = Query(None, min_length=3, description="Email search query"),
                          db: AsyncSession = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_by(first_name, second_name, email_add, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.create_contact(body, db)
    return contact


@router.put("/{contact_id}")
async def update_contact(body: ContactSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.delete("/{contact_id}")
async def delete_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.delete_contact(contact_id, db)
    return contact
