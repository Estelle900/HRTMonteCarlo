import numpy as np
import matplotlib.pyplot as plt

#assume normal distribution, 96.56–104.97% (90% CI) AUC, 81.68–95.13% (90% CI) geometric mean cipro/androcur, mean androcur=175ng/mL, mean ciproterone=150ng/mL, 80-125% (90% CI) Cmax
#Cmax androcur calculations: ratio mu=0.88405,sigma=0.0408851, geom mean cipro,androcur: 162.019

def simulate(dose,intervals):
    repeat=sum(intervals)
    for i in range(len(intervals)-1,0,-1):
        intervals[i]=sum(intervals[:i+1])
    l=[dose/100*162.019/np.random.normal(loc=0.88405,scale=0.0408851)**0.5]
    for i in range(repeat*5):
        if l[-1]>100:
            l.append(l[-1]*0.5**(6/np.random.normal(loc=8,scale=1)))
        elif l[-1]>50:
            l.append(l[-1]*0.5**(6/np.random.normal(loc=40,scale=3)))
        elif l[-1]>20:
            l.append(l[-1]*0.5**(6/(np.random.normal(loc=96,scale=12)-36)))
        else:
            l.append(l[-1]*0.8**(6/np.random.normal(loc=96,scale=24)))
        if (i%repeat)+1 in intervals:
            l[-1]+=dose/100*162.019/np.random.normal(loc=0.88405,scale=0.0408851)**0.5
    plt.plot(np.arange(repeat*5+1)*6,l,'r',alpha=0.1)
    #plt.show()
    return [min(l),max(l),np.mean(l)],l
#conservative estimate unsafe dosage 25mg/day
#min,max,mean: (37.26690717169299, 107.7282828387695, 72.4945087102889)

#comparison side effects intolerable for first 12h at 37.5mg
#56.44,62.84,58.50 #mean of the lowest point

def check(dose,intervals):
    r=sum(intervals)
    checker=[]
    for i in range(100):
        m,l=simulate(dose,intervals.copy())
        checker.append(l)
    #plt.plot(np.arange(r)/4,np.min(checker,axis=0)[-r:])
    #plt.plot(np.arange(r)/4,np.max(checker,axis=0)[-r:])
    #plt.plot(np.arange(r)/4,np.mean(checker,axis=0)[-r:])
    plt.show()
    #print(np.min(checker,axis=0),np.max(checker,axis=0),np.mean(checker,axis=0))

#reg 1: 12.5 every 3-4 days
check(12.5,[16,12])

#reg 2: 12.5 every 2 days
check(12.5,[8,8,8])

#reg 3: 25/week
check(25,[42,42])

#reg 4: 25 every 3-4 days
check(25,[16,12])

#comparison 1: 3.125/day (physiological [progesterone])
check(3.125,[4,4,4,4,4,4,4])

