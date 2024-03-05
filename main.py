import logging
from io import BytesIO

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from reportlab.lib.colors import blue
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

API_TOKEN = '6860436179:AAGmizGcCWjMHVGpUpk_08IapafmIjQfqYE'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

storage = MemoryStorage()
dp.storage = storage
DATABASE_URL = 'sqlite:///food.db'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Users(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    fullname = Column(String)
    address = Column(String)
    about_me = Column(String)
    phone_number = Column(Integer)
    github_link = Column(String)
    level = Column(String)
    Technology = Column(String)
    salary = Column(String)
    school = Column(String)
    education_direction = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def save_order_to_database(db_session: Session, data):
    order = Users(fullname=data['fullname'], address=data['address'], about_me=data["about_me"],
                  phone_number=data['phone_number'], github_link=data['github_link'],
                  level=data['level'], Technology=data["Technology"], salary=data["salary"], school=data["school"],
                  education_direction=data["education_direction"])
    db_session.add(order)
    db_session.commit()


class User(StatesGroup):
    fullname = State()
    address = State()
    about_me = State()
    phone_number = State()
    github_link = State()
    level = State()
    Technology = State()
    salary = State()
    school = State()
    education_direction = State()

    oʻchirish = State()


def generate_order_pdf(order_info):
    bio = BytesIO()
    c = canvas.Canvas(bio, pagesize=letter)
    c.setFillColor(blue)
    c.drawString(100, 750, "Shoh Resume")
    y_position = 730
    for line in order_info.split('\n'):
        c.drawString(100, y_position, line)
        y_position -= 20

    c.save()
    pdf_bytes = bio.getvalue()
    return pdf_bytes


from aiogram.dispatcher import FSMContext



from aiogram.dispatcher import FSMContext

#
# @dp.callback_query_handler(text="o'chirish")
# async def clear_data_button_handler(query: types.CallbackQuery, state: FSMContext):
#     # Extract user id from the callback query
#     user_id = query.from_user.id
#
#     # Delete user data from the database
#     db_session = Session()
#     delete_user_data_from_database(db_session, user_id)
#     db_session.close()
#
#     # Clear user's state
#     await state.finish()
#
#     # Send a message confirming that data has been cleared
#     await query.message.answer("Your data has been cleared successfully.")


def order_keyboard():
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton("o'chirish", callback_data="o'chirish"))
    return ikm


@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer("Assalomu alaykum! \nIltimos fullname kiriting:")
    await User.fullname.set()


@dp.message_handler(state=User.fullname)
async def process_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fullname'] = message.text
    await User.next()
    await message.answer(" manzilingizni kiriting:")
    await User.address.set()


@dp.message_handler(state=User.address)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["address"] = message.text
        await User.next()
        await message.answer(" oʻzingiz haqingizda qisqacha  kiriting ")
        await User.about_me.set()

@dp.message_handler(state=User.about_me)
async def process_about_me(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["about_me"] = message.text
    await User.next()
    await message.answer("Telefon raqamingizni kiriting", reply_markup=ReplyKeyboardRemove())
    await User.phone_number.set()


@dp.message_handler(state=User.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phone_number"] = message.text
        phone_number = message.text.strip()

        if phone_number.isdigit() and len(phone_number) == 9:
            data['phone_number'] = phone_number
            await User.next()
            await message.answer(" github_linkizni kiriting ")
            await User.github_link.set()
        else:
            await message.answer("Noto'g'ri telefon raqam. Iltimos, 9 xonali raqam kiriting.")



@dp.message_handler(state=User.github_link)
async def process_github_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["github_link"] = message.text
        await User.next()
        await message.answer("darajangizni kiriting ")
        await User.level.set()


@dp.message_handler(state=User.level)
async def process_level(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["level"] = message.text
        await User.next()
        await message.answer("technology kiriting ")
        await User.Technology.set()


@dp.message_handler(state=User.Technology)
async def process_technology(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["Technology"] = message.text
        await User.next()
        await message.answer("qancha ish haqqi talab qilasiz kiriting")
        await User.salary.set()


@dp.message_handler(state=User.salary)
async def process_salary(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["salary"] = message.text
        await User.next()
        await message.answer("qayerlarda oʻqigansiz")
        await User.school.set()


@dp.message_handler(state=User.school)
async def process_school(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["school"] = message.text
        await User.next()
        await message.answer("qachon oʻqishni tugatgansiz")
        await User.education_direction.set()


@dp.message_handler(state=User.education_direction)
async def process_education_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["education_direction"] = message.text
        order_info = (
            f"Fullname: {data['fullname']}\n"
            f"Address : {data['address']}\n"
            f"Telefon nomer: +998 {data['phone_number']}\n"
            f"about_me : {data['about_me']}\n"
            f"github_link : {data['github_link']}\n"
            f"level : {data['level']}\n"
            f"Technology : {data['Technology']}\n"
            f"salary : {data['salary']}\n"
            f"school : {data['school']}\n"
            f"education_direction : {data['education_direction']}\n"
        )
        await message.answer(f"{order_info} Malumotingiz", reply_markup=order_keyboard())

        await User.oʻchirish.set()
        pdf_bytes = generate_order_pdf(order_info)
        bio = BytesIO(pdf_bytes)
        bio.name = "order_info.pdf"
        await message.answer_document(bio)
        db_session = Session()
        save_order_to_database(db_session, data)
        db_session.close()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
