"""Этап 14: логика очереди, утверждения и истечения срока действия кэша"""
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock
import pytest
from src.backend.hitl import CacheHandler, ActiveLearningHandler
from src.backend.db import UncertainExample, KnowledgeBase


@pytest.mark.asyncio
async def test_queue_only_uncertain():
    session = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    assert await ActiveLearningHandler.enqueue_if_uncertain(session, input_text="x", model_output="y", critic_score=.9) is None
    session.add.assert_not_called()
    item = await ActiveLearningHandler.enqueue_if_uncertain(session, input_text="x", model_output="y", critic_score=.2)
    assert isinstance(item, UncertainExample)
    assert item.status == "pending"
    session.add.assert_called_once()


@pytest.mark.asyncio
async def test_approve_adds_knowledge():
    item = UncertainExample(internal_id=1, input_text="profile", model_output="draft", status="pending")
    session = MagicMock()
    session.get = AsyncMock(return_value=item)
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    updated, kb = await ActiveLearningHandler.review_example(session, 1, approve=True, corrected_text="corrected")
    assert updated.status == "approved"
    assert isinstance(kb, KnowledgeBase)
    assert kb.target_text == "corrected"


@pytest.mark.asyncio
async def test_reject_does_not_add_knowledge():
    item = UncertainExample(internal_id=2, input_text="profile", model_output="draft", status="pending")
    session = MagicMock()
    session.get = AsyncMock(return_value=item)
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    updated, kb = await ActiveLearningHandler.review_example(session, 2, approve=False)
    assert updated.status == "rejected"
    assert kb is None
    session.add.assert_not_called()


@pytest.mark.asyncio
async def test_repeated_review_is_rejected():
    session = MagicMock()
    session.get = AsyncMock(return_value=UncertainExample(status="approved", input_text="a", model_output="b"))
    with pytest.raises(ValueError, match="already"):
        await ActiveLearningHandler.review_example(session, 1, approve=True)


def test_cache_ttl():
    now = datetime.now(timezone.utc)
    assert CacheHandler.is_expired(now - timedelta(hours=25), now=now)
    assert not CacheHandler.is_expired(now - timedelta(hours=2), now=now)


@pytest.mark.asyncio
async def test_cache_hit_increments_counter():
    from src.backend.db import Cache
    row = Cache(input_key="k", output="summary", hits=3, load_date=datetime.now(timezone.utc))
    session = MagicMock()
    session.scalar = AsyncMock(return_value=row)
    session.commit = AsyncMock()
    assert await CacheHandler.get_cached(session, "k") == "summary"
    assert row.hits == 4
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_expired_cache_is_deleted():
    from src.backend.db import Cache
    row = Cache(input_key="k", output="stale", hits=3, load_date=datetime.now(timezone.utc) - timedelta(days=3))
    session = MagicMock()
    session.scalar = AsyncMock(return_value=row)
    session.commit = AsyncMock()
    session.delete = AsyncMock()
    assert await CacheHandler.get_cached(session, "k") is None
    session.delete.assert_awaited_once_with(row)
