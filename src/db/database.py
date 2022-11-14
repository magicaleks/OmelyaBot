import datetime
from .base import _db
from .models import Day, User, Booking, PaymentTypes
from typing import Optional

class Database:
    def __init__(self, _db) -> None:
        self._db = _db

    async def create_user(self, id: int) -> User:
        user = User(_id=id)
        await self._db.users.insert_one(user.get_payload())
        return user
    
    async def get_user(self, id: int) -> Optional[User]:
        res = await self._db.users.find_one({'_id': id})
        return User(**res) if res else None
    
    async def update_user(self, user: User):
        await self._db.users.replace_one({'_id': user.id}, user.get_payload())
    
    async def delete_user(self, id: int):
        await self._db.users.delete_one({'_id': id})
    
    async def get_users(self) -> list[User]:
        res = []
        async for u in self._db.users.find():
            res.append(User(**u))
        return res
    
    async def create_day(self, *, date: str = None, timestamp: int = None) -> Day:
        day = None
        if date:
            day = Day(_id=date)
        else:
            _date = datetime.datetime.fromtimestamp(timestamp)
            day = Day(_id=_date.strftime('%d/%m/%Y'), timestamp=timestamp)
        await self._db.days.insert_one(day.get_payload())
        return day
    
    async def book(self, service: str, service_num: int, day: str, time: int, user: int, payment_type: PaymentTypes) -> Booking:
        b = Booking(_id=f'{day}@{time}@{service_num}', user=user, payment_type=payment_type, confirmed=False, massage=service)
        await self._db.bookings.insert_one(b.get_payload())
        await self._db.days.update_one({'_id': day}, {'$set': {f'booked.{service}.{time}': b.id}})
        return b
    
    async def get_days(self, amount: int) -> list[Day]:
        now = datetime.datetime.now(tz=datetime.timezone(
            datetime.timedelta(
                hours=3
            )
        ))

        _start_date = datetime.datetime(
            now.year,
            now.month,
            now.day,
            tzinfo=now.tzinfo
        ).timestamp()

        _end_date = _start_date + datetime.timedelta(days=amount).total_seconds()

        days = []
        async for d in self._db.days.find({'$and': [
            {
                'timestamp': {'$gte': _start_date}
            },
            {
                'timestamp': {'$lte': _end_date}
            }
        ]}):
            days.append(Day(**d))

        if len(days) < amount:
            for i in range(len(days)+1, amount+1):
                day = await self.create_day(timestamp=_start_date+i*86400)
                days.append(day)
                
        return days
    
    async def get_day(self, date: str) -> Day:
        res = await self._db.days.find_one({'_id': date})
        return Day(**res) if res else None
    
    async def get_booking(self, id: str) -> Booking:
        res = await self._db.bookings.find_one({'_id': id})
        return Booking(**res) if res else None
    
    async def confirm_booking(self, id: str) -> None:
        await self._db.bookings.update_one({'_id': id}, {'$set': {'confirmed': True}})
    
    async def cancel_booking(self, id: str) -> None:
        res = await self._db.bookings.find_one_and_delete({'_id': id})
        b = Booking(**res)
        await self._db.days.update_one({'_id': id.split('@')[0]}, {'$set': {f"booked.{b.massage}.{id.split('@')[1]}": None}})
    
    async def get_user_bookings(self, user: int) -> list[Booking]:
        res = []
        async for b in self._db.bookings.find({'user': user}):
            res.append(Booking(**b))
        return res


db = Database(_db)
