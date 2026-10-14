# Tg not 2  
from aiogram import Router, F  
from aiogram.filters import CommandStart, Command  
from aiogram.types import (  
    Message,  
    LabeledPrice,  
    PreCheckoutQuery,  
    InlineKeyboardMarkup,  
    InlineKeyboardButton,  
    CallbackQuery,  
)  
from aiogram.fsm.context import FSMContext  
from aiogram.fsm.state import State, StatesGroup  
from config import PAYMENT_TOKEN  
  
router = Router()  
  
# Ссылки (замените юзернейм на свой)  @
DIRECTOR_TG = "https://t.me/EvKRomanov"  # Ссылка на ваш личный TG  
YOUTUBE_PLAYLIST = "https://youtube.com/playlist?list=PLBx5zww72gbg&si=EU8Pu0U1MnkAWjtx"  # Ссылка на бесплатный плейлист  
  
# Каталог курсов и предметов  
COURSES = {  
    "math_opora_self": {  
        "title": "Профильная математика: «Опора» (Самопроверка)",  
        "description": "4 вебинара/нед, ДЗ, пробники, банк материалов на 1 месяц.",  
        "price": 490000,  # 4 900 руб  
    },  
    "math_opora_expert": {  
        "title": "Профильная математика: «Опора» (Эксперт)",  
        "description": "4 вебинара/нед, индивидуальная проверка экспертом, материалы.",  
        "price": 590000,  # 5 900 руб  
    },  
    "physics_base": {  
        "title": "Физика: Полный экспресс-курс",  
        "description": "Механика, термодинамика, электродинамика. Все темы ЕГЭ/ОГЭ.",  
        "price": 450000,  # 4 500 руб  
    },  
    "inf_base": {  
        "title": "Информатика: Практикум по кодингу",  
        "description": "Разбор Python, динамическое программирование, теория графов.",  
        "price": 450000,  # 4 500 руб  
    },  
}  
  
# Вопросы для викторины по теории чисел  
QUIZ_QUESTIONS = [  
    {  
        "question": "Вопрос 1/3:\nСколько натуральных делителей имеет простое число?",  
        "options": ["Только 1", "Ровно 2 (1 и само число)", "Бесконечно много", "Зависит от четности"],  
        "correct": 1  
    },  
    {  
        "question": "Вопрос 2/3:\nКакое наименьшее общее кратное (НОК) у чисел 6 и 8?",  
        "options": ["48", "14", "24", "12"],  
        "correct": 2  
    },  
    {  
        "question": "Вопрос 3/3:\nЧисло делится на 9 тогда и только тогда, когда...",  
        "options": [  
            "Оно оканчивается на 9",  
            "Сумма его цифр делится на 9",  
            "Оно делится на 3 и на 6",  
            "Последние две цифры кратны 9"  
        ],  
        "correct": 1  
    }  
]  
  
# Машина состояний для FSM  
class BotStates(StatesGroup):  
    quiz_step = State()  
    waiting_cert_name = State()  
  
# Главное меню (Инлайн)  
def main_menu_keyboard():  
    return InlineKeyboardMarkup(  
        inline_keyboard=[  
            [InlineKeyboardButton(text="🎓 О курсе «Точка опоры»", callback_data="menu:about")],  
            [InlineKeyboardButton(text="📚 Каталог предметов и тарифов", callback_data="menu:catalog")],  
            [InlineKeyboardButton(text="🧠 Викторина по теории чисел", callback_data="menu:quiz_start")],  
            [InlineKeyboardButton(text="📺 Бесплатный курс (YouTube)", url=YOUTUBE_PLAYLIST)],  
            [InlineKeyboardButton(text="🎓 Получить сертификат об окончании", callback_data="menu:certificate")],  
            [InlineKeyboardButton(text="💬 Частые вопросы и Поддержка", callback_data="menu:faq")],  
        ]  
    )  
  
# --- 1. СТАРТ И ГЛАВНОЕ МЕНЮ ---  
@router.message(CommandStart())  
async def cmd_start(message: Message, state: FSMContext):  
    await state.clear()  
    await message.answer(  
        f"👋 Приветствуем, {message.from_user.first_name}!\n\n"  
        "Добро пожаловать в образовательный центр Karmadonov School \n"  
        "Выберите интересующий раздел в меню ниже:",  
        reply_markup=main_menu_keyboard()  
    )  
  
