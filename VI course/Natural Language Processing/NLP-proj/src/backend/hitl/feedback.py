"""Сейв обратной связи от редактора на протяжении всего процесса проверки с участием человека (HITL)"""

from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.hitl.active_learning import ActiveLearningHandler


async def save_feedback(session: AsyncSession, example_id: int, corrected_text: str):
    """Сейв обратной связи"""

    if not corrected_text.strip():
        raise ValueError(
            "Correction cannot be blank"
        )

    return await ActiveLearningHandler.review_example(
        session,
        example_id,
        approve=True,
        corrected_text=corrected_text
    )
