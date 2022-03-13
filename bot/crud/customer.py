from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_, select

from models.postgres import Customer, Holiday, Order, Recipient, RecipientHolidays


async def get_customer(conn: AsyncSession, username: str) -> ChunkedIteratorResult:
    return await conn.execute(select(Customer).where(Customer.username == username))


async def get_recipients_for_customer(
    conn: AsyncSession, username: str
) -> ChunkedIteratorResult:
    return await conn.execute(
        select(Recipient, Holiday)
        .join(Customer.recipients)
        .join(RecipientHolidays, and_(Recipient.id == RecipientHolidays.recipient_id))
        .join(Holiday, and_(Holiday.id == RecipientHolidays.holiday_id))
        .join(
            Order,
            and_(
                Order.customer_id == username,
                Order.recipient_id == Recipient.id,
                Order.holiday_id == RecipientHolidays.holiday_id,
            ),
            isouter=True,
        )
        .where(and_(Customer.username == username, Order.id.is_(None)))
    )
