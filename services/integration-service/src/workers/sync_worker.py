import asyncio
import logging
from src.services.sync_service import SyncService
from src.config.database import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_sync_worker():
    """
    Background worker that triggers sync periodically.
    """
    logger.info("Sync worker started")
    while True:
        try:
            db = SessionLocal()
            sync_service = SyncService(db)
            logger.info("Starting global sync...")
            await sync_service.sync_all()
            logger.info("Global sync completed successfully")
        except Exception as e:
            logger.error(f"Sync failed: {str(e)}")
        finally:
            db.close()
        
        # Sync every 10 minutes
        await asyncio.sleep(600)

if __name__ == "__main__":
    asyncio.run(run_sync_worker())
