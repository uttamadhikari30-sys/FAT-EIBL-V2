from apscheduler.schedulers.background import BackgroundScheduler
from .reports import generate_weekly_report, send_due_reminders

sched = None

def start_scheduler():
    global sched
    if sched:
        return
    sched = BackgroundScheduler()
    sched.add_job(func=generate_weekly_report, trigger='cron', day_of_week='fri', hour=18, minute=0)
    sched.add_job(func=send_due_reminders, trigger='cron', hour=9, minute=0)
    sched.start()
