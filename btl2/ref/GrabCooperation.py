from math import inf,sqrt
from random import randint
from functools import reduce
from copy import deepcopy
class Invoice:
    def __init__(self,id,coord,worth):
        self.id=id
        self.coord=coord
        self.worth=worth
    
    def __repr__(self):
        return f'Invoice(id={self.id},coord={self.coord},worth={self.worth})'

class Shipper:
    def __init__(self,id,grabCoord):
        self.id=id
        self.profit=-10
        self.invoices=[Invoice(id='Fake',coord=grabCoord,worth=0)]
    
    def __repr__(self):
        return f'Shipper(id={self.id},profit={self.profit},invoices={self.invoices})'

M=10
N=50

grabCoord=(10,10)
invoices=[Invoice(id=i,coord=(randint(0,N*100),randint(0,N*100)),worth=randint(0,N*100)) for i in range(N)]
shippers=[Shipper(id=i,grabCoord=grabCoord) for i in range(M)]
cachedDist=dict()

def distance(a,b):
    cacheKey=f'{a}{b}'
    if cacheKey in cachedDist:
        return cachedDist[cacheKey]
    else:
        cacheKey=f'{b}{a}'
        if cacheKey in cachedDist:
            return cachedDist[cacheKey]
    dist=sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))
    cachedDist[f'{a}{b}']=dist
    return dist

def iterativeAssignRandom():

    def assign(shipper,invoice,profitGained):
        shipper.profit+=profitGained
        shipper.invoices.append(invoice)
        for other in [*range(shipper.id),*range(shipper.id+1,M)]:
            tableDeltaProfit[shipper.id][other]+=profitGained
            tableDeltaProfit[other][shipper.id]-=profitGained
            
    global invoices,shippers
    invoices=deepcopy(invoices)
    shippers=deepcopy(shippers)
    tableDeltaProfit=[[0 for i in range(M)] for i in range(M)]

    for invoice in invoices:
        randomShipper=randint(0,M-1)
        shipper=shippers[randomShipper]
        profitGained=invoice.worth-distance(invoice.coord,shipper.invoices[-1].coord)/2
        assign(shipper,invoice,profitGained)

    print(f'Iteratively Assign Random: {int(reduce(lambda x,y: x+sum([abs(element) for element in y]),tableDeltaProfit,0)/2)}')

def iterativeAssignBest():

    def assign(shipper,invoice,profitGained):
        shipper.profit+=profitGained
        shipper.invoices.append(invoice)
        for other in [*range(shipper.id),*range(shipper.id+1,M)]:
            tableDeltaProfit[shipper.id][other]+=profitGained
            tableDeltaProfit[other][shipper.id]-=profitGained

    global invoices,shippers
    invoices=deepcopy(invoices)
    shippers=deepcopy(shippers)
    tableDeltaProfit=[[0 for i in range(M)] for i in range(M)]
    for invoice in invoices:
        bestShipper=None
        leastUneqIncr=inf
        bestProfitGained=None
        for shipper in shippers:
            profitGained=invoice.worth-distance(invoice.coord,shipper.invoices[-1].coord)/2
            uneqIncr=0
            for other in [*range(shipper.id),*range(shipper.id+1,M)]:
                uneqIncr+=abs(tableDeltaProfit[shipper.id][other]+profitGained)-abs(tableDeltaProfit[shipper.id][other])
            if uneqIncr<leastUneqIncr:
                leastUneqIncr=uneqIncr
                bestShipper=shipper
                bestProfitGained=profitGained
        assign(shippers[bestShipper.id],invoice,bestProfitGained)

    print(f'Iteratively Assign Best: {int(reduce(lambda x,y: x+sum([abs(element) for element in y]),tableDeltaProfit,0)/2)}')

def sortFirstIterativeAssignBest():

    def assign(shipper,invoice,profitGained):
        shipper.profit+=profitGained
        shipper.invoices.append(invoice)
        for other in [*range(shipper.id),*range(shipper.id+1,M)]:
            tableDeltaProfit[shipper.id][other]+=profitGained
            tableDeltaProfit[other][shipper.id]-=profitGained
            
    global invoices,shippers
    invoices=deepcopy(invoices)
    shippers=deepcopy(shippers)
    tableDeltaProfit=[[0 for i in range(M)] for i in range(M)]

    for i in range(N-2):
        nearestInvoice=i+1
        nearestDist=distance(invoices[i].coord,invoices[i+1].coord)
        for j in range(i+2,N):
            if distance(invoices[i].coord,invoices[j].coord)<nearestDist:
                nearestDist=distance(invoices[i].coord,invoices[j].coord)
                nearestInvoice=j
        invoices[i+1],invoices[nearestInvoice]=invoices[nearestInvoice],invoices[i+1]

    for invoice in invoices:
        bestShipper=None
        leastUneqIncr=inf
        bestProfitGained=None
        for shipper in shippers:
            profitGained=invoice.worth-distance(invoice.coord,shipper.invoices[-1].coord)/2
            uneqIncr=0
            for other in [*range(shipper.id),*range(shipper.id+1,M)]:
                uneqIncr+=abs(tableDeltaProfit[shipper.id][other]+profitGained)-abs(tableDeltaProfit[shipper.id][other])
            if uneqIncr<leastUneqIncr:
                leastUneqIncr=uneqIncr
                bestShipper=shipper
                bestProfitGained=profitGained
        assign(shippers[bestShipper.id],invoice,bestProfitGained)

    print(f'Sort First Iteratively Assign Best: {int(reduce(lambda x,y: x+sum([abs(element) for element in y]),tableDeltaProfit,0)/2)}')

