import re
import math


class Mytask():
    def __init__(self, phase_time, period, relative_deadline, execution_time, absolute_deadline, TID):
        self.phase_time = phase_time
        self.period = period
        self.relative_deadline = relative_deadline
        self.execution_time = execution_time
        self.absolute_deadline = absolute_deadline
        self.TID = TID


def Readfile(filename):
    f = open(filename, mode="r")
    test1 = f.readlines()
    job = []
    for i in range(len(test1)):
        splitstr = re.split(",| |\n", test1[i])
        # print(splitstr)
        rem = []
        for j in range(len(splitstr)):
            if splitstr[j] == " " or splitstr[j] == "," or splitstr[j] == "":
                continue
            else:
                rem.append(int(splitstr[j]))
        job.append(rem)
    return job


def RecursiveGcd(x, y):
    if y == 0:
        return x
    else:
        return RecursiveGcd(y, x % y)


def computeLcm(x, y):
    lcm = (x*y)//RecursiveGcd(x, y)
    return lcm


def sort_priority_EDF(e):
    return e.absolute_deadline


def sort_priority_RM(e):
    return e.period


def EDF(filename):
    jobs = Readfile(filename)
    clock = 0
    misstask = 0
    LCM = 1
    MaxPH = 0
    names = globals()
    ready_queue = []
    schedulability = 0
    sumOFjobs = 0
    for i in range(len(jobs)):
        names['task%s' % i] = Mytask(phase_time=jobs[i][0], period=jobs[i]
                                     [1], relative_deadline=jobs[i][2], execution_time=jobs[i][3], absolute_deadline=0, TID=i+1)
        LCM = computeLcm(LCM, jobs[i][1])
        schedulability += float(names['task%s' % i].execution_time) / \
            float(names['task%s' % i].period)
        if MaxPH < jobs[i][0]:
            MaxPH = jobs[i][0]
    if schedulability <= 1:
        f.write("Schedulable!\n")
    else:
        f.write("Unschedulable!\n")
        return
    while clock < LCM+MaxPH:
        # 1.判斷readyqueue是否有missdeadline的job
        i = 0
        while True:
            if i >= len(ready_queue):
                break
            if ready_queue[i].absolute_deadline-clock-ready_queue[i].execution_time < 0:
                ready_queue.pop(i)
                misstask += 1
            i += 1
        # 2.判斷task是否進來 並加入readyqueue
        for i in range(len(jobs)):
            names['task%s' % i] = Mytask(phase_time=jobs[i][0], period=jobs[i]
                                         [1], relative_deadline=jobs[i][2], execution_time=jobs[i][3], absolute_deadline=0, TID=i+1)
        for i in range(len(jobs)):
            if (clock-names['task%s' % i].phase_time) % names['task%s' % i].period == 0:
                names['task%s' % i].absolute_deadline = clock + \
                    names['task%s' % i].relative_deadline
                ready_queue.append(names['task%s' % i])
                sumOFjobs += 1
        # 3.根據priority sort ready queue
        ready_queue.sort(key=sort_priority_EDF)
        # 4.priority最高的exe要減掉一\
        if len(ready_queue) != 0:
            ready_queue[0].execution_time -= 1
            f.write("Time %s : Task %s\n" % (clock,ready_queue[0].TID))
            if ready_queue[0].execution_time == 0:
                del ready_queue[0]
        else:
            f.write("Time %s : No Task\n" % clock)
        clock += 1
    f.write("Missed Jobs = %s\n" % misstask)
    f.write("Sum of jobs = %s\n" % sumOFjobs)


def RM(filename):
    jobs = Readfile(filename)
    clock = 0
    misstask = 0
    LCM = 1
    MaxPH = 0
    names = globals()
    ready_queue = []
    schedulability = 0
    sumOFjobs = 0
    for i in range(len(jobs)):
        names['task%s' % i] = Mytask(phase_time=jobs[i][0], period=jobs[i]
                                     [1], relative_deadline=jobs[i][2], execution_time=jobs[i][3], absolute_deadline=0, TID=i+1)
        LCM = computeLcm(LCM, jobs[i][1])
        schedulability += float(names['task%s' % i].execution_time) / \
            float(names['task%s' % i].period)
        if MaxPH < jobs[i][0]:  
            MaxPH = jobs[i][0]
    if schedulability <= len(jobs)*(pow(2,1/len(jobs))-1):
       
        f.write("Schedulable!\n")
    else:
        f.write("Unschedulable or Schedulable!\n")
    while clock < LCM+MaxPH:
        # 1.判斷readyqueue是否有missdeadline的job
        i = 0
        while True:
            if i >= len(ready_queue):
                break
            if ready_queue[i].absolute_deadline-clock-ready_queue[i].execution_time < 0:
                ready_queue.pop(i)
                misstask += 1
            i += 1
        # 2.判斷task是否進來 並加入readyqueue
        for i in range(len(jobs)):
            names['task%s' % i] = Mytask(phase_time=jobs[i][0], period=jobs[i]
                                         [1], relative_deadline=jobs[i][2], execution_time=jobs[i][3], absolute_deadline=0, TID=i+1)
        for i in range(len(jobs)):
            if (clock-names['task%s' % i].phase_time) % names['task%s' % i].period == 0:
                names['task%s' % i].absolute_deadline = clock + \
                    names['task%s' % i].relative_deadline
                ready_queue.append(names['task%s' % i])
                sumOFjobs += 1
        # 3.根據priority sort ready queue
        ready_queue.sort(key=sort_priority_RM)
        # 4.priority最高的exe要減掉一
        if len(ready_queue) != 0:
            ready_queue[0].execution_time -= 1
            f.write("Time %s : Task %s\n" % (clock, ready_queue[0].TID))
            if ready_queue[0].execution_time == 0:
                del ready_queue[0]
        else:
            f.write("Time %s : No Task\n" % clock)
        clock += 1
    f.write("Missed Jobs = %s\n" % misstask)
    f.write("Sum of jobs = %s\n" % sumOFjobs)

for i in range(1, 7):
    f = open("EDF test%s.txt" % i, 'w')
    EDF("test%s.txt" % i)
    f.close()
    f = open("RM test%s.txt" % i, 'w')
    RM("test%s.txt" % i)
    f.close()