@router.callback_query(F.data == "menu:main")  
async def back_to_main(callback: CallbackQuery, state: FSMContext):  
    await state.clear()  
    await callback.message.edit_text(  
        "Главное меню школы:",  
        reply_markup=main_menu_keyboard()  
    )  
    await callback.answer()  
  
# --- 2. О КУРСЕ ---  
@router.callback_query(F.data == "menu:about")  
async def about_course(callback: CallbackQuery):  
    text = (  
        "📖 <b>О флагманском курсе «Точка опоры»:</b>\n\n"  
        "• <b>4 вебинара каждую неделю</b> с детальным разбором теории и задач;\n"  
        "• <b>Домашние задания</b> разного уровня сложности с видеоразборами;\n"  
        "• <b>Полноценные пробники</b> каждый месяц с таймингом реального экзамена;\n"  
        "• <b>Банк материалов:</b> конспекты, формуляры, чек-листы и скрипты к каждому уроку."  
    )  
    kb = InlineKeyboardMarkup(inline_keyboard=[  
        [InlineKeyboardButton(text="💳 Выбрать тариф и оплатить", callback_data="menu:catalog")],  
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="menu:main")]  
    ])  
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb)  
    await callback.answer()  
  
# --- 3. КАТАЛОГ ПРЕДМЕТОВ И ОПЛАТА ---  
@router.callback_query(F.data == "menu:catalog")  
async def catalog_menu(callback: CallbackQuery):  
    kb = InlineKeyboardMarkup(  
        inline_keyboard=[  
            [InlineKeyboardButton(text="«Опора» (Самопроверка) — 4 900 ₽", callback_data="buy:math_opora_self")],  
            [InlineKeyboardButton(text="«Опора» (С экспертом) — 5 900 ₽", callback_data="buy:math_opora_expert")],  
            [InlineKeyboardButton(text="Физика (Экспресс) — 4 500 ₽", callback_data="buy:physics_base")],  
            [InlineKeyboardButton(text="Информатика (Кодинг) — 4 500 ₽", callback_data="buy:inf_base")],  
            [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="menu:main")],  
        ]  
    )  
    await callback.message.edit_text("Выберите предмет и необходимый тариф для оплаты:", reply_markup=kb)  
    await callback.answer()  
  
@router.callback_query(F.data.startswith("buy:"))  
async def process_buy(callback: CallbackQuery):  
    item_key = callback.data.split(":")[1]  
    item = COURSES.get(item_key)  
    if not item:  
        await callback.answer("Товар не найден", show_alert=True)  
        return  
  
    await callback.message.answer_invoice(  
        title=item["title"],  
        description=item["description"],  
        payload=f"order_{item_key}_{callback.from_user.id}",  
        provider_token=PAYMENT_TOKEN,  
        currency="RUB",  
        prices=[LabeledPrice(label=item["title"], amount=item["price"])],  
        start_parameter=f"pay_{item_key}",  
        need_name=True,  
        need_phone_number=True,  
        need_email=True,  
        send_email_to_provider=True,  
    )  
    await callback.answer()  
  
@router.pre_checkout_query()  
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):  
    await pre_checkout_query.answer(ok=True)  
  
@router.message(F.successful_payment)  
async def process_successful_payment(message: Message):  
    pm = message.successful_payment  
    amount_rub = pm.total_amount // 100  
    await message.answer(  
        f"✅ <b>Оплата успешно получена ({amount_rub} ₽)!</b>\n\n"  
        f"Чек будет направлен на: {pm.order_info.email if pm.order_info else 'email'}\n"  
        "Доступ к обучающей платформе открыт! Напишите генеральному директору для добавления в чат группы.",  
        parse_mode="HTML"  
    )  
  
# --- 4. ПОДДЕРЖКА И СВЯЗЬ С ГЕНДИРЕКТОРОМ ---  
@router.callback_query(F.data == "menu:faq")  
async def support_faq(callback: CallbackQuery):  
    text = (  
        "❓ <b>Часто задаваемые вопросы:</b>\n\n"  
        "Q: С какого момента открывается доступ?\n"  
        "A: Сразу после подтверждения оплаты кассой.\n\n"  
        "Q: Что делать, если не успел на онлайн-вебинар?\n"  
        "A: Все записи и презентации сохраняются в личном кабинете навсегда."  
    )  
    kb = InlineKeyboardMarkup(  
        inline_keyboard=[  
            [InlineKeyboardButton(text="👤 Связь с генеральным директором", url=DIRECTOR_TG)],  
            [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="menu:main")],  
        ]  
    )  
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=kb)  
    await callback.answer()  
  
