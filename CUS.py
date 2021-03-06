import re
import math


class PeriodTask():
    def __init__(self, arrive_time, period, execution_time, absolute_deadline, TID):
        self.period = period
        self.arrive_time = arrive_time
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
    job = []
    for i in range(len(test1)):
        splitstr = re.split(",| |\n", test1[i])
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


def CUS(period, aperiod,f):
    peroid_jobs = Readfile(period)
    aperiod_jobs = Readfile(aperiod)
    clock = 0
    cus_deadline = 0
    MissPJobNumber = 0
    FinishedPJobNumber = 0
    FinishedAJobNumber = 0
    MaxSimTime = 1000
    names = globals()
    budget = True
    TotalPResponseTime = 0
    TotalAResponseTime = 0
    ready_queue_period = []
    ready_queue_aperiod = []
    TotalPJobNumber = 0

    while clock < MaxSimTime:
        if cus_deadline > clock:
            cus_deadline = cus_deadline
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
            names['Ptask%s' % i] = PeriodTask(arrive_time=0, period=peroid_jobs[i]
                                              [0], execution_time=peroid_jobs[i][1], absolute_deadline=0, TID=i+1)
        for i in range(len(peroid_jobs)):
            if clock % names['Ptask%s' % i].period == 0:
                names['Ptask%s' % i].absolute_deadline = clock + \
                    names['Ptask%s' % i].period
                names['Ptask%s' % i].arrive_time = clock
                ready_queue_period.append(names['Ptask%s' % i])
                TotalPJobNumber += 1
        # 將在時間點clock抵達的aperiodic job加入到AQ中
        for i in range(len(aperiod_jobs)):
            names['Atask%s' % i] = AperiodTask(arrive_time=aperiod_jobs[i]
                                               [0], execution_time=aperiod_jobs[i][1], TID=i+1)
        for i in range(len(aperiod_jobs)):
            if clock == names['Atask%s' % i].arrive_time:
                if len(ready_queue_aperiod) == 0 and cus_deadline == clock:
                    ready_queue_aperiod.append(names['Atask%s' % i])
                    cus_deadline = ready_queue_aperiod[0].execution_time/0.2+clock
                else:
                    ready_queue_aperiod.append(names['Atask%s' % i])
        # 根據priority sort ready queue
        ready_queue_period.sort(key=sort_priority_EDF)
        # 判斷cus_deadline是否回充
        if cus_deadline == clock:

            budget = True
            if len(ready_queue_aperiod) != 0:
                cus_deadline = ready_queue_aperiod[0].execution_time/0.2 + clock
            else:
                cus_deadline = clock
        # priority最高的exe要減掉一\
        # readyP有且readyA也有
        if (len(ready_queue_period) != 0 and len(ready_queue_aperiod) != 0 and ready_queue_period[0].absolute_deadline <= cus_deadline):
            ready_queue_period[0].execution_time -= 1
            f.write("Time %s :Ptask %s\n" % (clock, ready_queue_period[0].TID))
            if ready_queue_period[0].execution_time == 0:
                TotalPResponseTime += clock-ready_queue_period[0].arrive_time
                del ready_queue_period[0]
                FinishedPJobNumber += 1
        elif (len(ready_queue_period) != 0 and len(ready_queue_aperiod) != 0 and ready_queue_period[0].absolute_deadline > cus_deadline):
            if budget == True:
                ready_queue_aperiod[0].execution_time -= 1
                f.write("Time %s :Atask %s cus_deadline :%d\n" %
                        (clock, ready_queue_aperiod[0].TID, cus_deadline))
                if ready_queue_aperiod[0].execution_time == 0:
                    TotalAResponseTime += clock - \
                        ready_queue_aperiod[0].arrive_time
                    del ready_queue_aperiod[0]
                    budget = False
                    FinishedAJobNumber += 1
                    if len(ready_queue_aperiod) != 0 and clock == cus_deadline:
                        cus_deadline = ready_queue_aperiod[0].execution_time/0.2+clock
            else:
                ready_queue_period[0].execution_time -= 1
                f.write("Time %s :Ptask %s\n" %
                        (clock, ready_queue_period[0].TID))
                if ready_queue_period[0].execution_time == 0:
                    TotalPResponseTime += clock - \
                        ready_queue_period[0].arrive_time
                    del ready_queue_period[0]
                    FinishedPJobNumber += 1

        # readyP有readyA沒有
        elif len(ready_queue_period) != 0 and len(ready_queue_aperiod) == 0:
            ready_queue_period[0].execution_time -= 1
            f.write("Time %s :Ptask %s\n" % (clock, ready_queue_period[0].TID))
            if ready_queue_period[0].execution_time == 0:
                TotalPResponseTime += clock-ready_queue_period[0].arrive_time
                del ready_queue_period[0]
                FinishedPJobNumber += 1
        # readyP沒有readyA有
        elif len(ready_queue_period) == 0 and len(ready_queue_aperiod) != 0 and budget == True:
            ready_queue_aperiod[0].execution_time -= 1
            f.write("Time %s :Atask %s\n" %
                    (clock, ready_queue_aperiod[0].TID))
            if ready_queue_aperiod[0].execution_time == 0:
                TotalAResponseTime += clock-ready_queue_aperiod[0].arrive_time
                del ready_queue_aperiod[0]
                budget = False
                FinishedAJobNumber += 1
                if len(ready_queue_aperiod) != 0 and clock == cus_deadline:
                    cus_deadline = ready_queue_aperiod[0].execution_time/0.2+clock
        # 兩個都沒有jobs
        else:
            f.write("Time %s : No Task\n" % clock)

        clock += 1

    print("Missed Jobs = %d\n" % MissPJobNumber)
    print("Sum of jobs = %d\n" % TotalPJobNumber)
    print("Miss_rate = %.2f\n" % (MissPJobNumber/TotalPJobNumber))
    print("FinishedAJobNumber = %d\n" % FinishedAJobNumber)
    print("Average_Reponse_Time = %.2f\n" %
          (TotalAResponseTime/FinishedAJobNumber))
    f.write("Missed Jobs = %d\n" % MissPJobNumber)
    f.write("Sum of jobs = %d\n" % TotalPJobNumber)
    f.write("Miss_rate = %.2f\n" % (MissPJobNumber/TotalPJobNumber))
    f.write("FinishedAJobNumber = %d\n" % FinishedAJobNumber)
    f.write("Average_Reponse_Time = %.2f\n" %
          (TotalAResponseTime/FinishedAJobNumber))

f = open("0_8_CUS.txt", mode="w")
print("cus_test8.txt\n")
CUS("cus_test8.txt", "aperodic.txt",f)
f.close

f = open("0_9_CUS.txt", mode="w")
print("cus_test9.txt\n")
CUS("cus_test9.txt", "aperodic.txt",f)
f.close
