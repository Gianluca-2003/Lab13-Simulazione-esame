from database.DB_connect import DBConnect
from model.driver import Driver


class DAO():
    def __init__(self):
        pass



    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)


        res = []
        query = """SELECT s.`year`
                    FROM seasons s """


        cursor.execute(query)
        for row in cursor:
            res.append(row['year'])

        cursor.close()
        cnx.close()
        return res




    @staticmethod
    def getAllNodes(anno):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)


        res = []
        query = """SELECT DISTINCT d.*
            FROM  results r , drivers d , races r2 
            WHERE r.`position`>= 1 and d.driverId = r.driverId
            and YEAR(r2.Date) = %s and r2.raceId = r.raceId"""


        cursor.execute(query,(anno,))
        for row in cursor:
            res.append(Driver(**row))

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def getAllEdges(anno,idMap):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)


        res = []
        query = """SELECT r1.driverId AS vincente, r2.driverId AS sconfitto, COUNT(*) AS peso
                FROM races ra
                JOIN results r1 ON ra.raceId = r1.raceId
                JOIN results r2 ON ra.raceId = r2.raceId
                WHERE YEAR(ra.date) = %s
                  AND r1.position >= 1
                  AND r2.position >= 1
                  AND r1.position < r2.position
                  AND r1.driverId <> r2.driverId
                GROUP BY r1.driverId, r2.driverId"""


        cursor.execute(query,(anno,))
        for row in cursor:
            res.append((idMap[row['vincente']], idMap[row['sconfitto']], row['peso']))

        cursor.close()
        cnx.close()
        return res

