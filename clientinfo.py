from request import Request
from databasehandler import DatabaseHandler
import pprint
import re
import datetime
import math 
import socket
#returns all rows containing the ip
def _get_all_rows(ip,table):
    with DatabaseHandler(table) as db:
        return db.read(ip)
#queries the databse with the ip and returns a list of request instances of all the rows
def _make_request_instances(ip,table):
    rows = _get_all_rows(ip,table)
    if len(rows) == 0:
        return None
    request_instances = []
    for req in rows:
        req_instance = Request(insertid = req[0],ip=req[1],user_agent=req[2],referer=req[3],time=req[4],resource=req[5])
        request_instances.append(req_instance)
    return request_instances

def _number_of_ua(requests):
    user_agents = []
    for req in requests:
        if req.user_agent not in user_agents:
            user_agents.append(req.user_agent)

    return len(user_agents),user_agents

#returns all the requests for the given day
def get_requests_for_a_day(day,timestamps):
    new_timestamps = []
    for timestamp in timestamps:
        if day in timestamp:
            new_timestamps.append(timestamp)
    return new_timestamps

def _get_timestamps(requests):
    timestamps = []
    for req in requests:
        timestamps.append(req.get_time())
    return timestamps

#takes a timestamp in the format it is saved in the databse and returns a datetimeobject of it
def make_datetime_obj(timestamp):
    arr = re.split('T|Z',timestamp)
    day = arr[0].split('-')
    time = arr[1].split(':')
    new_day = datetime.datetime(year=int(day[0]),month=int(day[1]),day=int(day[2]),hour=int(time[0]),minute=int(time[1]),second=math.trunc(float(time[2]))) #ignore millisecond for now
    return new_day    
    


#returns a list of lists, where each element is a cluster of requests that were mawithin the given interval
def _get_request_clusters(interval,timestamps):
    datetime_timestamps = []
    for timestamp in timestamps:
       datetime_timestamps.append(make_datetime_obj(timestamp))
    datetime_timestamps.sort()
    if len(datetime_timestamps) < 2:
        return [datetime_timestamps]
    else:
        #x = datetime_timestamps[0]
        #y = datetime_timestamps[1]
        diff = datetime.timedelta(seconds=interval)
        i = 0
        whole_list = []
        relative_list = []
        x = i   
        y = i + 1
        relative_list.append(datetime_timestamps[x])
        while y < len(datetime_timestamps):  #returns a list of clusters where each cluster contains the requests that came within the given interval
            if (datetime_timestamps[y] - datetime_timestamps[x]) <= diff:
                relative_list.append(datetime_timestamps[y])
                
            else:
                whole_list.append(relative_list)
                relative_list = [datetime_timestamps[y]]
                x = y
            y = y + 1
        whole_list.append(relative_list)
        #pprint.pprint(whole_list)
        return whole_list

def _get_avarage_request_rate(request_clusters):
    avg_rate = 0
    for time_list in request_clusters:
          if len(time_list) == 1:
                rate_relative = 0 #probably unecessary
          else:
                avg_relative = 0
                start = time_list[0]
                finish = time_list[-1]
                try:
                    rate_relative = len(time_list)/((finish - start).total_seconds())
                except ZeroDivisionError:
                    rate_relative = len(time_list)
          avg_rate = avg_rate + rate_relative
    return avg_rate/len(request_clusters)
   
              

#takes an ip and calculates useful information regarding the ip such as number of user agents, request rate
#the interval parameter is the number of seconds between requests
#returns a dict with the info
def get_info(ip,table,interval=60):
    requests = _make_request_instances(ip,table)
    if requests is None:
        print("No requests were made by: {}".format(ip))
        return None
    number_of_user_agents,user_agents = _number_of_ua(requests)
    timestamps = _get_timestamps(requests)
    request_clusters = _get_request_clusters(interval,timestamps)
    avg_request_rate = _get_avarage_request_rate(request_clusters)
    return {"client_ip": ip,
            "number_of_user_agents":number_of_user_agents,
            "user_agents":user_agents,
            "request_clusters":request_clusters,
            "number_of_requests":len(requests),
            "avarage_request_rate":avg_request_rate}

if __name__ == "__main__":
    ips = ['2a03:2880:31ff:16::face:b00c','2002:9a60:e389::9a60:e389'] 
    dns= []
    for ip in ['2a00:801:707:8f4b:f500:dba2:881c:3e0b']:
        info = get_info(ip,'humans')
        pprint.pprint(info) 
        try:
            reversed_dns = socket.gethostbyaddr(ip)
            dns.append(reversed_dns[0])
            print(reversed_dns[0])
        except Exception as e:
            print(e)
    print(dns)
    
