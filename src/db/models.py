import datetime
from abc import ABC
import enum

import bson
from ..config import config

class _Document(ABC):

    _id: bson.ObjectId  # id in mongo documents (we won't use it)
    _payload: dict  # payload

    def __init__(self, *args, **kwargs):
        self._payload = dict()

    # @abstractmethod
    # def get_payload(self):
    #     raise NotImplementedError("get_payload method not implemented yet.")

    def get_payload(self) -> dict:  # returns payload to insert in mongo collection
        return self._payload

    # @abstractstaticmethod
    # def from_payload(_payload: dict):  # returns class instance from mongo document payload
    #     raise NotImplementedError("from_payload method not implemented yet.")


class Day(_Document):
    id: str
    timestamp: int
    alias: str
    booked: dict

    months = [
        'Янв.', 'Фев.', 'Март', 'Апр.', 'Май', 'Июнь', 'Июль', 'Авг.', 'Сен.', 'Окт.', 'Ноя.', 'Дек.'
    ]

    def __init__(self, *, _id: str, timestamp: int = None, booked: dict = {}, alias: str = '', **kwargs) -> None:
        super().__init__()
        self._payload['_id'] = _id
        if timestamp:
            self._payload['timestamp'] = timestamp
        else:
            _date = datetime.datetime.strptime(_id, '%d/%m/%Y')
            self._payload['timestamp'] = datetime.datetime(
                _date.year,
                _date.month,
                _date.day,
                tzinfo=datetime.timezone(
                    datetime.timedelta(
                        hours=3
                    )
                )
            ).timestamp()
        self._payload['alias'] = alias if alias else f"{_id.split('/')[0]} {Day.months[int(_id.split('/')[1])-1]}"
        if not booked:
            for m in config['services']['massages']:
                booked[m] = {}
                for i in range(7, 23):
                    booked[m][i.__str__()] = None
        self._payload['booked'] = booked
        self.booked = booked

    @property
    def timestamp(self):
        return self._payload['timestamp']

    @property
    def id(self):
        return self._payload['_id']
    
    @property
    def alias(self):
        return self._payload['alias']


class PaymentTypes(enum.Enum):
    CASH = 1
    CARD = 2
    TON = 3


class Booking(_Document):
    id: str
    user: int
    type: PaymentTypes
    confirmed: bool
    massage: str

    def __init__(self, *, _id: str, user: int = None, payment_type: PaymentTypes = None, confirmed: bool = None, massage: str = None, **kwargs) -> None:
        super().__init__()
        self._payload['_id'] = _id
        self._payload['user'] = user
        if isinstance(payment_type, PaymentTypes):
            self._payload['payment_type'] = payment_type.value
        else:
            self._payload['payment_type'] = payment_type
        self._payload['confirmed'] = confirmed
        self._payload['massage'] = massage

    @property
    def id(self):
        return self._payload['_id']
    
    @property
    def massage(self):
        return self._payload['massage']
    
    @property
    def user(self):
        return self._payload['user']
    
    @property
    def type(self):
        return PaymentTypes(self._payload['type']) if self._payload['type'] else None
    
    @property
    def confirmed(self):
        return self._payload['confirmed']


class User(_Document):
    id: int
    name: str
    phone: str
    referer_id: int
    referals_ids: list[int]
    points: int

    def __init__(self, *, _id: int, name: str = '', phone: str = '', referer_id: int = None, referals_ids: list[int] = [], points: int = 0, **kwargs) -> None:
        super().__init__()
        self._payload['_id'] = _id
        self._payload['name'] = name
        self._payload['phone'] = phone
        self._payload['referer_id'] = referer_id
        self._payload['referals_ids'] = referals_ids
        self._payload['points'] = points

    @property
    def referer_id(self):
        return self._payload['referer_id']

    @referer_id.setter
    def referer_id(self, value):
        self._payload['referer_id'] = value
    
    @property
    def referals_ids(self):
        return self._payload['referals_ids']

    def add_referal(self, id):
        self._payload['referals_ids'].append(id)

    @property
    def id(self):
        return self._payload['_id']

    @property
    def name(self):
        return self._payload['name']

    @name.setter
    def name(self, value: str):
        self._payload['name'] = value
    
    @property
    def phone(self) -> str:
        return self._payload['phone']

    @phone.setter
    def phone(self, value: str):
        self._payload['phone'] = value
    
    @property
    def points(self):
        return self._payload['points']

    @points.setter
    def points(self, value: int):
        self._payload['points'] = value


class Payment(_Document):
    order_id: str
    payment_id: int
    payment_url: str
    id: int
    description: str
    amount: int
    date: datetime.datetime
    confirmed: bool
    rebill_id: int

    def __init__(self, *, _id: int, order_id: int = None, payment_id: int = None, payment_url: str = None, description: str = '',
                 amount: int = 0, date: int = 0, confirmed: bool = None, subscription: str = '', rebill_id: int = None, **kwargs) -> None:
        super().__init__()
        self._payload['id'] = _id
        self._payload['order_id'] = order_id
        self._payload['payment_id'] = payment_id
        self._payload['payment_url'] = payment_url
        self._payload['date'] = date
        self._date = datetime.datetime.fromtimestamp(date)
        self._payload['description'] = description
        self._payload['amount'] = amount
        self._payload['subscription'] = subscription
        self._payload['confirmed'] = confirmed
        self._payload['rebill_id'] = rebill_id

    @property
    def id(self):
        return self._payload['_id']
    
    @property
    def rebill_id(self):
        return self._payload['rebill_id']

    @property
    def order_id(self):
        return self._payload['order_id']

    @property
    def payment_id(self):
        return self._payload['payment_id']

    @property
    def payment_url(self):
        return self._payload['payment_url']

    @property
    def description(self):
        return self._payload['description']

    @property
    def amount(self):
        return self._payload['amount']

    @property
    def date(self):
        return self._date

    @property
    def confirmed(self):
        return self._payload['confirmed']
