from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from models.postgres import Recipient


async def get_recipient_by_id(
    conn: AsyncSession, recipient_id: int
) -> ChunkedIteratorResult:
    return await conn.execute(
        select(Recipient).select_from(Recipient).where(Recipient.id == recipient_id)
    )
