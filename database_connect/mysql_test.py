from mysql_connector import MySQLConnector


if __name__ == '__main__':
    mysql_connector = MySQLConnector()
    print(mysql_connector)
    mysq_connector2 = MySQLConnector()
    print(mysq_connector2)
    print(mysql_connector)
    mysq_connector3 = MySQLConnector()
    print(mysq_connector3)
    with MySQLConnector() as mc:
        print(mc)
    mysq_connector4 = MySQLConnector()
    print(mysq_connector4)
