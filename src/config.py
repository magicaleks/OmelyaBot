config = {
    'bot': {
        'token': '5643404684:AAFrDOcFUcCywfKh_wdFv9Q-8HrxGLrz49I',
        'admins': [945482940, 1640897457]
    },

    'db': {
        'uri': 'mongodb://massagedb:27017',
        'timeout': 10,
        'name': 'massagedb'
    },

    'services': {
        'massages': ['Комплексный массаж', 'Термо-инфракрасная капсула', 'Выездной массаж'],
        'prices': {
            'Комплексный массаж': 1500,
            'Термо-инфракрасная капсула': 1000,
            'Выездной массаж': 4000
        }
    },

    'payments': {
        'token': '381764678:TEST:45436'
    }
}
