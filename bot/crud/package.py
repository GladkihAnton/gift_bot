from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, update

from models.postgres import Package


async def get_package_by_id(
    conn: AsyncSession, package_id: int
) -> ChunkedIteratorResult:
    return await conn.execute(
        select(Package.image, Package.file_id).where(Package.id == package_id)
    )


async def update_package_file_id(
    conn: AsyncSession, package_id: int, file_id: str
) -> ChunkedIteratorResult:
    return await conn.execute(
        update(Package).where(Package.id == package_id).values(file_id=file_id)
    )
