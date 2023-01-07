#import datetime
import sqlite3
import sys
import pathlib
import datetime
import logging
import asyncio
import time

import telebot.types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage




from aiogram import Bot, Dispatcher, executor, types
script_path = pathlib.Path(sys.argv[0]).parent



conn = sqlite3.connect('test_db.db', check_same_thread=True)
cursor = conn.cursor()
print("Подключено")

TOKEN = "5689103411:AAFNxmYASblnCK76THumwm_UIz3FJ6ixXoM"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
#db = Database('table_db.db')


def table_to(nik: str, user_name: str, user_age: int, number: int, city: str, category: str, pod_category: str, description: str, link: str) -> None:
    sqlite_insert_query = """INSERT INTO HomeWork (nik, user_name, user_age, number, city, category, pod_category, description, link) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    data_us = (nik, user_name, user_age, number, city, category, pod_category, description, link)
    cursor.execute(sqlite_insert_query, data_us)

def table_to_vak(cat: str, spec: str,  gorod: str, z_p: int, opis: str, number2: int) ->None:
    sqlite_to_vak = """INSERT INTO Vakans (cat, spec, gorod, z_p, opis, number2) VALUES (?, ?, ?, ?, ?, ?)"""
    data_to = (cat, spec, gorod, z_p, opis, number2)
    cursor.execute(sqlite_to_vak, data_to)



class UserState(StatesGroup):
    us_name = State()
    user_age = State()
    number = State()
    category = State()
    pod_category = State()
    description = State()
    link = State()
    zakaz = State()
    rem = State()
    dom = State()
    gorod = State()
    number2 = State()
    opis = State()
    z_p = State()
    cat = State()
    spec = State()
    us_city = State()
    cat_searsh = State()
    gorod_searsh =State()
    filtr = State()
    filtr_gorod = State()




@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    button_isp = KeyboardButton("Оставить резюме")
    button_zakas = KeyboardButton("Поиск резюме")
    button_vak = KeyboardButton("Оставить вакансию")
    button_searsh = KeyboardButton("Поиск вакансии")

    greet_kb = ReplyKeyboardMarkup(row_width=1)
    greet_kb.add(button_isp, button_zakas, button_vak, button_searsh)

    nik = message.from_user.first_name
    user_id = message.from_user.id


    await message.answer("Привет, " + nik, reply_markup=greet_kb)
    await message.answer("Выберите действие")

@dp.message_handler(text=['Меню'])
async def back_handler(message):
    button_isp = KeyboardButton("Оставить резюме")
    button_zakas = KeyboardButton("Поиск резюме")
    button_vak = KeyboardButton("Оставить вакансию")
    button_searsh = KeyboardButton("Поиск вакансии")


    greet_kb = ReplyKeyboardMarkup(row_width=1)
    greet_kb.add(button_isp, button_zakas, button_vak, button_searsh)
    await message.answer("Выберите действие", reply_markup=greet_kb)

@dp.message_handler(text=['Поиск вакансии'])
async def get_searsh(message: types.Message):
    button_rem = KeyboardButton("Ремонт")
    button_dety = KeyboardButton("Интернет")
    button_helth = KeyboardButton("Здоровье")
    button_hw = KeyboardButton("Домашние дела")
    button_brain = KeyboardButton("Образование")
    button_beauty = KeyboardButton("Красота")
    button_m = KeyboardButton("Меню")
    greet_kb_zak_one = ReplyKeyboardMarkup()
    greet_kb_zak_one.add(button_rem, button_dety, button_helth, button_hw, button_brain, button_beauty, button_m)
    await message.answer("Выберите категорию", reply_markup=greet_kb_zak_one)
    await UserState.cat_searsh.set()
@dp.message_handler(state=UserState.cat_searsh, text=["Ремонт", 'Интернет', 'Здоровье', 'Домашние дела', 'Образование', 'Красота', "Меню"])
async def get_cat_searsh(message: types.Message, state: FSMContext):
    if message.text == "Меню":
        await state.finish()
        await back_handler(message)
    else:
        await state.update_data(cat_searsh=message.text)

        button_filtr = KeyboardButton("Фильтр")
        button_searsh = KeyboardButton("Поиск")
        button_back = KeyboardButton("Назад")
        button_m = KeyboardButton("Меню")
        greet_kb_searsh = ReplyKeyboardMarkup(row_width=1)
        greet_kb_searsh.add(button_filtr, button_back, button_searsh, button_m)
        await message.answer("Нажмите ПОИСК, чтобы найти все вакансии в данной категории\nНажмите ФИЛЬТР, чтобы выполнить поиск по фильтру", reply_markup=greet_kb_searsh)
        await UserState.filtr.set()
@dp.message_handler(state=UserState.filtr, text=['Фильтр', 'Поиск', 'Назад', 'Меню'])
async def get_filter_searsh(message: types.Message, state: FSMContext):

    if message.text == "Меню":
        await state.finish()
        await back_handler(message)

    if message.text == 'Назад':
        await get_searsh(message)
    if message.text == 'Поиск':
        await state.update_data(filter=message.text)
        data4 = await state.get_data()
        cat_searsh = (data4['cat_searsh'])

        cursor.execute(f"""SELECT * FROM Vakans WHERE cat = '{cat_searsh}'""")
        result = cursor.fetchall()
        for i in result:
                await message.answer("Город: " + str(i[2]) + "\n" "Зарплата: " + str(i[3]) + "\n" "Специальность: " + str(
                        i[1]) + "\n" "Номер телефона: " + str(i[5]) + "\n" "Описание: " + str(i[4]))

    if message.text == 'Фильтр':
        button_filtr_gorod = KeyboardButton("Город")
        button_filtr_z_p = KeyboardButton("Зарплата")
        button_filtr_spec = KeyboardButton("Специальность")
        button_menu = KeyboardButton('Назад')
        greet_kb_searsh_filtr = ReplyKeyboardMarkup(row_width=1)
        greet_kb_searsh_filtr.add(button_filtr_gorod, button_menu)
        await message.answer("Выберите фильтр", reply_markup=greet_kb_searsh_filtr)
        await UserState.filtr_gorod.set()
@dp.message_handler(state=UserState.filtr_gorod, text=['Город', 'Зарплата', 'Специальность', 'Назад'])
async def get_searsh_filtr(message: types.Message, state: FSMContext):
    await state.update_data(filter_gorod=message.text)
    if message.text == 'Назад':
        await get_cat_searsh(message, state)
    if message.text == 'Город':
        a = ReplyKeyboardRemove()

        await message.answer("Введите город для поиска", reply_markup=a)
        await UserState.gorod_searsh.set()
@dp.message_handler(state=UserState.gorod_searsh)
async def get_gorod_searsh(message: types.Message, state: FSMContext):

    await state.update_data(gorod_searsh=message.text)
    data3 = await state.get_data()
    cat_searsh = (data3['cat_searsh'])
    gorod_searsh = (data3['gorod_searsh'])
    await state.finish()


    cursor.execute(f"""SELECT * FROM Vakans WHERE cat = '{cat_searsh}' AND gorod = '{gorod_searsh}'""")
    result = cursor.fetchall()
    for i in result:
        await message.answer("Город: " + str(i[2]) + "\n" "Зарплата: " + str(i[3]) + "\n" "Специальность: " + str(
                        i[1]) + "\n" "Номер телефона: " + str(i[5]) + "\n" "Описание: " + str(i[4]))
    button_menu = KeyboardButton('Меню')
    button_back = KeyboardButton('Назад')
    greet_kb_back = ReplyKeyboardMarkup(row_width=1)
    greet_kb_back.add(button_menu, button_back)
    await message.answer("Попробуйте другой фильтр", reply_markup=greet_kb_back)
    @dp.message_handler(text=['Меню', 'Назад'])
    async def get_menu_searsh(message: types.Message):
        if message.text == 'Назад':
            await get_filter_searsh(message, state)
        if message.text == 'Меню':
            await back_handler(message)









@dp.message_handler(text=['Оставить вакансию'])
async def get_vak(message: types.Message):
    button_rem = KeyboardButton("Ремонт")
    button_dety = KeyboardButton("Дети")
    button_helth = KeyboardButton("Здоровье")
    button_hw = KeyboardButton("Домашние дела")
    button_brain = KeyboardButton("Образование")
    button_beauty = KeyboardButton("Красота")
    button_men = KeyboardButton('Меню')
    greet_kb_one = ReplyKeyboardMarkup(row_width=1)
    greet_kb_one.add(button_rem, button_dety, button_helth, button_hw, button_brain, button_beauty, button_men)
    await message.answer("Выберите категорию", reply_markup=greet_kb_one)
    await UserState.cat.set()
@dp.message_handler(state=UserState.cat, text=["Ремонт", 'Дети', 'Здоровье', 'Домашние дела', 'Образование', 'Красота', 'Меню'])
async def get_cat_vak(message: types.Message, state: FSMContext):

    await state.update_data(cat=message.text)
    a = ReplyKeyboardRemove()

    await message.answer("Укажите специальность", reply_markup=a)
    await UserState.spec.set()
@dp.message_handler(state=UserState.spec)
async def get_spec(message: types.Message, state: FSMContext):
    await state.update_data(spec=message.text)
    await message.answer("Введите город")
    await UserState.gorod.set()
@dp.message_handler(state=UserState.gorod)
async def get_gorod(message: types.Message, state: FSMContext):
    await state.update_data(gorod=message.text)
    await message.answer("Укажите з/п")
    await UserState.z_p.set()
@dp.message_handler(state=UserState.z_p)
async def get_z_p(message: types.Message, state: FSMContext):
    await state.update_data(z_p=message.text)
    await message.answer("Описание вакансии")
    await UserState.opis.set()
@dp.message_handler(state=UserState.opis)
async def get_opis(message: types.Message, state: FSMContext):
    await state.update_data(opis=message.text)
    await message.answer("Введите номер телефона, по которому можно откликнуться на вакансию")
    await UserState.number2.set()
@dp.message_handler(state=UserState.number2)
async def get_number2(message: types.Message, state: FSMContext):
    await state.update_data(number2=message.text)


    data2 = await state.get_data()
    cat = (data2['cat'])
    spec = (data2['spec'])
    gorod = (data2['gorod'])
    z_p = (data2['z_p'])
    opis = (data2['opis'])
    number2 = (data2['number2'])
    await state.finish()

    table_to_vak(cat=cat, spec=spec, gorod=gorod, z_p=z_p, opis=opis, number2=number2)
    print("Добавлено")
    button_menu = KeyboardButton('Меню')
    greet_menu = ReplyKeyboardMarkup(row_width=1)
    greet_menu.add(button_menu)
    await message.answer("Спасибо! Вакансия опубликована.", reply_markup=greet_menu)
    conn.commit()










@dp.message_handler(text=['Оставить резюме', 'Поиск резюме', 'Оставить вакансию', 'Поиск вакансии'])
async def bot_start(message: types.Message):

    if message.text == 'Оставить резюме':
        a = ReplyKeyboardRemove()
        await message.answer("Введите ваш возраст", reply_markup=a)
        await UserState.user_age.set()

    if message.text == 'Поиск резюме':
        button_rem = KeyboardButton("Ремонт")
        button_dety = KeyboardButton("Интернет")
        button_helth = KeyboardButton("Здоровье")
        button_hw = KeyboardButton("Домашние дела")
        button_brain = KeyboardButton("Образование")
        button_beauty = KeyboardButton("Красота")
        button_m = KeyboardButton("Меню")
        greet_kb_zak_one = ReplyKeyboardMarkup()
        greet_kb_zak_one.add(button_rem, button_dety, button_helth, button_hw, button_brain, button_beauty, button_m)
        await message.answer("Выберите категорию", reply_markup=greet_kb_zak_one)

        @dp.message_handler(text=["Ремонт", 'Интернет', 'Здоровье', 'Домашние дела', 'Образование', 'Красота', 'Меню'])
        async def get_pod_cat(message: types.Message, state: FSMContext):



            if message.text == "Назад":
                await message.answer("Выберите категорию", reply_markup=greet_kb_zak_one)
            else:
                cursor.execute(f"""SELECT * FROM HomeWork WHERE category = '{message.text}'""")
                result = cursor.fetchall()
                for i in result:
                    await message.answer("Имя: " + str(i[2]) + "\n" "Возраст: " + str(i[3]) + "\n" "Город: " + str(
                        i[5]) + "\n" "Номер телефона: " + str(i[4]) + "\n" "Специальность: " + str(
                        i[7]) + "\n" "Описание: " + str(i[8]) + "\n" "Ссылка: " + str(i[9]))










                    #if message.text != message.text:
                        #await message.answer("Выберите подкатегорию")


                        #await message.answer("Имя: " +(p[1]) +"\n" "Возраст: " +str(p[2]))

                    #t = (" ".join(map(str,p)))
                    #await message.answer("Имя: " +(p[1]) +"\n" "Возраст: " +str(p[2]))
                       # await message.answer("Возраст: " +int(n[r]))





            #  chat_text = message.text
               # @dp.message_handler()
               # async def get_searsh(message: types.Message):
                  #  if message.text == chat_text:
                  #      await message.reply(str(db.))





@dp.message_handler(state=UserState.user_age)
async def get_user_age(message: types.Message, state: FSMContext):

    await state.update_data(user_age=message.text)
    await message.answer("Введите ваше имя")
    await UserState.us_name.set()

@dp.message_handler(state=UserState.us_name)
async def get_user_name(message: types.Message, state: FSMContext):
    await state.update_data(us_name=message.text)
    await message.answer("Введите ваш номер телефона, чтобы заказчик смог с вами связаться")
    await UserState.number.set()

@dp.message_handler(state=UserState.number)
async def get_number(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer("Отлично! Теперь введите ваш город")
    await UserState.us_city.set()

@dp.message_handler(state=UserState.us_city)
async def get_city(message: types.Message, state: FSMContext):
    await state.update_data(us_city=message.text)
    button_rem = KeyboardButton("Ремонт")
    button_dety = KeyboardButton("Дети")
    button_helth = KeyboardButton("Здоровье")
    button_hw = KeyboardButton("Домашние дела")
    button_brain = KeyboardButton("Образование")
    button_beauty = KeyboardButton("Красота")
    greet_kb_one = ReplyKeyboardMarkup(row_width=1)
    greet_kb_one.add(button_rem, button_dety, button_helth, button_hw, button_brain, button_beauty)
    await message.answer("Осталось выбрать род занятий", reply_markup=greet_kb_one)
    await message.answer("Выберите категорию")
    await UserState.category.set()

@dp.message_handler(state=UserState.category, text=["Ремонт", 'Интернет', 'Здоровье', 'Домашние дела', 'Образование', 'Красота'])
async def get_cat(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("Введите вашу специальность")
    await UserState.pod_category.set()

@dp.message_handler(state=UserState.pod_category)
async def get_pod_cat(message: types.Message, state: FSMContext):
    await state.update_data(pod_category=message.text)
    a = ReplyKeyboardRemove()
    await message.answer("Введите описание своих услуг", reply_markup=a)
    await UserState.description.set()

@dp.message_handler(state=UserState.description)
async def get_user_age(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)

    button_end = KeyboardButton("Завершить")
    button_menu = KeyboardButton("Меню")

    greet_kb_end = ReplyKeyboardMarkup(row_width=1)
    greet_kb_end.add(button_end, button_menu)
    await message.answer("Оставьте ссылку на вашу страницу в соцсетях, либо нажмите кнопку завершения", reply_markup=greet_kb_end)
    await UserState.link.set()



@dp.message_handler(state=UserState.link)
async def get_user_age(message: types.Message, state: FSMContext):
    if message.text == "Завершить":
        await state.update_data(link="none")
        await message.answer("Спасибо за регистрацию!")
        await back_handler(message)
    else:
        await state.update_data(link=message.text)
        await message.answer("Спасибо за регистрацию!")
    data = await state.get_data()
    us_name = (data['us_name'])
    user_age = (data['user_age'])
    number = (data['number'])
    us_city = (data['us_city'])
    category = (data['category'])
    pod_category = (data['pod_category'])
    description = (data['description'])
    link = (data['link'])
    nik = message.from_user.first_name
    await state.finish()

    table_to (nik=nik, user_name=us_name, user_age=user_age, number=number, city=us_city, category=category, pod_category=pod_category, description=description, link=link)
    print("Добавлено")



    conn.commit()







if __name__ == "__main__":
    executor.start_polling(dp)