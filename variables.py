PRICE_WEIGHT_MOSCOW = 4.3 # для цены по весу в Москве - если выше 200кг то по 3.3
PRICE_WEIGHT_MOSCOW_200 = 3.3
ADMIN_PASSWORD = '1'

LINK_WHATSAPP = 'https://wa.me/79261068788'


# ADRESS_BISH = '👤 蓝天LT01-{}\n📞  15547009391\n{}: \n广东省广州市白云区江高镇南岗三元南路广新元素54号云创港1119-蓝天LT01库房-{} ({})'
ADRESS_MOSCOW = '别里科夫 RU-{}高生生\n电话 18565140222{}: \n广东省佛山市南海区恒大御景湾25号BK库房(RU-{}){} \n Почтовый индекс: 528200'
PINDUODUO = 'https://youtube.com/shorts/eW9HNJ_OiMM?si=k4Pvx9B9JJP_rM4F'
TAOBAO = 'https://youtube.com/shorts/JHp78xqBDwg?si=x5HZNp56I6CRQT0N'
ONE_AND_SIX = 'https://youtube.com/shorts/KHVRE2nC8Fk?si=Z_JFZzAJk0aAr0GC' #1688
POIZON = 'https://youtube.com/shorts/PL473nyMvsM?si=2PH_SX1VhrurwvoI'

def send_adress(id,phone_number,lang,city,ADRESS_MOSCOW):
    if lang == 'RU':
        if city == 'MOSCOW':
            return ADRESS_MOSCOW.format(id,'Полный адрес',id,phone_number)
    else:
        if city == 'MOSCOW':
            return ADRESS_MOSCOW.format(id,'Толук адрес',id,phone_number)
    

def send_profile(kwargs):
    if kwargs['language'] == 'RU':
        text = '📃Ваш профиль📃\n🪪 Персональный id: {}\n👤 Имя: {}\n👤 Фамилия: {}\n📞 Номер: {}\n🌍 Геопозиция: {}'
    if kwargs['language'] == 'KG':
        text = '📃Сиздин профилиниз📃\n🪪 Жеке id: {}\n👤 Аты: {}\n👤 Фамилия: {}\n📞 Номер: {}\n🌍 Турган жери: {}'
    if kwargs["city"] == 'MOSCOW':
        city = 'Москва'

    if kwargs['language'] == 'RU':
        return text.format(kwargs['id'], kwargs['name'], kwargs['full_name'], kwargs['phone_number'], city)
    elif kwargs['language'] == 'KG':
        return text.format(kwargs['id'], kwargs['name'], kwargs['full_name'], kwargs['phone_number'], city)

def cancel_sender(lang):
    if lang == 'RU':
        return f'Вы отменили последнее действие'
    else:
        return f'Акыркы аракетиңизди артка кайтардыңыз'
    