import re
from clientinfo import _make_request_instances, get_info

#--------------HELP VARIABLES---------------

#All different types of browser, most use Mozilla
valid_applications = ['Mozilla','Opera', 'Safari']
#Most common types of operative systems
valid_systems = ['Mac OS', 'Linux', 'Windows', 'X11', 'Android', 'PlayStation']
#Most common types of operative platforms
valid_platforms = ['AppleWebKit', 'KHTML']
#Most common types of platform details
valid_platform_details = ['Gecko', 'KHTML']
#Most common types of extensions
valid_extensions = ['Gecko', 'Safari', 'Firefox', 'Chrome', 'Mobile', 'Version', 'Presto', 'Waterfox', 'Chromium', 'Edge', 'OPR', 'Edg', 'Yowser', 'YaBrowser']




#--------------HELP FUNCTIONS---------------

def useragent_long(ua_splitted):
    #Boolean to keep track if each test passes. If a test passes, reset to False and go to next
    real = False
    #Checks if the app is a legit one (e.g. "Mozilla", "Opera", "Safari")
    for app in valid_applications:
        if(ua_splitted[0].find(app) != -1):
            real = True
    if not real:
        print("Not a real APP name: ", ua_splitted[0])
        #Not a valid application name
        return False

    real = False


    #Checks if the system is a legit one (e.g. "Windows NT", "Linux", "Mac OS")
    for sys in valid_systems:
        if(ua_splitted[1].find(sys) != -1):
            real = True
    if not real:
        print("Not a real SYSTEM name: ", ua_splitted[1])
        #Not a valid system
        return False

    real = False

    #Checks if the platform is a legit one (e.g. "AppleWebKit")
    for plat in valid_platforms:
        if(ua_splitted[2].find(plat) != -1):
            real = True
    if not real:
        print("Not a real PLATFORM name: ", ua_splitted[2])
        #Not a valid platform
        return False

    real = False

    #Checks if the platform detail is a legit one (e.g. "KHTML")
    for dets in valid_platform_details:
        if(ua_splitted[3].find(dets)):
            real = True
    if not real:
        print("Not a real PLATFORM detail name: ", ua_splitted[3])
        #Not a valid platform detail
        return False

    real = False

    #Checks if the extension is a legit one (e.g. "Mobile")
    for ext in valid_extensions:
        if(ua_splitted[4].find(ext) != -1):
            real = True
    if not real:
        print("Not a real EXTENSION name: ", ua_splitted[4])
        #Not a valid extension
        return False

    #Made all five tests without ending pre-maturely, the user-agent is a real one
    return True



def useragent_short(ua_splitted):
    #Boolean to keep track if each test passes. If a test passes, reset to False and go to next
    real = False
    #Checks if the app is a legit one (e.g. "Mozilla", "Opera", "Safari")
    for app in valid_applications:
        if(ua_splitted[0].find(app) != -1):
            real = True
    if not real:
        print("Not a real APP name: ", ua_splitted[0])
        #Not a valid application name
        return False

    real = False

    #Checks if the system is a legit one (e.g. "Windows NT", "Linux", "Mac OS")
    for sys in valid_systems:
        if(ua_splitted[1].find(sys) != -1):
            real = True
    if not real:
        print("Not a real SYSTEM name: ", ua_splitted[1])
        #Not a valid system
        return False

    real = False

    for ext in valid_extensions:
        if(ua_splitted[2].find(ext) != -1):
            real = True
    if not real:
        print("Not a real EXTENSION name: ", ua_splitted[2])
        #Not a valid extension
        return False

    #Made all three tests without ending pre-maturely, the user-agent is a real one
    return True



#User-Agent (UA): App/X.X (<system-information>) <platform> (<platform-details>) <extensions>
#Checks if the given user-agent is legit, return either True or False
def real_useragent(user_agent):


    #Split UA with radix ' (' or ') '
    ua_splitted = re.split('\ \(|\)\ ', user_agent)
    length = len(ua_splitted)

    ##Check the length of the UA and call for helper function.
    #Too short to be a real UA
    if length < 3:
        return False
    elif length == 3:
        #e.g: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:74.0) Gecko/20100101 Firefox/74.0'
        return useragent_short(ua_splitted)
    elif length == 5:
        #e.g: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
        return useragent_long(ua_splitted)
    else: return False



#-------------ANALYZE A REQUEST--------------


#Analyzes a request with LEVEL 1 detection, return a integer: 1 or 4
def analyze_level_one(ip_info):
    if(real_useragent(ip_info['user_agents'][0]) is False):
        return 4
    return 1



#Analyzes a request with LEVEL 2 detection, return a integer: 1, 2, 3, 4
def analyze_level_two(ip_info):
    value = 1
    #Request contains: request_rate, number_of_user_agents, user_agents,
    user_agents = ip_info['user_agents']
    number_of_ua = ip_info['number_of_user_agents']
    number_of_requests = ip_info['number_of_requests']
    avarage_request_rate = ip_info['avarage_request_rate']
    ua_ratio = number_of_ua/number_of_requests
    #Test 1, is all the user-agents real from all the requests made from this IP?
    for ua in user_agents:
        if(real_useragent(ua) is False):
             return 4
    if number_of_ua > 1.03: #avarage number of user agents in the human set
        value = value + 1
    if avarage_request_rate > 0.49: #taken from human set
        value = value + 1
    if ua_ratio > 0.69 and number_of_requests > 2.71: #taken from human set
        value = value + 1
    return value






#--------------------MAIN--------------------

#Recieve a list of IPs to analyze, for each IP, decide LEVEL 1 or 2
def analyze(ip_list,table):
    score_list = []
    for ip in ip_list:
        #check ip in DB and decide LEVEL 1 or LEVEL 2
        ip_info = get_info(ip,table)
        if ip_info['number_of_requests'] == 1:
            score = analyze_level_one(ip_info)
        else:
            score = analyze_level_two(ip_info)
        #Store each detection score in list
        score_list.append(score)

    #Returns a list of touples, each request with its score
    zipped = zip(ip_list, score_list)
    #Format: [(ip1, score1),...(ipx,scorex)]
    return list(zipped)


# user_agent_rotator = UserAgent(limit=100)
# list = user_agent_rotator.get_user_agents()#

# for ua in list:
#     real = real_useragent(ua['user_agent'])
#     if real is False:
#         print('False UA: ' + ua['user_agent'] + '\n')
#         print(ua['user_agent'] + '\n')