# --- 5. ВИКТОРИНА ПО ТЕОРИИ ЧИСЕЛ ---  
@router.callback_query(F.data == "menu:quiz_start")  
async def quiz_start(callback: CallbackQuery, state: FSMContext):  
    await state.set_state(BotStates.quiz_step)  
    await state.update_data(score=0, step=0)  
    await show_quiz_question(callback.message, 0)  
    await callback.answer()  
  
async def show_quiz_question(message: Message, step: int):  
    q = QUIZ_QUESTIONS[step]  
    buttons = [  
        [InlineKeyboardButton(text=opt, callback_data=f"ans:{idx}")]  
        for idx, opt in enumerate(q["options"])  
    ]  
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)  
    await message.edit_text(f"🎲 <b>Интерактивная викторина: Теория чисел</b>\n\n{q['question']}", parse_mode="HTML", reply_markup=kb)  
  
@router.callback_query(BotStates.quiz_step, F.data.startswith("ans:"))  
async def process_quiz_answer(callback: CallbackQuery, state: FSMContext):  
    data = await state.get_data()  
    step = data.get("step", 0)  
    score = data.get("score", 0)  
    user_ans = int(callback.data.split(":")[1])  
  
    if user_ans == QUIZ_QUESTIONS[step]["correct"]:  
        score += 1  
  
    step += 1  
    if step < len(QUIZ_QUESTIONS):  
        await state.update_data(score=score, step=step)  
        await show_quiz_question(callback.message, step)  
    else:  
        await state.clear()  
        kb = InlineKeyboardMarkup(  
            inline_keyboard=[  
                [InlineKeyboardButton(text="💳 Записаться на курс", callback_data="menu:catalog")],  
                [InlineKeyboardButton(text="⬅️ В главное меню", callback_data="menu:main")]  
            ]  
        )  
        await callback.message.edit_text(  
            f"🎉 <b>Викторина завершена!</b>\n\n"  
            f"Ваш результат: <b>{score} из {len(QUIZ_QUESTIONS)}</b> правильных ответов.\n\n"  
            "Хотите прокачать решение задач на максимум? Выбирайте тариф в каталоге!",  
            parse_mode="HTML",  
            reply_markup=kb  
        )  
    await callback.answer()  
  
# --- 6. СЕРТИФИКАТЫ ОБ ОКОНЧАНИИ ---  
@router.callback_query(F.data == "menu:certificate")  
async def ask_certificate_name(callback: CallbackQuery, state: FSMContext):  
    await state.set_state(BotStates.waiting_cert_name)  
    await callback.message.answer(  
        "🎓 <b>Оформление сертификата выпускника</b>\n\n"  
        "Напишите в ответном сообщении ваши <b>Имя и Фамилию</b>:",  
        parse_mode="HTML"  
    )  
    await callback.answer()  
  
@router.message(BotStates.waiting_cert_name)  
async def issue_certificate(message: Message, state: FSMContext):  
    user_name = message.text.strip()  
    await state.clear()  
      
    cert_text = (  
        "╔══════════════════════════════════════╗\n"  
        "║      🏆 ЭЛЕКТРОННЫЙ СЕРТИФИКАТ       ║\n"  
        "║          ОБ ОКОНЧАНИИ ОБУЧЕНИЯ       ║\n"  
        "╠══════════════════════════════════════╣\n"  
        f"║ Выдан: {user_name:<30}║\n"  
        "║ Курс: «Точка опоры»                  ║\n"  
        "║ Предмет: Профильная математика       ║\n"  
        "║ Статус: Успешно освоен               ║\n"  
        "╚══════════════════════════════════════╝"  
    )  
      
    kb = InlineKeyboardMarkup(  
        inline_keyboard=[[InlineKeyboardButton(text="⬅️ Вернуться в меню", callback_data="menu:main")]]  
    )  
    await message.answer(  
        f"Поздравляем, {user_name}!\nВаш официальный сертификат сформирован:\n\n<pre>{cert_text}</pre>",  
        parse_mode="HTML",  
        reply_markup=kb  
    )  
