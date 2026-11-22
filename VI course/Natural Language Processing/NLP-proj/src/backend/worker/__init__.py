from .celery_app import celery_app
from .tasks import compare_models_task, evaluate_model_task, reindex_knowledge_base_task, cleanup_cache_task, generate_batch_task