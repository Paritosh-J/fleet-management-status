import mysql.connector as connector


class dataBase:
    def __init__(self):
        self.con = connector.connect(
            host='localhost', port='3306', user='root', password='', database='Fleet_System')

        q = 'CREATE TABLE IF NOT EXISTS FleetSystem(serialNum INT PRIMARY KEY, vehicleNum TEXT, features TEXT, entryType TEXT, entryTime TIME, parkingStat TEXT)'

        cur = self.con.cursor()
        cur.execute(q)
        print("Query executed successfully!")

    def insertDataBase(self, serialNum, vehicleNum, features, entryType, entryTime, parkingStat):
        query = "INSERT INTO FleetSystem(serialNum, vehicleNum, features, entryType, entryTime, parkingStat) VALUES({}, '{}', '{}', '{}', {}, '{}')".format(
            serialNum, vehicleNum, features, entryType, entryTime, parkingStat)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()
        print("Data entered into DB successfully!")

    def updateDataBase(self, vehicleNum, parkingStat):
        query = "UPDATE FleetSystem SET parkingStat='{}' WHERE vehicleNum={}".format(parkingStat, vehicleNum)
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()
        print("Data updated successfully!")
