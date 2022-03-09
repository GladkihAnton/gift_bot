from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import insert

from models.postgres import Comment


async def create_comment(conn: AsyncSession, **comment_data) -> ChunkedIteratorResult:
    return await conn.execute(insert(Comment).values(**comment_data))
