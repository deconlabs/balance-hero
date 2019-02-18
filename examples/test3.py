"""
멀티프로세싱 내에서 하나의 공통된 딕셔너리를 공유하는 예제
Manager를 이용해서 만든 dictionary는 Manager가 close될 때 사라지므로
copy() 메소드를 이용해서 따로 빼줘야한다
"""


from multiprocessing import Process, Manager

procs = []


def f(s_a_dict, i):
    s_a_dict[i] = {"id": i}


with Manager() as manager:
    s_a_dict = manager.dict()
    procs = []
    for i in range(10):
        proc = Process(target=f, args=(s_a_dict, i))
        procs.append(proc)
        proc.start()

    for i in range(10):
        procs[i].join()

    my_dict = s_a_dict.copy()

print(my_dict)
