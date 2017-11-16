import time,datetime
import sys
import threading
import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers.api import ObservedWatch

'''
Two handlers for each server.
Global variable "current_server" means the state of two servers:
01 means the first server is available, 10 means the second one is available,11 means both are available.
'''
class MyHandler1(PatternMatchingEventHandler):
    '''Change here to match expected files.'''
    patterns=["*.cpp"]       
    
    def on_created(self,event):
        print event.src_path,event.event_type
        global current_server
        current_server^=1

    def on_deleted(self,event):
        print event.src_path,event.event_type

class MyHandler2(PatternMatchingEventHandler):
    '''Change here to match expected files.'''
    patterns=["*.cpp"]       
    
    def on_created(self, event):
        print event.src_path,event.event_type
        global current_server
        current_server^=2

    def on_deleted(self,event):
        print event.src_path,event.event_type

'''This part has been tested.'''
def Mount_to_server(folder_name,server):
    directory="/Users/username/"+folder_name
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.system("mount -t afp://"+server+" "+directory)

'''Return true if it's time to begin monitoring'''
def Begin(h,b,e):
    if b>e:
        if (h>=b or h<e):
            return (True)
    else:
        if (h>=b and h<e):
            return (True)
    return (False)

'''Return true if it's time to end monitoring'''
def End(h,b,e):
    if b>e:
        if (h<b and h>=e):
            return (True)
    else:
        if (h<b or h>=e):
            return (True)
    return (False)

if __name__ == "__main__":
    '''args1,args2 denotes the folders that mount to two servers respectively.'''
    args1=sys.argv[1]
    args2=sys.argv[2]

    #Mount_to_server(args1,server1);Mount_to_server(args2,server2)
    
    observer=Observer()
    watch1=observer.schedule(MyHandler1(),path=args1,recursive=False)
    watch2=observer.schedule(MyHandler2(),path=args2,recursive=False)

    '''Decide whether to begin monitoring (from begin_time to end_time)'''
    begin_time=19;end_time=9
    i=datetime.datetime.now()
    print "Now is: ", time.asctime(time.localtime(time.time()))
    if not Begin(i.hour,begin_time,end_time):
        print("Program hasn't started yet...")
    while True:
        time.sleep(1)
        i=datetime.datetime.now()
        if Begin(i.hour,begin_time,end_time):
            break
    current_server=0
    print("Start watching!")
    observer.start()

    try:
        while True:
            time.sleep(1)
            
    except (KeyboardInterrupt or End(datetime.datetime.now().hour,begin_time,end_time)):
        print("End watching!")
        observer.stop()
    observer.join()
