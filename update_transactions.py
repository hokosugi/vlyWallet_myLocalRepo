from models import db, User, Transaction
from datetime import datetime
import logging
from app import create_app
from models import User
from vly_wallet_api import main as get_vly_transactions

logger = logging.getLogger(__name__)


def update_transactions():
    """
    Update transaction data for all users based on the results from vly_api_like_tx.py
    """
    
    users = User.query.all()
    current_time = datetime.utcnow()

    # Get all vly_user_ids
    vly_user_ids = [user.vly_user_id for user in users]

    # Get transaction counts for all users
    try:
        tx_counts = get_vly_transactions(vly_user_ids)
    except Exception as e:
        logger.error(f"Error fetching transaction data: {str(e)}")
        return

    for user in users:
        try:
            if user.vly_user_id not in tx_counts:
                logger.warning(
                    f"No transaction data for vly_user_id: {user.vly_user_id}")
                continue

            tx_count = tx_counts[user.vly_user_id]
            if tx_count is None:
                logger.warning(
                    f"Failed to get transaction count for vly_user_id: {user.vly_user_id}"
                )
                continue

            # Update or create transaction record
            transaction = Transaction.query.filter_by(
                vly_user_id=user.vly_user_id).first()
            if not transaction:
                transaction = Transaction(vly_user_id=user.vly_user_id)
                db.session.add(transaction)

            # Update transaction count
            transaction.tx_count = tx_count

            # Update last updated timestamp
            transaction.last_updated = current_time

            # Update weekly streak (you may want to implement the logic for this)
            # transaction.update_weekly_streak()

            logger.info(
                f"Updated transactions for vly_user_id {user.vly_user_id}: count = {tx_count}"
            )

        except Exception as e:
            logger.error(
                f"Error updating transactions for vly_user_id {user.vly_user_id}: {str(e)}"
            )
            db.session.rollback()
            continue

    # Commit all changes
    try:
        db.session.commit()
        logger.info("Successfully committed all transaction updates")
    except Exception as e:
        logger.error(f"Error committing transaction updates: {str(e)}")
        db.session.rollback()


if __name__ == "__main__":
    app = create_app()  # アプリケーションを作成
    with app.app_context(): 
        update_transactions()
