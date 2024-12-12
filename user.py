from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from models import User as UserModel  # Импортируем модель SQLAlchemy
from schemas import User, CreateUser, UpdateUser  # Импортируйте вашу Pydantic модель ответа
from sqlalchemy import insert, select, update, delete
from slugify import slugify
from typing import Annotated, List

router = APIRouter()


@router.get("/", response_model=List[User])  # Используйте Pydantic модель для ответа
async def all_users(db: Annotated[Session, Depends(get_db)]):
	users = db.execute(select(UserModel)).scalars().all()
	return users  # Теперь вернётся список Pydantic моделей


@router.get("/{user_id}", response_model=User)
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
	user = db.execute(select(UserModel).where(UserModel.id == user_id)).scalar_one_or_none()
	if user is None:
		raise HTTPException(status_code=404, detail="User was not found")
	return user  # Возвращаем Pydantic модель


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
	existing_user = db.execute(select(UserModel).where(UserModel.username == user.username)).scalar_one_or_none()
	if existing_user:
		raise HTTPException(status_code=400, detail="User already exists")

	new_user = UserModel(username=slugify(user.username), firstname=user.firstname, lastname=user.lastname,
	                     age=user.age)

	db.execute(insert(UserModel).values(new_user))
	db.commit()

	return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user_data: UpdateUser, db: Annotated[Session, Depends(get_db)]):
	user = db.execute(select(UserModel).where(UserModel.id == user_id)).scalar_one_or_none()
	if user is None:
		raise HTTPException(status_code=404, detail="User was not found")

	db.execute(update(UserModel).where(UserModel.id == user_id).values(
		firstname=user_data.firstname,
		lastname=user_data.lastname,
		age=user_data.age
	))
	db.commit()

	return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
	user = db.execute(select(UserModel).where(UserModel.id == user_id)).scalar_one_or_none()
	if user is None:
		raise HTTPException(status_code=404, detail="User was not found")

	db.execute(delete(UserModel).where(UserModel.id == user_id))
	db.commit()