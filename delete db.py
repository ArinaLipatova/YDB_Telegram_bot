import ydb

# Установить соединение с базой данных
driver_config = ydb.DriverConfig(
    endpoint='grpcs://ydb.serverless.yandexcloud.net:****/?database=/ru-central1/***********/***********',  # эндпоинт
    database='/ru-central1/****************************',  # путь к базе данных
    credentials=ydb.construct_credentials_from_environ(),
)

with ydb.Driver(driver_config) as driver:
    driver.wait(timeout=5)

    session = driver.table_client.session().create()

    # Выполнение команды DELETE через YDB SDK
    query = "DELETE FROM Users;"
    session.transaction(ydb.SerializableReadWrite()).execute(
        query,
        commit_tx=True,
    )

    print("All rows deleted from Users table.")

