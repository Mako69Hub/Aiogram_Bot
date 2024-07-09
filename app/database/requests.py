# записывать, удалять запросы в бд

from app.database.models import async_session
from app.database.models import User, Category, Item
from sqlalchemy import select, update, delete  # add через селит делается desc - перевернуть, сортировка иначе делается, потом


async def set_user(tg_id: int) -> None:  # добавить нвого пользователя
    async with async_session() as session:  # контексный менеджер, открывает и закрывает функцию asyns with
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        # скаляр лучше, чем через экзекют (не всегда понятно, что вернёт, объект, словарь, список), получаем скалярный результат, полноценный объект, который имеет свои поля, скаляр.s возвращает объект, который можно инттерировать
        if not user:
            session.add(User(
                tg_id=tg_id))  # если возварашает ничего, то не эвейтебл, в скл не может записывать данные асинхронно
            await session.commit()  # если возврашает короутину, то эвейт


async def get_categories():
    async with async_session() as session:
        return await session.scalar(select(Category))
