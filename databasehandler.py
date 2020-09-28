import sqlite3

#columns for the db (experimental): IP, User-Agent,referer,time,resource


#initilize the db, for now its all stored in memory
req = {"IP":"10.0.0.1",
       "UserAgent":"/*",
       "Referer":"/google.com",
       "Time":"10.23",
       "Resource":"/offers"
      }

req2 = {"IP":"10.0.0.2",
       "UserAgent":"/*",
       "Referer":"/google.com",
       "Time":"10.23",
       "Resource":"/offers"
      }


req3 = {"IP":"10.0.0.1",
       "UserAgent":"python",
       "Referer":"/google.com",
       "Time":"10.23",
       "Resource":"/offers"
      }
l= [req,req2,req3]

class DatabaseHandler:


    def create_table(self,table):#cant use palceholders for table and column names
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS {} (
                    Insertid text,
                    IP text,
                    UserAgent text,
                    Referer text,
                    Time text,
                    Resource text
                    )""".format(table))
        self.conn.commit()

    def __init__(self,name):
        self.conn = sqlite3.connect('req.db')
        self.cursor = self.conn.cursor()
        self.table_name = name
    
    def __enter__(self):
        return self        

    def __exit__(self,exception_type, exception_value, traceback):
        self.conn.commit()
        self.conn.close()

    #takes a request as a dict and stores it in the db
    def store(self,request):
        values = (request["Insertid"],request["IP"],request["UserAgent"],request["Referer"],request["Time"],request["Resource"])
        l = self.cursor.execute("SELECT * FROM {} WHERE Insertid=?".format(self.table_name),(request["Insertid"],)).fetchall()
        if len(l) > 0:
            return
        else:
            self.cursor.execute("INSERT INTO {} VALUES (?,?,?,?,?,?)".format(self.table_name),values)

    #takes an ip  and returns all the rows (requests) that came from that ip
    def read(self,ip):
        value = (ip,)
        l = self.cursor.execute("SELECT * FROM {} WHERE IP=?".format(self.table_name),value).fetchall()
        return l
    
    def clear_table(self):
        self.cursor.execute("DELETE FROM {}".format(self.table_name))
        self.conn.commit()
    
    
    def close_connection(self):
        self.conn.commit()
        self.conn.close()

    #prints all the rows in the table
    def print_table(self):
        self.cursor.execute("SELECT * FROM {}".format(self.table_name))
        l = self.cursor.fetchall()
        for req in l:
            print(req)
        print("There are {} rows in the {} table".format(str(len(l)),self.table_name))


if __name__ == "__main__":
    with DatabaseHandler('humans') as db:
       l = db.cursor.execute("SELECT * FROM humans").fetchall()
       ips = []
       for val in l:
            ips.append(val[1])
       unique = list(set(ips))
       print(len(unique))
