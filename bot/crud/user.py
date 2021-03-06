from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_, select

from models.postgres import User, Holiday, Order, Recipient, RecipientHolidays


async def get_user(conn: AsyncSession, username: str) -> ChunkedIteratorResult:
    return await conn.execute(select(User).where(User.username == username))


async def get_recipients_for_customer(
    conn: AsyncSession, username: str
) -> ChunkedIteratorResult:
    return await conn.execute(
        select(Recipient, Holiday)
        .join(User.recipients)
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
        .where(and_(User.username == username, Order.id.is_(None)))
    )
