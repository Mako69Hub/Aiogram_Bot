# Модели бд
from sqlalchemy import BigInteger, String, ForeignKey  # потому что количество пользователей большое, потому большое инт
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')  # создать бд

async_session = async_sessionmaker(engine)  # подключение к бд



class Base(AsyncAttrs, DeclarativeBase):  # цправлять всеми таблицами
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)  # autoincrement=True сам понимает
    tg_id = mapped_column(BigInteger)


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))  # принимает 25 символов


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(25))  # ограничение стр, если использовать майэскл не прокатит, если sql то прокатит
    description: Mapped[str] = mapped_column(String(120))  # слишком большое значение может тоже не прокатить
    price: Mapped[
        int] = mapped_column()  # если дробное, то лучше в стринге хранить, а не флоат, ибо не такое точное значение
    category: Mapped[int] = mapped_column(ForeignKey(
        'categories.id'))  # к foreinkey можно прописать, что случиться, если удалить категорию, удалять айтем (каскад, рестрик, дунафинг(защитить или удалить товар, либо ничего не делать))


# релейшен шип связь таблиц в склалхимик


async def async_main():  # создаёт все таблицы, если их не сущ.
    async with engine.begin() as conn:  # контекстный менеджер engine начать сессию и создать новую переменную
        await conn.run_sync(
            Base.metadata.create_all)  # запустить синхронизацию, передадим бэйс и в методате хранятся классыЮ мы их создаём
