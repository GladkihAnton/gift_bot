from typing import Optional, Tuple

from db import async_db_connection
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_, insert, or_, select, update

from models.postgres import (
    Gift,
    GiftHobbies,
    GiftType,
    Recipient,
    RecipientHobbies,
    Sex,
    SuggestedGift,
)


async def get_gifts_for_recipient(
    conn: AsyncSession, recipient_id: int, username: str
) -> ChunkedIteratorResult:
    return await conn.execute(
        select(Gift, Sex.name, GiftType.name)
        .select_from(Recipient)
        .join(RecipientHobbies, and_(Recipient.id == RecipientHobbies.recipient_id))
        .join(GiftHobbies, and_(GiftHobbies.hobby_id == RecipientHobbies.hobby_id))
        .join(Gift, and_(GiftHobbies.gift_id == Gift.id))
        .join(Sex, and_(Gift.sex_id == Sex.id))
        .join(GiftType, and_(Gift.type_id == GiftType.id))
        .join(
            SuggestedGift,
            and_(
                SuggestedGift.recipient_id == Recipient.id,
                SuggestedGift.gift_id == Gift.id,
                or_(
                    SuggestedGift.customer_id == username,
                    SuggestedGift.presented.is_(True),
                ),
            ),
            isouter=True,
        )
        .where(and_(Recipient.id == recipient_id), SuggestedGift.checked.isnot(True))
        .limit(1)
    )


async def get_and_update_gift(
    username: str, recipient_id: int
) -> Tuple[Optional[Gift], Optional[str], Optional[str]]:
    async with async_db_connection() as conn:
        try:
            (gift, sex, gift_type) = (
                await get_gifts_for_recipient(conn, recipient_id, username)
            ).one()
        except NoResultFound:
            return None, None, None

        await conn.execute(
            insert(SuggestedGift).values(
                customer_id=username, recipient_id=recipient_id, gift_id=gift.id
            )
        )

        await conn.commit()

        return gift, sex, gift_type


async def update_suggested_gift(
    conn: AsyncSession, username: str, recipient_id: int, gift_id: int
) -> None:
    return await conn.execute(
        update(SuggestedGift)
        .where(
            and_(
                SuggestedGift.gift_id == gift_id,
                SuggestedGift.recipient_id == recipient_id,
                SuggestedGift.customer_id == username,
            )
        )
        .values(presented=True)
    )


async def update_gift_file_id(
    conn: AsyncSession, gift_id: int, file_id: str
) -> ChunkedIteratorResult:
    return await conn.execute(
        update(Gift).where(Gift.id == gift_id).values(file_id=file_id)
    )
