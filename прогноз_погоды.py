import requests
import calendar

api_key = '<ваш_API_ключ>'
api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + '<ваш_API_ключ>'

running = True

print('Добро пожаловать в приложение прогноза погоды от Виктора, использующее OpenWeather')

# Программный цикл
while running:

    # Запрос у пользователя название города или индекса
    while True:

        # Проверка ввода
        try:
            print('Это приложение поддерживает поиск по городу (0) и поиск по почтовому индексу (1).')
            search = int(input('Пожалуйста введите 0 или 1: '))
        except ValueError:
            print("Извините, мне это не понятно.")
        else:

            # Начало проверочного теста
            if search == 0:
                city = input('Пожалуйста, введите название города: ')
                if city.lower() == 'NY':
                    city = 'New York, US'

                # Добовляем город к вызову API
                api_call += '&q=' + city
                break

            elif search == 1:
                zip_code = input('Пожалуйста введите почтовый индекс: ')

                # Добовляем почтовый индекс к вызову API
                api_call += '&zip=' + zip_code
                break

            else:
                # Печатает неверное число ( ни 0, ни 1)
                print('{} не является допустимым параметром.'.format(search))

    # Сохраняет ответ Json
    json_data = requests.get(api_call).json()

    location_data = {
        'город': json_data['город']['название'],
        'страна': json_data['город']['страна']
    }

    print('\n{город}, {cтрана}'.format(**location_data))

    # Текущая дата которую мы итерируем
    current_date = ''

    # Перебирает массив словарей с list в json_data
    for item in json_data['list']:

        # Время получения данных о погоде разбитое на 3-х часовые блоки
        time = item['dt_txt']

        # Разделить время на дату и час [2022-11-18 06:00:00]
        next_date, hour = time.split(' ')

        # Сохраняет текущую дату и печатает ее один раз
        if current_date != next_date:
            current_date = next_date
            year, month, day = current_date.split('-')
            date = {'y': year, 'm': month, 'd': day}
            print('\n{m}/{d}/{y}'.format(**date))

        # Берем первые 2 целых числа ЧЧ:ММ:СС, чтобы получить часы
        hour = int(hour[:2])

        # Устанавливает часы до полудня (АМ) и после полудня (РМ)
        if hour < 12:
            if hour == 0:
                hour = 12
            meridiem = 'AM'
        else:
            if hour > 12:
                hour -= 12
            meridiem = 'PM'

        # Печатаем часы [ЧЧ:MM AM/PM]
        print('\n%i:00 %s' % (hour, meridiem))

        # Температура измеряется в Кельвинах
        temperature = item['главный']['температура']

        # Погодные условия
        description = item['погода'][0]['description'],

        # Печатает описание, а так же температуру в Цельсиях и по Фарингейту
        print('Погодные условия: %s' % description)
        print('Цельсий: {:.2f}'.format(temperature - 273.15))
        print('Фарингейт: %.2f' % (temperature * 9 / 5 - 459.67))

    # Печатает колендарь текущего месяца
    calendar = calendar.month(int(year), int(month))
    print('\n' + calendar)

    # Спрашивает пользователя хочет ли он выйти
    while True:
        running = input('Чем еще мы можем вам помочь? ')
        if running.lower() == 'да' or running.lower() == 'д':
            print('Отлично!')
            break
        elif running.lower() == 'нет' or running.lower() == 'н' or running == 'выход':
            print('Спасибо что используете на приложения для прогноза погоды.')
            print('Хорошего дня!')
            running = False
            break
        else:
            print('Извините, мы вас не поняли.')