from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from as_fast.database.db import get_db
from as_fast.repository import contact as repository_contacts
from as_fast.schemas.contact import ContactSchema, ContactSchemaResponse

router = APIRouter(prefix='/users', tags=['users'])


@router.get("/", response_model=list[ContactSchemaResponse])
async def get_users(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                    db: AsyncSession = Depends(get_db)):
    users = await repository_contacts.get_users(limit, offset, db)
    return users


@router.get("/birth_date", response_model=list[ContactSchemaResponse])
async def get_users_birth(limit: int = Query(7, ge=7, le=100),
                          db: AsyncSession = Depends(get_db)):
    users = await repository_contacts.get_users_birth(limit, db)
    return users


@router.get("/search_by", response_model=list[ContactSchemaResponse])
async def get_users_by(first_name: str = Query(None, min_length=3, description="Frist name search query"),
                       second_name: str = Query(None, min_length=3, description="Second name search query"),
                       email_add: str = Query(None, min_length=3, description="Email search query"),
                       db: AsyncSession = Depends(get_db)):
    users = await repository_contacts.get_users_by(first_name, second_name, email_add, db)
    return users


@router.get("/{user_id}", response_model=ContactSchemaResponse)
async def get_user(user_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    user = await repository_contacts.get_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return user


@router.post("/", response_model=ContactSchemaResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: ContactSchema, db: AsyncSession = Depends(get_db)):
    user = await repository_contacts.create_user(body, db)
    return user


@router.put("/{user_id}")
async def update_user(body: ContactSchema, user_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    user = await repository_contacts.update_user(user_id, body, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    user = await repository_contacts.delete_user(user_id, db)
    return user
