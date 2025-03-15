# coding=utf-8
# date: 20250225
# author: Chenhao Cui
# email: 3313398924@qq.com
# description: design two different adaptive cluster algorithm and compare time consumption.
# algorithm: For any x belonging to list A, if |x-y| <= step, then y belongs to the same list A.

# library
from typing import List,Tuple
import numpy as np
import warnings
import copy
warnings.filterwarnings("ignore")
import time
import matplotlib as mpl
mpl.use("TKAgg")
import matplotlib.pyplot as plt
# modules

# method1
class cluster_v1:
    """
    Algorithm1. Its time complexity is O(sorted) + O(n^2).

    Attributes:
        step: int.
    
    Methods:
        cluster: split a list to several sublist adaptively.
        run: main program
    """
    def __init__(self,step: int) -> None:
        """
        initialize class cluster_v1
        param step: int
        return None
        """
        self.step = step
        return None
    
    def cluster(self, x: List) -> Tuple:
        """
        split a list to several sublist adaptively.
        param x: a list.
        return: (results_list,index_list).
        """
        drop_index = []
        r = []
        a = x[0]
        r.append(a)
        low_threshold = min(r) - self.step
        high_threshold = max(r) + self.step 
        i = 1
        while i <= len(x) - 1:
            b = x[i]
            if low_threshold <= b and b<= high_threshold:
                r.append(b)
                low_threshold = min(r) - self.step
                high_threshold = max(r) + self.step
                i = i + 1
            else:
                drop_index.append(i)
                i = i + 1
                continue
        return r,drop_index

    def run(self, x: List) -> List:
        """
        cluster x based on loc step
        param x: a list.
        return: a list that contains different sublists.
        """
        if len(x) <= 1:
            return x
        else:
            results = []
            y = sorted(x)
            while len(y) > 0:
                r,drop_index = self.cluster(y)
                results.append(r)
                if len(drop_index) > 0:
                    y = np.array(y)[drop_index].tolist()
                else:
                    break
            return results


# method2
class cluster_v2:
    """
    Algorithm2. Its time complexity is O(sorted) + O(n).

    Attributes:
        step: int.
    
    Methods:
        cluster: split a list to several sublist adaptively.
        run: main program
    """
    def __init__(self,step: int) -> None:
        """
        initialize class cluster_v2
        param step: int
        return None
        """
        self.step = step
        return None
    
    def cluster(self,x: List,start_index: int) -> Tuple:
        """
        cluster x based on loc step
        param x: a list.
        param start_index: int
        return: (results_list,index_list).
        """
        r = []
        a = x[start_index]
        r.append(a)
        low_threshold = min(r) - self.step
        high_threshold = max(r) + self.step
        end_index = -1
        for i in range(start_index+1,len(x)):
            b = x[i]
            if low_threshold <= b and b <= high_threshold:
                r.append(b)
                low_threshold = min(r) - self.step
                high_threshold = max(r) + self.step
            else:
                end_index = i
                break
        return r,end_index


    def run(self,x: List) -> List:
        """
        cluster x based on step
        param x: a list.
        param start_index: int
        return: a list that contains different sublists.
        """
        if len(x) <= 1:
            return x
        else:
            x = sorted(x)
            results = []
            start_index = 0
            r,end_index = self.cluster(x,start_index)
            results.append(r)
            while end_index != -1:
                start_index = end_index
                r,end_index = self.cluster(x,start_index)
                results.append(r)
            return results

if __name__ == "__main__":
    # compare time consumption
    step = 2
    n_list = [1000,5000,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000]
    m1 = cluster_v1(step)
    m2 = cluster_v2(step)
    m1_t, m2_t = [], []
    for i in range(len(n_list)):
        n = n_list[i]
        test_list = [i for i in range(1,n,3)]

        d0 = time.time()
        a = m1.run(test_list)
        d1 = time.time()
        

        d2 = time.time()
        b = m2.run(test_list)
        d3 = time.time()

        if a == b:
            print("the two different algorithm have same results. Then, we save time consumption.")
            m1_t.append(d1-d0)
            m2_t.append(d3-d2)
    # plot
    plt.rcParams["font.family"] = "Times New Roman"
    plt.figure(figsize=(14,6))
    plt.plot(m1_t,color="red",label="algorithm1")
    plt.plot(m2_t,color="blue",label="algorithm2")
    plt.xticks(list(range(len(n_list))),[str(i) for i in n_list])
    plt.xlabel("data size")
    plt.ylabel("time consumption(second)")
    plt.title("time consumption for different algorithm")
    plt.tight_layout()
    plt.legend(loc="upper left")
    plt.show()
