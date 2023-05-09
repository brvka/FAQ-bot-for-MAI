import logging

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Command, Text

from config import data
from keyboards.inline.callback_datas import *
from keyboards.inline.choice_buttons import menu
from loader import dp
from states.sostoy import sostoy


@dp.message_handler(Command("start"), state='*')
async def start(message: Message):
    await message.answer("Привет, {0}! В этом боте ты узнаешь ответы на все вопросы, которые таят в себе стены МАИ. Просто выбери интересующую тебя тему".format(message.from_user.first_name), reply_markup=menu)
    await sostoy.glavnaya.set()


@dp.callback_query_handler(text_contains="category", state=sostoy.glavnaya)
async def category(call: CallbackQuery):
    await call.answer(cache_time=60)
    category = call.data.split(":")[1]
    for el in data['faq']:
        if el['category'] == category:
            try:
                subcat_categories = [el2['category'] for el2 in el['subcategory']]

                subcat_menu = InlineKeyboardMarkup(row_width=1)
                buttons = [InlineKeyboardButton(text=el,
                                                callback_data=subcat_callback.new(subcat_cat=category, subcat_text=el)) for el in subcat_categories]
                for el in buttons:
                    subcat_menu.insert(el)

                return_button = InlineKeyboardButton(text="Вернуться назад", callback_data="cancel")
                subcat_menu.add(return_button)

                await call.message.answer("Выберите подкатегорию", reply_markup=subcat_menu)
            except:
                que_list = await get_questions(category)

                que_menu = InlineKeyboardMarkup(row_width=1)
                buttons = [InlineKeyboardButton(text=el['question'], callback_data=que_callback.new(que_cat=category, que_subcat='', que_id=el['id'])) for el in
                           que_list]
                for el in buttons:
                    que_menu.insert(el)

                return_button = InlineKeyboardButton(text="Вернуться назад", callback_data="cancel")
                que_menu.add(return_button)

                await sostoy.category.set()
                await call.message.answer("Выберите вопрос из списка", reply_markup=que_menu)


@dp.callback_query_handler(text_contains="subc_ategory", state=sostoy.glavnaya)
async def subcategory(call: CallbackQuery):
    await call.answer(cache_time=60)
    _, category, subcategory = call.data.split(":")

    que_list = await get_questions(category, subcategory)

    que_menu = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(text=el['question'],
                                    callback_data=que_callback.new(que_cat=category, que_subcat=subcategory, que_id=el['id']))
               for el in
               que_list]
    for el in buttons:
        que_menu.insert(el)
    return_button = InlineKeyboardButton(text="Вернуться назад", callback_data="cancel")
    que_menu.add(return_button)

    await sostoy.category.set()
    await call.message.answer("Выберите вопрос из списка", reply_markup=que_menu)


@dp.callback_query_handler(text_contains="question", state=sostoy.category)
async def question(call: CallbackQuery):
    await call.answer(cache_time=60)
    _, que_cat, que_subcat, que_id = call.data.split(":")
    for el in data['faq']:
        if el['category'] == que_cat:
            if que_subcat == "":
                the_element = el['questions']
                break
            else:
                for elem in el['subcategory']:
                    if elem['category'] == que_subcat:
                        the_element = elem['questions']
                        break
    for question in the_element:
        if str(question['id']) == que_id:
            await call.message.answer(question['answer'])
            await sostoy.glavnaya.set()
            await call.message.answer("Возвращаем вас в главное меню", reply_markup=menu)


@dp.callback_query_handler(Text(equals=["cancel"]), state='*')
async def cancel(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer('Вы в главном меню. Выберите категорию вопроса', reply_markup=menu)
    await sostoy.glavnaya.set()


async def get_questions(category, subcategory=None):
    for el in data['faq']:
        if el['category'] == category:
            if subcategory:
                for el2 in el['subcategory']:
                    if el2['category'] == subcategory:
                        return el2['questions']
            else:
                return el['questions']