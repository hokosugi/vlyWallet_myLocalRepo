from apscheduler.schedulers.background import BackgroundScheduler
from models import User
import logging

logger = logging.getLogger(__name__)

def run_update_transactions():
    from update_transactions import update_transactions
    from app import create_app
    app=create_app()
    logging.info("Updating transaction data...") 
    with app.app_context():  # アプリケーションコンテキストを設定
        update_transactions()
    logging.info("Transaction data updated successfully.")

def start_scheduler(run_update_transactions):
    scheduler = BackgroundScheduler()
    try:
        scheduler.add_job(run_update_transactions, 
                        trigger="interval", 
                        hours=1,
                        id='update_transactions_job',
                        name='Update transaction data everyday')
        scheduler.start()

        if not scheduler.running:
                scheduler.start()
                logger.info("Scheduler started successfully")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")


if __name__ == "__main__":
    from app import create_app
    app=create_app()
    start_scheduler(run_update_transactions)  # スケジューラーを開始
    print("Scheduler started. Waiting for jobs...")
    while True:  # スクリプトが終了しないように無限ループ
            pass