from database import get_connection

connection = get_connection()   # 如果連線失敗，這裡會拋出例外，就不會進入try

try:
    print("MySQL 連線成功!")

finally:
    connection.close()
