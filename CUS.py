
import re


class Mytask():
    def __init__(self, phase_time, period, relative_deadline, execution_time, absolute_deadline):
        self.phase_time = phase_time
        self.period = period
        self.relative_deadline = relative_deadline
        self.execution_time = execution_time
        self.absolute_deadline = absolute_deadline


class Node():
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList():
    def __init__(self):
        self.head = None


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


def sort_priority(e):
    return e.absolute_deadline


def EDF(filename):
    jobs = Readfile(filename)
    clock = 0
    misstask = 0
    LCM = 1
    MaxPH = 0
    names = globals()
    ready_queue = []
    for i in range(len(jobs)):
        names['task%s' % i] = Mytask(phase_time=jobs[i][0], period=jobs[i]
                                     [1], relative_deadline=jobs[i][2], execution_time=jobs[i][3], absolute_deadline=0)
        LCM = computeLcm(LCM, jobs[i][1])
        if MaxPH < jobs[i][0]:
            MaxPH = jobs[i][0]
    while clock < LCM+MaxPH:

        # 1.判斷readyqueue是否有missdeadline的job
        ready_length = len(ready_queue)
        for i in range(ready_length):
            print(i)
            if ready_queue[i].absolute_deadline-clock-ready_queue[i].execution_time < 0:
                del ready_queue[i]
                ready_length -= 1
                misstask += 1
            if i == ready_length-1:
                break

        # 2.判斷task是否進來 並加入readyqueue
        for i in range(len(jobs)):
            if (clock-names['task%s' % i].phase_time) % names['task%s' % i].period == 0:
                names['task%s' % i].absolute_deadline = clock + \
                    names['task%s' % i].relative_deadline
                ready_queue.append(names['task%s' % i])
        # 3.根據priority sort ready queue
        ready_queue.sort(key=sort_priority)
        print("第%s個" % clock)

        for i in range(len(ready_queue)):
            print(ready_queue[i].absolute_deadline)
        clock += 1
        # print(clock)

    print("misstask = %s"%misstask)


for i in range(1, 2):
    print("test%s：" % i)
    EDF("test%s.txt" % i)
    
