# приложение собирает статистику с рекламного кабинета Yandex direct за последние 30 дней и сохраняет в файл report.tsv
"""Токен для приложения Yandex_direct_api
https://ya.ru/#access_token=y0_AgAAAABRzx-eAAx-iAAAAAESFadrAACvJsMMAxFKG7ktyCnZ4FkX9gWbnQ&token_type=bearer&expires_in=31535176&cid=zbvvxaf0m4kfwkmqkuevkrxee4"""

import json  # импортируем модули запросов и работы с JSON
import time  # для задержки запросов

import requests  # для обращения к API
from const import TOKEN, REPORTS_URL, CLIENT_LOGIN  # для импорта констант
from requests.exceptions import ConnectionError  # для обработки исключений
from storage import Storage, FileStorage, PandasStorage
from timing import timing  # для подсчета времени
from yandex_helper import get_headers, get_body


@timing
def get_report(start_date: str, end_date: str) -> str:
    #  Заголовки http-запроса
    headers = get_headers(TOKEN, CLIENT_LOGIN)
    # Тело запроса
    body = get_body(start_date, end_date)

    # Кодирование тела запроса в JSON
    body = json.dumps(body, indent=4)

    # Цикл выполнения запросов
    while True:
        try:
            request = requests.post(REPORTS_URL, body, headers=headers)
            request.encoding = 'utf-8'  # Принудительная обработка ответа в кодировке UTF-8
            # 400 = параметры запроса указаны неверно или достигнут лимит отчетов в очереди
            if request.status_code == 400:
                print("Параметры запроса указаны неверно или достигнут лимит отчетов в очереди")
                break
            # 200 = выводится содержание отчета
            elif request.status_code == 200:
                print("Отчет создан успешно")

                return request.text
            # 201 = выполняются повторные запросы, поставлен в очередь
            elif request.status_code == 201:
                print("Отчет успешно поставлен в очередь в режиме офлайн")
                retry_in = int(request.headers.get("retryIn", 60))
                print(f"Повторная отправка запроса через {retry_in} секунд")
                time.sleep(retry_in)
            # 202 = выполняются повторные запросы
            elif request.status_code == 202:
                print("Отчет формируется в режиме офлайн")
                retry_in = int(request.headers.get("retryIn", 60))
                print(f"Повторная отправка запроса через {retry_in} секунд")
                time.sleep(retry_in)
            elif request.status_code == 500:
                print("При формировании отчета произошла ошибка. Пожалуйста, попробуйте повторить запрос позднее")
                break
            # 502 = время формирования отчета превысило серверное ограничение
            elif request.status_code == 502:
                print("Время формирования отчета превысило серверное ограничение.")
                print(
                    "Пожалуйста, попробуйте изменить параметры запроса - уменьшить период и количество запрашиваемых данных.")
                break
            else:
                print("Произошла непредвиденная ошибка")
                break
        except ConnectionError:
            print("Произошла ошибка соединения с API Яндекса. Пожалуйста, попробуйте повторить запрос позднее")
            break

        except Exception as e:
            print(f"Произошла непредвиденная ошибка. {e}")
            break


# функция для получения статистики
def work(saver: Storage):
    """ функция для получения статистики и сохранения в файл"""

    report_dates = [("2024-01-01", "2024-01-31"), ("2024-02-01", "2024-02-28"), ("2024-03-01", "2024-03-31"), ]
    for dates in report_dates:
        date_start, date_end = dates
        report = get_report(date_start, date_end)
        saver.save_report(report, date_start, date_end)


if __name__ == "__main__":
    """Запуск программы"""
    try:
        storage = PandasStorage()
        # storage = FileStorage()
        # storage = MemoryStorage()
        work(storage)
    except Exception as e:
        print(e)
