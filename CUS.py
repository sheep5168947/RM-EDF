import re
import math


class PeriodTask():
    def __init__(self, period, execution_time, absolute_deadline, TID):
        self.period = period
        self.execution_time = execution_time
        self.absolute_deadline = absolute_deadline
        self.TID = TID


class AperiodTask():
    def __init__(self, arrive_time, execution_time, TID):
        self.arrive_time = arrive_time
        self.execution_time = execution_time
        # self.absolute_deadline = absolute_deadline
        self.TID = TID


def Readfile(filename):
    f = open(filename, mode="r")
    test1 = f.readlines()
    print(len(test1))
    job = []
    for i in range(len(test1)):
        splitstr = re.split(",| |\n", test1[i])
        print(splitstr)
        rem = []
        for j in range(len(splitstr)):
            if splitstr[j] == " " or splitstr[j] == "," or splitstr[j] == "":
                continue
            else:
                rem.append(int(splitstr[j]))
        job.append(rem)
    return job


def sort_priority_EDF(e):
    return e.absolute_deadline

def EDF(period, aperiod):
    peroid_jobs = Readfile(period)
    aperiod_jobs = Readfile(aperiod)
    clock = 0
    cus_deadline = 0
    MissPJobNumber = 0
    MaxSimTime = 1000
    names = globals()
    TotalResponseTime = 0
    ready_queue_period = []
    ready_queue_aperiod = []
    # schedulability = 0
    TotalPJobNumber = 0
    for i in range(len(peroid_jobs)):
        names['period_task%s' % i] = PeriodTask(
            period=peroid_jobs[i][0], execution_time=peroid_jobs[i][1], absolute_deadline=0, TID=i+1)
    for i in range(len(aperiod_jobs)):
        names['aperiod_task%s' % i] = AperiodTask(
            arrive_time=aperiod_jobs[i][0], execution_time=aperiod_jobs[i][1], TID=i+1)
    while clock < MaxSimTime:
        if cus_deadline > clock:
            continue
        else:
            cus_deadline = clock
        # 1.判斷readyqueue是否有missdeadline的job

        i = 0
        while True:
            if i >= len(ready_queue_period):
                break
            if ready_queue_period[i].absolute_deadline-clock-ready_queue_period[i].execution_time < 0:
                ready_queue_period.pop(i)
                MissPJobNumber += 1
            i += 1
        # 2.判斷period_task是否進來 並加入readyqueue
        for i in range(len(peroid_jobs)):
            names['Ptask%s' % i] = PeriodTask(period=peroid_jobs[i]
                                             [0], execution_time=peroid_jobs[i][1], absolute_deadline=0, TID=i+1)
        for i in range(len(peroid_jobs)):
            if clock % names['Ptask%s' % i].period == 0:
                names['Ptask%s' % i].absolute_deadline = clock + \
                    names['Ptask%s' % i].period
                ready_queue_period.append(names['Ptask%s' % i])
                TotalPJobNumber += 1
        # 將在時間點clock抵達的aperiodic job加入到AQ中
        for i in range(len(aperiod_jobs)):
            names['Atask%s' % i] = AperiodTask(arrive_time=aperiod_jobs[i]
                                             [0], execution_time=aperiod_jobs[i][1], TID=i+1)
        for i in range(len(aperiod_jobs)):
            if clock == names['Atask%s' % i].arrive_time:
                ready_queue_aperiod.append(names['Atask%s' % i])
                if ready_queue_period[0].arrive_time == clock:
                    cus_deadline = names['Atask%s' % i].exection_time/0.2 + clock
        # 根據priority sort ready queue
        ready_queue_period.sort(key=sort_priority_EDF)
        # priority最高的exe要減掉一\
        if ready_queue_period[0].absolute_time <= cus_deadline:
            chose = 0
        else:
            chose = 1
        if len(ready_queue_period) != 0 and chose == 0:
            ready_queue_period[0].execution_time -= 1
            f.write("Time %s : Task %s\n" % (clock, ready_queue_period[0].TID))
            if ready_queue_period[0].execution_time == 0:
                del ready_queue_period[0]
        elif len(ready_queue_aperiod) != 0 and chose == 0:
            ready_queue_aperiod[0].execution_time -=1
            f.write("Time %s : No Task\n" % clock)
        clock += 1
    f.write("Missed Jobs = %s\n" % misstask)
    f.write("Sum of jobs = %s\n" % TotalPJobNumber)

f = open("0_8.txt",mode="w")
EDF("cus_test8.txt", "aperodic.txt")
f.close