from aiogram.utils.keyboard import InlineKeyboardBuilder,InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton

def get_lang_kb(current_lang):
    if current_lang == 'RU':
        flag = '🇰🇬'
        new_lang = 'KG'
    else:
        flag = '🇷🇺'
        new_lang = 'RU'
    kb = InlineKeyboardButton(text = f'Переключить язык на {flag}',callback_data = f'switch_language_{new_lang}')
    return kb

login_or_register_ru = ReplyKeyboardMarkup(
    keyboard= [
        [
        KeyboardButton(text = 'Войти'),
        KeyboardButton(text = 'Пройти регистрацию')
        ]
    ],
    resize_keyboard=True
)

login_or_register_kg = ReplyKeyboardMarkup(
    keyboard= [
        [
        KeyboardButton(text = 'Кируу'),
        KeyboardButton(text = 'Катталуу')
        ]
    ],
    resize_keyboard=True
)

set_city_kb = InlineKeyboardBuilder(
    markup= [
        [InlineKeyboardButton(text = 'Кемин',callback_data='city_set_kemin'),]
    ]   
)
profile_kb_ru = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Изменить профиль',callback_data='update_profile')],
        [get_lang_kb('RU')],
        [InlineKeyboardButton(text = 'Выйти из профиля',callback_data = 'logout_profile')]

    ]
)
profile_kb_kg = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Профилди өзгөртүү',callback_data='update_profile')],
        [get_lang_kb('KG')],
        [InlineKeyboardButton(text = 'Профилден чыгуу',callback_data = 'logout_profile')]
    ]
)
default_kb_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = '👤Профиль'),
            KeyboardButton(text = '📬Адреса'),
            KeyboardButton(text = '📦Мои посылки'),
        ],
        [
            KeyboardButton(text = '📕Инструкция'),
            KeyboardButton(text = '🚫Запрещенные товары'),
            KeyboardButton(text = '⚙️Поддержка'),
        ],
        [
            KeyboardButton(text = '📚Тариф/условия'),
            KeyboardButton(text = '✅Добавить трек код'),
        ]
    ],
    resize_keyboard=True
)

default_kb_kg = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = '👤Профиль'),
            KeyboardButton(text = '📬Дарек'),
            KeyboardButton(text = '📦Менин товарларым'),
            
        ],
        [
            KeyboardButton(text = '📕Нускама'),
            KeyboardButton(text = '🚫Тыюу салынган товарлар'),
            KeyboardButton(text = '⚙️Колдоо'),
        ],
        [
            KeyboardButton(text = '📚Жеткирүү баасы/мөөнөтү'),
            KeyboardButton(text = '✅Трек код кошуу'),
        ]
    ],
    resize_keyboard=True
)
cancel_calc_ru = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text = 'Отмена')
        ]
    ],
    resize_keyboard=True
)
cancel_calc_kg = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text = 'Артка')
        ]
    ],
    resize_keyboard=True
)


tracking_kb_ru = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'По трек-коду',callback_data = 'track-code')],
        [InlineKeyboardButton(text = 'По коду клиента',callback_data='client_id')]
    ]
)


tracking_kb_kg = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Трек код боюнча',callback_data = 'track-code')],
        [InlineKeyboardButton(text = 'Жеке id боюнча',callback_data='client_id')]
    ]
)

instruction_kb = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Pinduoduo',callback_data = 'choose_pin')],
        [InlineKeyboardButton(text = 'Taobao',callback_data = 'choose_tao')],
        [InlineKeyboardButton(text = '1688',callback_data = 'choose_1688')],
        [InlineKeyboardButton(text = 'Poizon',callback_data = 'choose_poi')]
    ]
)

set_variables_kbds = InlineKeyboardBuilder(
    markup = [
        [InlineKeyboardButton(text = 'Поменять цены',callback_data='set_prices')],
        [InlineKeyboardButton(text = 'Поменять ссылку для поддержки',callback_data = 're_whatsapp')],
        [InlineKeyboardButton(text = 'Поменять маркетплейсы',callback_data='set_marketplace')],
        [InlineKeyboardButton(text = 'Рассылка новостей',callback_data = 'send_broadcast')],
        [InlineKeyboardButton(text = 'Сменить пароль админа',callback_data = 'reset_password')],
        [InlineKeyboardButton(text = 'Сменить адрес Кемина',callback_data = 'reset_city_kemin')],
        [InlineKeyboardButton(text = 'Рассылка о выданной посылке',callback_data = 'send_delivered')],
        [InlineKeyboardButton(text = 'Выйти',callback_data='logout_admin')]
    ]
)

set_marketplace = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Pinduoduo',callback_data = 'r_pinduoduo')],
        [InlineKeyboardButton(text = 'TAOBAO',callback_data = 'r_taobao')],
        [InlineKeyboardButton(text = '1688',callback_data = 'r_1688')],
        [InlineKeyboardButton(text = 'POIZON',callback_data = 'r_poizon')]
    ]
)

set_price = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Цена по весу в Кемине',callback_data = 'p_price_weight_kemin')]
    ]
)