import psycopg2

try:
    # 建立数据库连接
    connection = psycopg2.connect(
        user="postgres",
        password="123456",
        host="localhost",
        port="5432",
        database="test"
    )

    # 创建一个游标对象
    cursor = connection.cursor()

    # 执行 SQL 查询
    cursor.execute("SELECT version();")

    # 获取查询结果
    record = cursor.fetchone()
    print("You are connected to - ", record)

    """创建表
    
    """
    # 创建表的 SQL 语句
    create_table_query = '''CREATE TABLE employees
                              (id INT PRIMARY KEY     NOT NULL,
                              name           TEXT    NOT NULL,
                              age            INT     NOT NULL,
                              salary         REAL); '''

    # 执行创建表的 SQL 语句
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")


    """插入数据
    """

    # 插入数据的 SQL 语句
    insert_query = "INSERT INTO employees (id, name, age, salary) VALUES (%s, %s, %s, %s)"
    record_to_insert = (1, 'John Doe', 30, 5000.00)

    # 执行插入数据的 SQL 语句
    cursor.execute(insert_query, record_to_insert)
    connection.commit()
    print("Record inserted successfully into employees table")


    """
    查询数据"""

    # 查询数据的 SQL 语句
    select_query = "SELECT * FROM employees"
    cursor.execute(select_query)

    # 获取所有查询结果
    records = cursor.fetchall()
    print("Total number of rows in employees table: ", cursor.rowcount)

    print("\nPrinting each employee record")
    for row in records:
        print("Id = ", row[0], )
        print("Name = ", row[1])
        print("Age = ", row[2])
        print("Salary = ", row[3], "\n")




except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # 关闭游标和连接
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")