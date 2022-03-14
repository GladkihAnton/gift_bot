from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .meta import Base

customer_recipients = Table(
    'customer_recipients',
    Base.metadata,
    Column('customer_id', ForeignKey('customer.username'), primary_key=True),
    Column('recipient_id', ForeignKey('recipient.id'), primary_key=True),
)


class Customer(Base):
    __tablename__ = 'customer'

    username: Column = Column(String(256), primary_key=True, index=True)
    password: Column = Column(String(128), nullable=False)

    account_status: Column = Column(String(128))

    chat_id: Column = Column(Integer)
    recipients = relationship(
        "Recipient", secondary=customer_recipients, backref="customers"
    )


class Recipient(Base):
    __tablename__ = 'recipient'
    id: Column = Column(Integer, primary_key=True, index=True)

    full_name: Column = Column(String(256))

    company_name: Column = Column(String(256))
    position: Column = Column(String(256))

    delivery_address: Column = Column(String(256))
    contact_info: Column = Column(String(256))

    sex_id: Column = Column(Integer, ForeignKey('sex.id'))


class RecipientHobbies(Base):
    __tablename__ = 'recipient_hobbies'

    id: Column = Column(Integer, primary_key=True, index=True)

    recipient_id: Column = Column(Integer, ForeignKey('recipient.id'))
    hobby_id: Column = Column(Integer, ForeignKey('hobby.id'))


class RecipientHolidays(Base):
    __tablename__ = 'recipient_holidays'

    id: Column = Column(Integer, primary_key=True, index=True)

    recipient_id: Column = Column(Integer, ForeignKey('recipient.id'))
    holiday_id: Column = Column(Integer, ForeignKey('holiday.id'))


class Hobby(Base):
    __tablename__ = 'hobby'

    id: Column = Column(Integer, primary_key=True, index=True)

    name: Column = Column(String(256))


class Holiday(Base):
    __tablename__ = 'holiday'

    id: Column = Column(Integer, primary_key=True, index=True)

    name = Column(String(256))
    active: Column = Column(Boolean, default=True)

    def to_dict(self):
        return {'id': self.id, 'name': self.name}


class Sex(Base):
    __tablename__ = 'sex'

    id: Column = Column(Integer, primary_key=True, index=True)

    name: Column = Column(String(256))


class Gift(Base):
    __tablename__ = 'gift'

    id: Column = Column(Integer, primary_key=True, index=True)

    name: Column = Column(String(256))
    description: Column = Column(String(256))
    price: Column = Column(Float)
    link: Column = Column(String(256))

    coolness = Column(Integer)

    image: Column = Column(String(100))
    file_id: Column = Column(String(256))

    package_id: Column = Column(Integer, ForeignKey('package.id'))
    type_id: Column = Column(Integer, ForeignKey('gift_type.id'))
    sex_id: Column = Column(Integer, ForeignKey('sex.id'))


class GiftType(Base):
    __tablename__ = 'gift_type'

    id: Column = Column(Integer, primary_key=True, index=True)

    name: Column = Column(String(256))


class Package(Base):
    __tablename__ = 'package'

    id: Column = Column(Integer, primary_key=True, index=True)

    name: Column = Column(String(256))
    image: Column = Column(String(100))
    file_id: Column = Column(String(256))


class GiftHobbies(Base):
    __tablename__ = 'gift_hobbies'
    id: Column = Column(Integer, primary_key=True, index=True)

    gift_id = Column(Integer, ForeignKey('gift.id'))
    hobby_id = Column(Integer, ForeignKey('hobby.id'))


class SuggestedGift(Base):
    __tablename__ = 'suggested_gift'

    id: Column = Column(Integer, primary_key=True, index=True)

    customer_id: Column = Column(
        String(256), ForeignKey('customer.username'), nullable=False
    )
    gift_id: Column = Column(Integer, ForeignKey('gift.id'), nullable=False)
    recipient_id: Column = Column(Integer, ForeignKey('recipient.id'), nullable=False)

    checked: Column = Column(Boolean, default=True)
    presented: Column = Column(Boolean, default=False)


class OrderStatus(Base):
    __tablename__ = 'order_status'

    id: Column = Column(Integer, primary_key=True, index=True)

    name: Column = Column(String(256), nullable=False)


class Comment(Base):
    __tablename__ = 'comment'

    id: Column = Column(Integer, primary_key=True, index=True)

    customer_id = Column(String(256), ForeignKey('customer.name'))
    recipient_id = Column(Integer, ForeignKey('recipient.id'))
    comment: Column = Column(String(256))
    voice: Column = Column(String(256))


class Order(Base):
    __tablename__ = 'order'

    id: Column = Column(Integer, primary_key=True, index=True)

    customer_id: Column = Column(
        String(256), ForeignKey('customer.username'), nullable=False
    )
    gift_id: Column = Column(Integer, ForeignKey('gift.id'), nullable=False)
    recipient_id: Column = Column(Integer, ForeignKey('recipient.id'), nullable=False)
    holiday_id: Column = Column(Integer, ForeignKey('holiday.id'))

    status_id = Column(Integer, ForeignKey('status.id'))
    package_id = Column(Integer, ForeignKey('package.id'), nullable=True)
    delivered_at = Column(Date, nullable=True)
