from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_, select

from models.postgres import Holiday, RecipientHolidays


async def get_holidays_for_recipient(
    conn: AsyncSession, recipient_id: str
) -> ChunkedIteratorResult:
    return await conn.execute(
        select(Holiday)
        .join(RecipientHolidays, and_(RecipientHolidays.holiday_id == Holiday.id))
        .where(and_(RecipientHolidays.id == recipient_id, Holiday.active.is_(True)))
    )
