from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_, insert, select

from models.postgres import Gift, Holiday, Order, OrderStatus, Recipient, Sex


async def get_orders(conn: AsyncSession, username: str) -> ChunkedIteratorResult:
    return await conn.execute(
        select(
            Recipient.full_name,
            Holiday.name,
            Sex.name,
            OrderStatus.name,
            Order.delivered_at,
            Recipient.delivery_address,
            Recipient.contact_info,
        )
        .select_from(Order)
        .join(Recipient, and_(Recipient.id == Order.recipient_id))
        .join(Sex, and_(Sex.id == Recipient.sex_id))
        .join(OrderStatus, and_(OrderStatus.id == Order.status_id))
        .join(Holiday, and_(Holiday.id == Order.holiday_id))
        .join(Gift, and_(Gift.id == Order.gift_id))
        .where(Order.customer_id == username)
    )


async def create_order(conn: AsyncSession, **order_data) -> ChunkedIteratorResult:
    return await conn.execute(insert(Order).values(**order_data))
