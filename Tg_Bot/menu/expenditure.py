# from aiogram.types import Message, CallbackQuery
# from aiogram.dispatcher.filters import Text
# from aiogram.dispatcher import FSMContext
# from ..bot import bot, dp
# from ..decors import admin
# from ..states import AddExpenditure
# from ..keyboards import kbd
# from DB import ExpenditureDb, SessionDb
# import traceback


# @dp.callback_query_handler(text='expenditure')
# @admin
# async def coming(cq: CallbackQuery, state: FSMContext):
#     msg = cq.message
#     user_id = msg.chat.id
#     await state.update_data(page=0)
#     await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выбери продукт:', reply_markup=kbd.all_products())
#     await AddExpenditure.product.set()


# @dp.callback_query_handler(Text(startswith='select_product_'), state=AddExpenditure.product)
# @admin
# async def select_product_(cq: CallbackQuery, state: FSMContext):
#     msg = cq.message
#     user_id = msg.chat.id
#     product = cq.data.split('select_product_')[1]
#     await state.update_data(product=product, msg=msg)
#     await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Выбери направление:', reply_markup=kbd.all_flows(product=product))
#     await AddExpenditure.next()


# @dp.callback_query_handler(Text(startswith='select_flow_'), state=AddExpenditure.flow_direction)
# @admin
# async def select_flow_(cq: CallbackQuery, state: FSMContext):
#     msg = cq.message
#     user_id = msg.chat.id
#     flow = cq.data.split('select_flow_')[1]
#     await state.update_data(flow=flow, msg=msg)
#     await bot.edit_message_text(chat_id=user_id, message_id=msg.message_id, text='Введи количество:', reply_markup=kbd.single_back())
#     await AddExpenditure.next()


# @dp.message_handler(state=AddExpenditure.count)
# @admin
# async def _count(msg: Message, state: FSMContext):
#     user_id = msg.chat.id
#     count = msg.text
#     await bot.delete_message(chat_id=user_id, message_id=msg.message_id)
#     data = await state.get_data()
#     try:
#         count = float(count)
#         await state.update_data(count = count)
#         await bot.edit_message_text(chat_id=user_id, message_id=data['msg'].message_id, text='Введи цену', reply_markup=kbd.single_back())
#         await AddExpenditure.next()
#     except:
#         await bot.edit_message_text(chat_id=user_id, message_id=data['msg'].message_id,  text=f'Неверный формат. "{msg.text}" - не число', reply_markup=kbd.single_back())


# @dp.message_handler(state=AddExpenditure.price)
# @admin
# async def _price(msg: Message, state: FSMContext):
#     user_id = msg.chat.id
#     price = msg.text
#     await bot.delete_message(chat_id=user_id, message_id=msg.message_id)
#     data = await state.get_data()
#     try:
#         price = float(price)
#         exp = ExpenditureDb(user_id=user_id,product=data['product'], count=data['count'],price=price, flow_direction =data['flow'] )
#         SessionDb.add(exp)
#         SessionDb.commit()
#         await bot.edit_message_text(chat_id=user_id, message_id=data['msg'].message_id, text='Расход записан.', reply_markup=kbd.all_products(page=data['page'] if 'page' in data.keys() else 0))
#         await AddExpenditure.product.set()
#     except:
#         await bot.edit_message_text(chat_id=user_id, message_id=data['msg'].message_id,  text=f'Неверный формат. "{msg.text}" - не число', reply_markup=kbd.single_back())



# @dp.callback_query_handler(Text(startswith='replace_page_'), state=AddExpenditure.flow_direction)
# @admin
# async def replace_page_(cq: CallbackQuery, state:FSMContext):
#     msg = cq.message
#     user_id = msg.chat.id
#     page_new = int(cq.data.split('replace_page_')[1])
#     await state.update_data(page=page_new)
#     data = await state.get_data()
#     await bot.edit_message_reply_markup(chat_id=user_id, message_id=msg.message_id, reply_markup=kbd.all_flows(page=page_new, product=data['product']))
