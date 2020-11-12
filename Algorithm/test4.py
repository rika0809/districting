import multiprocessing


a = [1, 2, 3, 4]

chunks = [a[i::2] for i in range(2)]


def append_neighbor(list, share_var, index, share_lock):
    n = []
    for i in range(len(list)):
        ad = []
        for j in range(len(a)):
            if (list[i] + a[j]) % 2 == 1:
                ad.append(a[j])
        n.append(ad)
    share_lock.acquire()
    share_var[index] = n
    share_lock.release()

# 不能将共享变量和共享锁定义成全局变量然后通过global引用那样会报错，只能传过来
def sub_process(process_name,share_var,share_lock):
    # 获取锁
    share_lock.acquire()
    share_var.append(process_name)
    # 释放锁
    share_lock.release()
    for item in share_var:
        print(f"{process_name}-{item}")
    pass

def main_process():
    # 单个值声明方式。typecode是进制类型，C写法和Python写法都可以，见下方表格；value是初始值。
    # 这种单值形式取值赋值需要通过get()/set()方法进行，不能直接如一般变量那样取值赋值
    # share_var = multiprocessing.Manager().Value(typecode, value)
    # 数组声明方式。typecode是数组变量中的变量类型，sequence是数组初始值
    # share_var = multiprocessing.Manager().Array(typecode, sequence)
    # 字典声明方式
    # share_var = multiprocessing.Manager().dict()
    # 列表声明方式
    share_var = multiprocessing.Manager().dict()


    # 声明一个进程级共享锁
    # 不要给多进程传threading.Lock()或者queue.Queue()等使用线程锁的变量，得用其进程级相对应的类
    # 不然会报如“TypeError: can't pickle _thread.lock objects”之类的报错
    share_lock = multiprocessing.Manager().Lock()
    process_list = []

    process_name = "process 1"
    tmp_process = multiprocessing.Process(target=append_neighbor, args=(chunks[0], share_var, 0, share_lock))
    process_list.append(tmp_process)

    process_name = "process 2"
    tmp_process = multiprocessing.Process(target=append_neighbor, args=(chunks[1], share_var, 1, share_lock))
    process_list.append(tmp_process)

    for process in process_list:
        process.start()
    for process in process_list:
        process.join()

    print(share_var)

if __name__ == "__main__":
    main_process()