def sortFirstIterativeAssignBest2():

    def assign(shipper,invoice,profitGained):
        shipper.profit+=profitGained
        shipper.invoices.append(invoice)
        for other in [*range(shipper.id),*range(shipper.id+1,M)]:
            tableDeltaProfit[shipper.id][other]+=profitGained
            tableDeltaProfit[other][shipper.id]-=profitGained
            
    global invoices,shippers
    invoices=deepcopy(invoices)
    shippers=deepcopy(shippers)
    tableDeltaProfit=[[0 for i in range(M)] for i in range(M)]

    for i in range(N-1):
        bestInvoice=i+1
        bestReplicaProfit=invoices[i].worth-distance(invoices[i].coord,grabCoord)/2
        for j in range(i+1,N):
            if invoices[j].worth-distance(invoices[j].coord,grabCoord)/2>bestReplicaProfit:
                bestReplicaProfit=invoices[j].worth-distance(invoices[j].coord,grabCoord)/2
                bestInvoice=j
        invoices[i+1],invoices[bestInvoice]=invoices[bestInvoice],invoices[i+1]

    for invoice in invoices:
        bestShipper=None
        leastUneqIncr=inf
        bestProfitGained=None
        for shipper in shippers:
            profitGained=invoice.worth-distance(invoice.coord,shipper.invoices[-1].coord)/2
            uneqIncr=0
            for other in [*range(shipper.id),*range(shipper.id+1,M)]:
                uneqIncr+=abs(tableDeltaProfit[shipper.id][other]+profitGained)-abs(tableDeltaProfit[shipper.id][other])
            if uneqIncr<leastUneqIncr:
                leastUneqIncr=uneqIncr
                bestShipper=shipper
                bestProfitGained=profitGained
        assign(shippers[bestShipper.id],invoice,bestProfitGained)

    print(f'Sort First Iteratively Assign Best 2: {int(reduce(lambda x,y: x+sum([abs(element) for element in y]),tableDeltaProfit,0)/2)}')

def sortFirstIterativeAssignBest3():

    def assign(shipper,invoice,profitGained):
        shipper.profit+=profitGained
        shipper.invoices.append(invoice)
        for other in [*range(shipper.id),*range(shipper.id+1,M)]:
            tableDeltaProfit[shipper.id][other]+=profitGained
            tableDeltaProfit[other][shipper.id]-=profitGained
            
    global invoices,shippers
    invoices=deepcopy(invoices)
    shippers=deepcopy(shippers)
    tableDeltaProfit=[[0 for i in range(M)] for i in range(M)]

    for i in range(N-1):
        bestInvoice=i+1
        bestReplicaProfit=invoices[i].worth
        for j in range(i+1,N):
            if invoices[j].worth>bestReplicaProfit:
                bestReplicaProfit=invoices[j].worth
                bestInvoice=j
        invoices[i+1],invoices[bestInvoice]=invoices[bestInvoice],invoices[i+1]

    for invoice in invoices:
        bestShipper=None
        leastUneqIncr=inf
        bestProfitGained=None
        for shipper in shippers:
            profitGained=invoice.worth-distance(invoice.coord,shipper.invoices[-1].coord)/2
            uneqIncr=0
            for other in [*range(shipper.id),*range(shipper.id+1,M)]:
                uneqIncr+=abs(tableDeltaProfit[shipper.id][other]+profitGained)-abs(tableDeltaProfit[shipper.id][other])
            if uneqIncr<leastUneqIncr:
                leastUneqIncr=uneqIncr
                bestShipper=shipper
                bestProfitGained=profitGained
        assign(shippers[bestShipper.id],invoice,bestProfitGained)

    print(f'Sort First Iteratively Assign Best 3: {int(reduce(lambda x,y: x+sum([abs(element) for element in y]),tableDeltaProfit,0)/2)}')

iterativeAssignRandom()

iterativeAssignBest()

sortFirstIterativeAssignBest()

sortFirstIterativeAssignBest2()

sortFirstIterativeAssignBest3()





