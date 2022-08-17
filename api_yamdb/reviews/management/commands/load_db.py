from csv import DictReader
from django.core.management import BaseCommand

 
from reviews.models import Genre


class Command(BaseCommand):
    help = "Загрузка данных из CSV файлов"

    def handle(self, *args, **options):
    
        # Сообщение о пристуствии такой строки в БД
        #if User.objects.exists():
        #    print('Строка уже загружена')
        #    return

        # Сообщение о начале загрузки
        print("Начало загрузки")

        # Основной кодя для импорта
        for row in DictReader(open('./genre.csv')):
            genre = Genre(id=row['id'], name=row['name'], slug=row['slug'])
            genre.save()
