import random as r
import time as t
from utils import *

class Kojo_s_kitchen_simulator:
    inf =  1e10
    def __init__(self, additionalworker = False,my_lambda = 0.5):
        self.time = 0
        # first worker, second worker and auxiliar worker end-service-time
        self.tfw = self.tsw = self.taw = self.inf
        self.clients = []
        self.n = 0 # number of clients in the system
        self.uns_clients = 0 # number of unsatisfied client in the system
        self.time_nd = 660
        self.next_arrival = self.inf
        self.additionalworker = additionalworker
        self.acumulated_time = 0
        self.my_lambda = my_lambda

    def next_arrival_time(self):
        new_time = round(generate_exponential(self.my_lambda))        
        if self.time + new_time > self.time_nd: 
            return self.inf
        return self.time + new_time
    
    def food_decition(self):
        # choice a number between 0 and 1
        return r.randint(0,1)

    def food_time(self,decition):
        if decition == 0:
            return round(r.uniform(3,5))
        return round(r.uniform(5,7))

    def call_client(self):
        client = self.clients.pop(0) # a new client left the queue
        if self.time - client > 5 :# if the client wait more than 5 mints is unsatisfied
            self.uns_clients += 1
        decition = self.food_decition() # decide what's gonna eat
        ts = self.food_time(decition)
        return self.time + ts # time to fish new service

    """Return 0 if the minimun is arrival_time, 1 if it's tfw, 2 if it's tsw and 3 if it's taw"""
    def next_event(self):
        arrival_time_tuple = (self.next_arrival, 0)
        tfw_tuple = (self.tfw, 1)
        tsw_tuple = (self.tsw, 2)
        taw_tuple = (self.taw, 3)
        return min(arrival_time_tuple, tsw_tuple, tfw_tuple, taw_tuple)
  
    """Returns 0 is anybody it's free, 1 if tfw is, 2 if tsw is and 3 if taw is"""
    def who_is_free(self):
        if self.tfw == self.inf: 
            return 1
        if self.tsw == self.inf: 
            return 2
        if self.additionalworker and ((90 < self.time < 210) or (420 < self.time< 540)):
            if self.taw == self.inf: 
                return 3
        return 0 

    def simulate(self):
        # print("*"*20 +"Kojo's kitchen"+ "*"*20)       
        while(not(self.time >= self.time_nd and self.tfw == self.tsw == self.taw == self.next_arrival == self.inf)):
            if self.next_arrival == self.inf and self.time < self.time_nd: #I'm in first moment of the simulation
                self.next_arrival = self.next_arrival_time()
            event = self.next_event()
            if event[0] == self.inf:
                    continue
            if event[1] == 0: # It's an arrival_time
                self.time = self.next_arrival
                self.n += 1
                
                worker = self.who_is_free()
                if worker == 0: # anybody is free                    
                    self.clients.append(self.next_arrival)
                else:
                    ts = self.food_time(self.food_decition())
                    if worker == 1:
                        self.tfw = self.time + ts
                    elif worker == 2:
                        self.tsw = self.time + ts
                    elif worker == 3:
                        self.taw = self.time + ts
                
                self.next_arrival = self.next_arrival_time()
            
            else:
                self.time = event[0]
                new_ts = self.inf
                if event[1] == 1: # the first worker finish
                    if len(self.clients) > 0:
                        new_ts = self.call_client()
                    self.tfw = new_ts
                elif event[1] == 2: # the second worker finish
                    if len(self.clients) > 0:
                        new_ts = self.call_client()
                    self.tsw = new_ts
                elif event[1] == 3: # the additional worker finish
                    if 90 <= self.time <= 210 or 240 <= self.time < 540:                        
                        if len(self.clients)> 0:
                            new_ts = self.call_client()
                    
                    self.taw = new_ts
        # print("\n"+"*"*20+"Simulattion ends"+"*"*20)        
        # print(self.time)  
        # print(self.n)
        # print(self.uns_clients)
        # return(self.time, self.n, self.uns_clients)
        return (self.uns_clients * 100)/self.n

if __name__ == "__main__":
    results = {}
    results["0.5"]= (0,0)
    for i in range(1000):
        k = Kojo_s_kitchen_simulator(False,0.5)
        sinE = results["0.5"][0] + k.simulate()
        l = Kojo_s_kitchen_simulator(True,0.5)
        conE = results["0.5"][1] + l.simulate()
        results["0.5"] = (sinE,conE)

    results["0.25"] = (0,0)
    for i in range(1000):
        k = Kojo_s_kitchen_simulator(False,0.25)
        sinE = results["0.25"][0] + k.simulate()
        l = Kojo_s_kitchen_simulator(True,0.25)
        conE = results["0.25"][1] + l.simulate()
        results["0.25"]=(sinE,conE)
    for lab in results:
        print(lab.__str__())
        print("SinExtra: " + str(results[lab][0]/1000))
        print("ConExtra: " + str(results[lab][1]/1000))
            
