import multiprocessing
from multiprocessing import Manager
a = [1,2,3,4]

chunks = [a[i::2] for i in range(2)]


def append_neighbor(list, b):
    n = []
    for i in range(len(list)):
        ad =[]
        for j in range(len(a)):
            if (list[i]+a[j])%2 == 1:
                ad.append(a[j])
        n.append(ad)
    b.append(n)



if __name__ == "__main__":
    b = Manager().list()
    jobs = []
    for i in range(2):
        p = multiprocessing.Process(target=append_neighbor, args=(chunks[i], b))
        jobs.append(p)
        p.start()
    for p in jobs:
        p.join()
    print(b)