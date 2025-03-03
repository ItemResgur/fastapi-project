import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('greetings.db')
cursor = conn.cursor()

# Выполнение запроса на удаление всех записей
cursor.execute("DELETE FROM greetings")

# Сохранение изменений
conn.commit()

# Закрытие соединения
conn.close()

print("All records have been deleted.")
