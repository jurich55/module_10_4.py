from random import randint
from threading import Thread
from time import sleep
from queue import Queue


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        sleep(randint(3, 10))


class Cafe:
    list_thr = []

    def __init__(self, *tables):
        self.queue = Queue()       # - очередь (объект класса Queue)
        self.tables = list(tables)

    def guest_arrival(self, *guests):       # прибытие гостей
        len_list_guests = len(list(guests))
        min_guests_tables = min(len_list_guests, len(self.tables))
        for i in range(min_guests_tables):
            self.tables[i].guest = guests[i]
            thr1 = guests[i]
            thr1.start()
            Cafe.list_thr.append(thr1)
            print(f'{list(guests)[i].name} сел(-а) за стол номер {self.tables[i].number}')
        if len_list_guests > min_guests_tables:
            for i in range(min_guests_tables, len_list_guests):
                self.queue.put(guests[i])      # добавление в очередь
                print(f'{list(guests)[i].name} в очереди')

    def discuss_guests(self):                   # - обслуживание гостей
        while not (self.queue.empty()) or Cafe.check_table(self):
            for table in self.tables:
                if not (table.guest is None) and not (table.guest.is_alive()):
                    print(f'{table.guest.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер {table.number} свободен')
                    table.guest = None          # стол  освободился
                if (not (self.queue.empty())) and table.guest is None:
                    table.guest = self.queue.get()     # гость занимает стол №
                    print(f'{table.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}')
                    thr1 = table.guest
                    thr1.start()                # старт потока этого гостя
                    Cafe.list_thr.append(thr1)

    def check_table(self):
        for table in self.tables:
            if table.guest is not None:
                return True
        return False


tables = [Table(number) for number in range(1, 6)]

guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

guests = [Guest(name) for name in guests_names]

cafe = Cafe(*tables)
                      # Приём гостей
cafe.guest_arrival(*guests)
                       # Обслуживание гостей
cafe.discuss_guests()
for thr in Cafe.list_thr:
    thr.join()
