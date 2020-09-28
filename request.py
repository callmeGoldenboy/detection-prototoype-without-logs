
class Request:
    
    def __init__(self,insertid,ip,user_agent,referer,resource,time):
          self.insertid = insertid
          self.ip = ip
          self.user_agent = user_agent
          self.referer = referer
          self.resource = resource
          self.time = time

    def __repr__(self):
        return "insertid={}, ip={}, user_agent={}, referer={}, resource={}, time={}".format(self.insertid,self.ip,self.user_agent,self.referer,self.resource,self.time)

    def get_user_agent(self):
        return self.user_agent
    
    def get_ip(self):
        return self.ip
      
    def get_referer(self):
        return self.referer

    def get_resource(self):
        return self.resource

    def get_time(self):
        return self.time



if __name__ == "__main__":
    r = Request(ip="20.20.3",user_agent="python",referer="/google.com",resource="/panprices/offers",time="10.20")
    print(r.get_user_agent())
    print(r.get_ip())
    print(r.get_referer())
    print(r.get_resource())
    print(r.get_time())
