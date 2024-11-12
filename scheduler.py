from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def start_scheduler(update_func):
    scheduler.add_job(func=update_func, 
                     trigger="interval", 
                     weeks=1,
                     id='update_transactions_job',
                     name='Update transaction data weekly')
    scheduler.start()
