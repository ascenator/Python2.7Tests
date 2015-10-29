import timeit
import numpy as np
import multiprocessing

# setup
low = -100
high = 100
samples = 1000000
lst = list(np.random.randint(low, high, samples))


def closest_to_average_jim_wood(xs):
    avg = sum(xs)/len(xs)
    min_diff = None
    closest = None
    for i in xs:
        diff = abs(avg - i)
        if min_diff is None or diff < min_diff:
            min_diff = diff
            closest = i
    return closest


def closest_to_average_jim_wood_rewritten(xs):
    avg = sum(xs)/len(xs)
    min_diff = xs[0]
    closest = xs[0]
    for i in xs:
        diff = abs(avg - i)
        if diff < min_diff:
            min_diff = diff
            closest = i
    return closest


def closest_to_average_niescior(xs):
    avg = sum(xs)/len(xs)
    closest = 0
    for i in xs:
        diff = abs(avg - i)
        if diff < abs(avg - closest):
            closest = i
    return closest


def closest_to_average_bothwell(lst):
    avg = sum(lst) / len(lst)
    return min(lst, key = lambda x: abs(avg - x))


def closest_to_average_ascenator(xs):
    avg = sum(xs)/len(xs)
    return reduce(lambda x, y: x if (abs(x - avg) < abs(y - avg)) else y, xs)

def closest_to_average_ascenator_worker(q, xs, avg):
    q.put(reduce(lambda x, y: x if (abs(x - avg) < abs(y - avg)) else y, xs))

def parallel(xs):
    queue = multiprocessing.Queue()
    avg = sum(xs)/len(xs)

    num_threads = 4
    worker = []

    low = 0
    high = len(xs)/num_threads

    for i in range(0, num_threads):
        worker.append(multiprocessing.Process(target=closest_to_average_ascenator_worker, args=(queue, xs[0:len(xs)/4], avg)))
        worker[i].start()
        low += len(xs)/num_threads
        high += len(xs)/num_threads

    for i in range(0, num_threads):
        worker[i].join()

    result_list = []

    while not queue.empty():
        result_list.append(queue.get())

    closest_to_average_ascenator_worker(queue, result_list, avg)

    return queue.get()

#print parallel(lst)
#print closest_to_average_ascenator(lst)
#print closest_to_average_bothwell(lst)
#print closest_to_average_jim_wood(lst)


time_jim_wood = timeit.timeit("closest_to_average_jim_wood(lst)",
                                "from __main__ import closest_to_average_jim_wood, lst",
                                number=10)

time_jim_wood_rewritten = timeit.timeit("closest_to_average_jim_wood_rewritten(lst)",
                                "from __main__ import closest_to_average_jim_wood_rewritten, lst",
                                number=10)

time_niescoir = timeit.timeit("closest_to_average_niescior(lst)",
                                "from __main__ import closest_to_average_niescior, lst",
                                number=10)

time_bothwell = timeit.timeit("closest_to_average_bothwell(lst)",
                                "from __main__ import closest_to_average_bothwell, lst",
                                number=10)

time_ascenator = timeit.timeit("closest_to_average_ascenator(lst)",
                                "from __main__ import closest_to_average_ascenator, lst",
                                number=10)

time_ascenator_parallel = timeit.timeit("parallel(lst)",
                                "from __main__ import parallel, lst",
                                number=10)

print("time_jim_wood:             {0:.5f}".format(time_jim_wood))
print("time_jim_wood_rewritten:   {0:.5f}".format(time_jim_wood_rewritten))
print("time_niescior:             {0:.5f}".format(time_niescoir))
print("time_bothwell:             {0:.5f}".format(time_bothwell))
print("time_ascenator:            {0:.5f}".format(time_ascenator))
print("time_ascenator_parallel:   {0:.5f}".format(time_ascenator_parallel))