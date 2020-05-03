from flask import Flask, request
import logging
import json
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# создаем словарь, в котором ключ — название города,
# а значение — массив, где перечислены id картинок,
# которые мы записали в прошлом пункте.

cities = {
    'москва': '1030494/172b28f45e6660180e70',
    'нью-йорк': '1533899/283e55e768024752dc95',
    'париж': "1540737/4c0a41e67e2f2bd3bc20",
    'милан': '213044/66f1ac9423706a467910',
    'прага': '213044/d5d01a000fd1915b9102',
    'рига': '1521359/990ea96179316ea196e7',
    'ярославль': '1533899/21664799215ca2c26258',
    'дубай': '1533899/48c415d2bf1495af3f01',
    'казань': '1533899/467828424886676bc86c',
}

# создаем словарь, где для каждого пользователя
# мы будем хранить его имя
sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info(f'Response: {response!r}')
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']

    # если пользователь новый, то просим его представиться.
    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови свое имя!'
        # создаем словарь в который в будущем положим имя пользователя
        sessionStorage[user_id] = {
            'first_name': None,
            'level': 1,
            'true': 0,
            'attempts': 0
        }
        return

    # если пользователь не новый, то попадаем сюда.
    # если поле имени пустое, то это говорит о том,
    # что пользователь еще не представился.
    if sessionStorage[user_id]['first_name'] is None:
        # в последнем его сообщение ищем имя.
        first_name = get_first_name(req)
        # если не нашли, то сообщаем пользователю что не расслышали.
        if first_name is None:
            res['response']['text'] = \
                'Не расслышала имя. Повтори, пожалуйста!'
        # если нашли, то приветствуем пользователя.
        # И спрашиваем какой город он хочет увидеть.
        else:
            sessionStorage[user_id]['first_name'] = first_name
            sessionStorage[user_id]['level'] = 1
            sessionStorage[user_id]['true'] = 0
            sessionStorage[user_id]['attempts'] = 0
            res['response'][
                'text'] = 'Приятно познакомиться, ' \
                          + first_name.title() \
                          + '. Я Алиса. Сейчас мы сыграем в географический' \
                            ' тест. На экране будет изображение' \
                            ' географического объекта, а ты должен' \
                            ' будешь угадать его название.'
            """res['response']['buttons'] = [
                {
                    'title': 'Старт!',
                    'hide': True
                }
            ]"""
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['image_id'] = cities['москва']
    # если мы знакомы с пользователем и он нам что-то написал,
    # то это говорит о том, что он уже говорит о городе,
    # что хочет увидеть.
    else:
        # ищем город в сообщение от пользователя
        city = get_city(req)
        # если этот город среди известных нам,
        # то показываем его (выбираем одну из двух картинок случайно)
        if city in cities and city == 'москва' and sessionStorage[user_id]['true'] == 0:
            res['response']['buttons'] = [
                {
                    'title': 'Канберра',
                    'hide': True
                }
            ]
            res['response']['buttons'] = [
                {
                    'title': 'Москва',
                    'hide': True
                }
            ]
            res['response']['buttons'] = [
                {
                    'title': 'Париж',
                    'hide': True
                }
            ]
            res['response']['text'] = 'Верно!'
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['image_id'] = cities['нью-йорк']
            sessionStorage[user_id]['true'] += 1
        elif city in cities and city == 'нью-йорк' and sessionStorage[user_id]['true'] == 1:
            res['response']['buttons'] = [
                {
                    'title': 'Нью-Йорк',
                    'hide': True
                }
            ]
            res['response']['buttons'] = [
                {
                    'title': 'Сидней',
                    'hide': True
                }
            ]
            res['response']['buttons'] = [
                {
                    'title': 'Шанхай',
                    'hide': True
                }
            ]
            res['response']['text'] = 'Верно!'
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['image_id'] = cities['париж']
            sessionStorage[user_id]['true'] += 1
        elif city in cities and city == 'париж' and sessionStorage[user_id]['true'] == 2:
            res['response']['text'] = 'Верно!'
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['image_id'] = cities['милан']
            sessionStorage[user_id]['true'] += 1
        elif city in cities and city == 'милан' and sessionStorage[user_id]['true'] == 3:
            res['response']['text'] = 'Верно!'
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['image_id'] = cities['прага']
            sessionStorage[user_id]['true'] += 1
        elif city in cities and city == 'прага' and sessionStorage[user_id]['true'] == 4:
            res['response']['text'] = 'Верно!'
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['image_id'] = cities['рига']
            sessionStorage[user_id]['true'] += 1
        elif city in cities and city == 'рига' and sessionStorage[user_id]['true'] == 5:
            res['response']['text'] = 'Верно!'
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['image_id'] = cities['ярославль']
            sessionStorage[user_id]['true'] += 1
        elif city in cities and city == 'ярославль' and sessionStorage[user_id]['true'] == 6:
            res['response']['text'] = 'Верно!'
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['image_id'] = cities['дубай']
            sessionStorage[user_id]['true'] += 1
        elif city in cities and city == 'дубай' and sessionStorage[user_id]['true'] == 7:
            res['response']['text'] = 'Верно!'
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['image_id'] = cities['казань']
            sessionStorage[user_id]['true'] += 1
        elif city in cities and city == 'казань' and sessionStorage[user_id]['true'] == 8:
            res['response']['text'] = 'Верно!'
            sessionStorage[user_id]['true'] += 1
        elif sessionStorage[user_id]['true'] == 9:
            res['response']['text'] = 'Верно! Вы потратили' + sessionStorage[user_id]['attempts']
        # если не нашел, то отвечает пользователю
        # 'Первый раз слышу об этом городе.'
        else:
            res['response']['text'] = \
                'Не верно! Попробуй ещё раз.'


def get_city(req):
    # перебираем именованные сущности
    for entity in req['request']['nlu']['entities']:
        # если тип YANDEX.GEO то пытаемся получить город(city),
        # если нет, то возвращаем None
        if entity['type'] == 'YANDEX.GEO':
            # возвращаем None, если не нашли сущности с типом YANDEX.GEO
            return entity['value'].get('city', None)


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
