import json
import pprint
import re
from databasehandler import DatabaseHandler 
#import check_user_agent as checker
from analyzer import real_useragent

#Takes in a list of request after they have been formated by "_format_requests(req)" and removes bots
def remove_bot_req(req):
    new_list = []
    for r in req: 
        if(real_useragent(r['UserAgent'])):
            new_list.append(r)
        #else:
            #print(r['UserAgent'])
    return new_list

def _read_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data


def _format_time(timestamp):
    val = re.split('T|Z',timestamp)
    print(val)

#takes in a list of tuples (httprequest,timestamp) where httprequest is a dict.
#returns a dict in the format the store function in the database needs it
def _format_requests(reqs):
    requests = []
    for req in reqs:
        try:
            formated = {"IP":req[0]['remoteIp'],
                        "UserAgent":req[0]['userAgent'],
                        "Referer":req[0]['referer'],
                        "Time":req[1],
                        "Resource":req[0]["requestUrl"],
                        "Insertid":req[2]
                       }
        except KeyError:
            formated = {"IP":req[0]['remoteIp'],
                        "UserAgent":"empty",
                        "Referer":req[0]['referer'],
                        "Time":req[1],
                        "Resource":req[0]["requestUrl"],
                        "Insertid":req[2]
                       }
        requests.append(formated)
    return requests

#takes in a json file with our logs and extracts the httprequest and timestamp for each entry
#returns 2 lists: first is a list of the unique ips and the second is a list  of tuples of type (httprequest,timestamp) where httprequest is a dict
def _extract_http_and_time(filename='humans.json'):
    data = _read_json(filename)
    reqs = []
    ips = []
    #pprint.pprint(data)
    for i in range (0,len(data)-1):
        try:
            req = data[i]['httpRequest']
            timestamp = data[i]['timestamp']
            insertid = data[i]['insertId']
            ip = data[i]['httpRequest']['remoteIp']
            ips.append(ip)
            reqs.append((req,timestamp,insertid))
        except KeyError as e:
            print("httpRequest is probably missing in the json log at i={}".format(i))
            pass
    return list(set(ips)),reqs

#takes in the json file with the logs and stores them in the database
#returns a list of unique ips
def parse_requests(table_name,filename='logs/humans.json'):
    try:
        ips,requests = _extract_http_and_time(filename) ##requests is a list of tuple
        formated_requests = _format_requests(requests)  #get the requests as a dict in the format the database accepts
        if filename == 'logs/humans.json':
            formated_requests_clean = remove_bot_req(formated_requests)
        else:
            formated_requests_clean = formated_requests
            
        with DatabaseHandler(table_name) as db:
            db.create_table(table_name)
            for req in formated_requests_clean:
                db.store(req)
        with DatabaseHandler(table_name) as db:
            l = db.cursor.execute("SELECT * FROM {}".format(table_name)).fetchall()
            ips_in_table = []
            for val in l:
                ips_in_table.append(val[1])
        return list(set(ips_in_table))
    except Exception as e:
        raise e

def get_unique_ips(table_name):
    with DatabaseHandler(table_name) as db:
        l = db.cursor.execute("SELECT * FROM {}".format(table_name)).fetchall()
        ips_in_table = []
        for val in l:
            ips_in_table.append(val[1])
    return list(set(ips_in_table))

if __name__ == "__main__": 
    ips = parse_requests('humans')
    db = DatabaseHandler("humans")
    db.print_table()
