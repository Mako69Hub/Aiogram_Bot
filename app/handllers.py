from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb #импорт и дать короткое название
import app.database.requests as rq
router = Router()


class Register(StatesGroup):
    name = State()
    age = State()
    number = State()
#медал вари постоянно проверять в бд, если пользователь заблокирован

@router.message(CommandStart(), )
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Привет!', reply_markup= kb.main) #открыть клавиатуру мейн, когда буду отправлять соо
    await message.reply('Как дела?')



@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Вы нажали на кнопку помощи')


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=kb.catalog)


@router.callback_query(F.data == 't-shirt')
async def t_shirt(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию', show_alert=True) # чтобы не подсвечивалось, show _навязчивое напоминание
    await callback.message.answer('Вы выбрали категорию футболок')

@router.message(Command('register')) # использовать состояния, присвоить состояние нужно их в отдельный файл
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введите ваше имя')

@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer('Введите ваш возраст')

@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.number)
    await message.answer('Отправьте ваш номер телефона', reply_markup=kb.get_number)

@router.message(Register.number, F.contact)
async def register_number(message:Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f'Ваше имя: {data["name"]}\nВаш возраст: {data["age"]}\nНомер: {data["number"]}')
    await state.clear()