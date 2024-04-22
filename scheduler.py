from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from data_collector import form_dataset, upload_dataframe_to_database


def form_and_upload_dataframe_job():
    '''
    Задача для планировщика по формированию датасета
    и загрузке его в базу данных.
    '''
    print(f"Executing function at: {datetime.now()}")
    upload_dataframe_to_database(form_dataset())


# Создаем планировщик задач
scheduler = BackgroundScheduler()
scheduler.add_job(form_and_upload_dataframe_job, 'interval', minutes=10)

# Запускаем планировщик
scheduler.start()


def shutdown_scheduler():
    '''
    Остановить работу планировщика задач.
    '''
    scheduler.shutdown()
