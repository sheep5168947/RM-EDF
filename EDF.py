
import re


class Mytask():
    def __init__(self,TID,Phase,Period,WCET,RD,Utilization):
        self.TID = TID
        self.Phase = Phase
        self.Period = Period
        self.WCET = WCET
        self.RD = RD
        self.Utilization = Utilization

class Myjob():
    def __init__(self,release_time,remain_execution_time,absolute_deadline,TID):
        self.release_time = release_time
        self.remain_execution_time = remain_execution_time
        self.absolute_deadline = absolute_deadline
        self.TID = TID

def Readfile(filename):
    f = open(filename,mode = "r")

    test1 = f.readlines()
    job = []

    for i in range(len(test1)):

        splitstr = re.split(",| |\n",test1[i])
        # print(splitstr)
        rem = []
        for j in range(len(splitstr)):
        
            if splitstr[j] == " " or splitstr[j] == ","or splitstr[j] == "":
                continue
            else:
                rem.append(int(splitstr[j]))
        job.append(rem)
    return job

def EDF(filename):
    jobs = Readfile(filename)
    for i in range(len(jobs)):
        


    return 0




