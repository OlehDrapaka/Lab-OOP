from abc import ABC, abstractmethod

class Report:
    def forming(self):
        return "Звіт"

class ReportSaver:
    def save_to_file(self, report):
        print(f"Збережено: {report}")

class Data:
    def save_data_abonement(self, data):
        print(f"Збережено: {data}")


class Abonement:
    def __init__(self, name, phone, balance):
        self.name = name
        self.phone = phone
        self.balance = balance

class Massage:
    def send_massage(self, sms):
        print("send sms", {sms})

class Balance:
    def calculate_balance(self,abonement_balance, cost):
        self.abonement_balance = abonement_balance
        abonement_balance -= cost
        print(f"Новий баланс: {abonement_balance}")

class Tariff:
    def price(self, minutes):
        return 0

class BasicTariff(Tariff):
    def price(self, minutes):
        return minutes *1

class NewTariff(Tariff):
    def price(self, minutes):
        return minutes *0.5

class VoiceTariff(Tariff):
    def calculate(self, minutes):
        return minutes * 0.6

class DataTariff(Tariff):
    def calculate(self, minutes):
        return minutes * 0.1

class RoamingTariff(Tariff):
    def calculate(self, minutes):
        return minutes * 5

class NetworkConnection:
    pass

class LTEConnection(NetworkConnection):
    def connect(self):
        print("LTE підключено")

class WiFiConnection(NetworkConnection):
    def connect(self):
        print("WiFi підключено")

class SatelliteConnection:
    def connect(self):
        print("Супутник не може працювати, як звичайне з'єднання")


class ICall:
    def make_call(self):
        pass

class ISMS:
    def send_sms(self):
        pass

class IConnect:
    def connect_to_network(self):
        pass

class IData:
    def send_data(self):
        pass

class TelecomDevice(ICall, ISMS, IConnect):
    def make_call(self):
        print("дзвінок")

    def send_sms(self):
        print("відправляємо повідомлення")

    def connect_to_network(self):
        print("триває підключення")

class IoT(IConnect, IData):
    def connect_to_network(self):
        print("підключення")

    def send_data(self):
        print("відправлення даних")

class ILogger(ABC):
    @abstractmethod

    def log(self, message: str):
        pass

class FileLogger(ILogger):
    def log(self, message: str):
        print(f"Запис у файл: {message}")

class ServerLogger(ILogger):
    def log(self, message: str):
        print(f"Відправка на сервер моніторингу: {message}")

class ConsoleLogger(ILogger):
    def log(self, message: str):
        print(f"Вивід у консоль: {message}")

class NetworkMonitor:
    def __init__(self, logger: ILogger):
        self.logger = logger

    def check_connection(self, status: bool):
        if not status:
            self.logger.log("Помилка: З'єднання розірвано!")
        else:
            self.logger.log("Мережа стабільна.")