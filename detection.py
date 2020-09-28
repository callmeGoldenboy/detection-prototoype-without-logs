from LogReader import parse_requests, get_unique_ips
from analyzer import analyze
from clientinfo import get_info 
import pprint 
 
#Input -> Output: (JSON File) ->  [{IP, 1-4},..., {IP, 1-4}]
def detection(table_name):
    print("Analyzing for: {}".format(table_name))
    #Store each request in the DB and return a list of unique IPs from the json log file
    #ip_list = parse_requests('botslevel1','logs/humans.json')
    ip_list = get_unique_ips(table_name)
    print("There are {} IP-addresses".format(str(len(ip_list))))
    ip_value_list = analyze(ip_list,table_name)
    pprint.pprint(ip_value_list)


def test_human():
    #Store each request in the DB and return a list of unique IPs from the json log file
     ip_list = parse_requests('humans','logs/humans.json')
     #ip_value_list = analyze(ip_list)
     info =[]
     tot_rate = 0
     tot_user_agents = 0
     tot_ratio = 0
     tot_requests = 0
     for ip in ip_list:
         val = get_info(ip,'humans')
         if val is not None: 
             pprint.pprint(val)
             info.append(val)
     for val in info:
         tot_rate = tot_rate + val["avarage_request_rate"]
         tot_user_agents = tot_user_agents + val["number_of_user_agents"]
         tot_ratio = tot_ratio + (val["number_of_user_agents"]/val["number_of_requests"])
         tot_requests = tot_requests + val["number_of_requests"]
     print("Avarage request rate in the human set is: {}".format(str(tot_rate/len(info))))
     print("Avarage number of user agents in the human set is: {}".format(str(tot_user_agents/len(info))))
     print("Avarage ratio of user agents/requests in the human set is: {}".format(str(tot_ratio/len(info))))
    
     print("Avarage number of requests in the human set is: {}".format(str(tot_requests/len(info))))
     print("There are {} unique ips".format(str(len(info))))
     #print(ip_value_list)

def test_bot_level1():
    #Store each request in the DB and return a list of unique IPs from the json log file
     ip_list = parse_requests('botslevel1','logs/SandboxScrapedLevel1-100x3requests.json')
     #ip_value_list = analyze(ip_list)
     info =[]
     tot_rate = 0
     tot_user_agents = 0
     for ip in ip_list:
         val = get_info(ip,'botslevel1')
         if val is not None: 
             pprint.pprint(val)
             info.append(val)
     for val in info:
         tot_rate = tot_rate + val["avarage_request_rate"]
         tot_user_agents = tot_user_agents + val["number_of_user_agents"]
     print("Avarage request rate in the botslevel1 set is: {}".format(str(tot_rate/len(info))))
     print("Avarage number of user agents in the botslevel1 set is: {}".format(str(tot_user_agents/len(info))))
     print("There are {} unique ips".format(str(len(info))))

def test_bot_level2_singleua():
    #Store each request in the DB and return a list of unique IPs from the json log file
     ip_list = parse_requests('botslevel2singleua','logs/SandboxScrapedLevel2OneUA-100x3requests.json')
     #ip_value_list = analyze(ip_list)
     info =[]
     tot_rate = 0
     tot_user_agents = 0
     for ip in ip_list:
         val = get_info(ip,'botslevel2singleua')
         if val is not None: 
             pprint.pprint(val)
             info.append(val)
     for val in info:
         tot_rate = tot_rate + val["avarage_request_rate"]
         tot_user_agents = tot_user_agents + val["number_of_user_agents"]
     print("Avarage request rate in the botslevel1 set is: {}".format(str(tot_rate/len(info))))
     print("Avarage number of user agents in the botslevel1 set is: {}".format(str(tot_user_agents/len(info))))
     print("There are {} unique ips".format(str(len(info))))


def test_bot_level2_multipleua():
    #Store each request in the DB and return a list of unique IPs from the json log file
     ip_list = parse_requests('botslevel2multipleua','logs/SandboxScrapedLevel2MultipUA-100x3requests.json')
     #ip_value_list = analyze(ip_list)
     info =[]
     tot_rate = 0
     tot_user_agents = 0
     for ip in ip_list:
         val = get_info(ip,'botslevel2multipleua')
         if val is not None: 
             pprint.pprint(val)
             info.append(val)
     for val in info:
         tot_rate = tot_rate + val["avarage_request_rate"]
         tot_user_agents = tot_user_agents + val["number_of_user_agents"]
     print("Avarage request rate in the botslevel1 set is: {}".format(str(tot_rate/len(info))))
     print("Avarage number of user agents in the botslevel1 set is: {}".format(str(tot_user_agents/len(info))))
     print("There are {} unique ips".format(str(len(info))))

def test_bot_level3_singleua():
    #Store each request in the DB and return a list of unique IPs from the json log file
     ip_list = parse_requests('botslevel3singleua','logs/SandboxScrapedLevel3OneUA-Sleep(5-10s)-100x3requests.json')
     #ip_value_list = analyze(ip_list)
     info =[]
     tot_rate = 0
     tot_user_agents = 0
     for ip in ip_list:
         val = get_info(ip,'botslevel3singleua')
         if val is not None: 
             pprint.pprint(val)
             info.append(val)
     for val in info:
         tot_rate = tot_rate + val["avarage_request_rate"]
         tot_user_agents = tot_user_agents + val["number_of_user_agents"]
     print("Avarage request rate in the botslevel1 set is: {}".format(str(tot_rate/len(info))))
     print("Avarage number of user agents in the botslevel1 set is: {}".format(str(tot_user_agents/len(info))))
     print("There are {} unique ips".format(str(len(info))))


def test_bot_level3_multipleua():
    #Store each request in the DB and return a list of unique IPs from the json log file
     ip_list = parse_requests('botslevel3multipleua','logs/SandboxScrapedLevel3MultipUA-Sleep(5-10s)-100x3requests.json')
     #ip_value_list = analyze(ip_list)
     info =[]
     tot_rate = 0
     tot_user_agents = 0
     for ip in ip_list:
         val = get_info(ip,'botslevel3multipleua')
         if val is not None: 
             pprint.pprint(val)
             info.append(val)
     for val in info:
         tot_rate = tot_rate + val["avarage_request_rate"]
         tot_user_agents = tot_user_agents + val["number_of_user_agents"]
     print("Avarage request rate in the botslevel1 set is: {}".format(str(tot_rate/len(info))))
     print("Avarage number of user agents in the botslevel1 set is: {}".format(str(tot_user_agents/len(info))))
     print("There are {} unique ips".format(str(len(info))))
 
if __name__ == "__main__":
    #test_human()
    #test_bot_level1()
    #test_bot_level2_singleua()
    #test_bot_level2_multipleua()
    #test_bot_level3_singleua()
    #test_bot_level3_multipleua()
    detection('humans')
    detection('botslevel1')
    detection('botslevel2singleua')
    detection('botslevel2multipleua')
    detection('botslevel3singleua')
    detection('botslevel3multipleua')
