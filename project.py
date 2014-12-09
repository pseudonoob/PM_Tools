from collections import deque
from random import randint
class Project():

    def __init__(self, name):
        self.name = name
        self.tasks = []
        self.TASK_ID = 0
        self.critical_path = []

    def new_task(self, name, duration):
        task = Task(name, duration)
        self.tasks.append(task)
        task.task_id = self.TASK_ID
        if len(self.tasks) == 1:
            self.duration = task.duration
            self.critical_path.append(task)
        else:
            self.update()

        self.TASK_ID += 1

    def del_task(self, task):
        #TODO: Test del_task()
        for t in task.next_tasks:
            t.prev_tasks.remove(task)
        for t in task.prev_tasks:
            t.next_tasks.remove(task)
        for t in self.tasks:
            t.connected = t.connected - {task}
        self.tasks.remove(task)

    def set_prev_task(self, task, prev_task):
        task.add_prev_task(prev_task)
        self.update()

    def update(self):
        self.update_early_times()
        self.update_late_times()
        self.duration = max([t.late_finish for t in self.tasks])
        self.find_critical_path()

    def update_early_times(self):
        todo = deque()
        for task in self.tasks:
            if not task.prev_tasks:
                todo.append(task)
        while todo:
            task = todo.popleft()
            todo += [next for next in task.next_tasks if next not in todo]
            if task.prev_tasks:
                task.early_start = max(task.prev_tasks, key=lambda x: x.early_finish).early_finish + 1
            else:
                task.early_start = 1
            task.early_finish = task.early_start + task.duration - 1

    def update_late_times(self):
        todo = deque()
        for task in self.tasks:
            if not task.next_tasks:
                todo.append(task)
        while todo:
            task = todo.popleft()
            todo += [prev for prev in task.prev_tasks if prev not in todo]
            if task.next_tasks:
                task.late_finish = min(task.next_tasks, key=lambda x: x.late_start).late_start - 1
            else:
                task.late_finish = max([t.early_finish for t in self.tasks])
            task.late_start = task.late_finish - task.duration + 1

            task.slack = task.late_start - task.early_start

    def find_critical_path(self):
        self.critical_path = []
        starts = [t for t in self.tasks if not t.prev_tasks]
        for task in starts:
            path = self.rec_path(task)
            if path:
                self.critical_path = path

    def rec_path(self, task):
        if not task.next_tasks and task.slack == 0 and task.late_finish == self.duration:
            return [task]
        elif task.slack > 0:
            return
        else:
            for t in task.next_tasks:
                path = self.rec_path(t)
                if path:
                    return [task] + path
        return


class Task():

    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.prev_tasks = []
        self.next_tasks = []
        self.early_start = 1
        self.early_finish = duration
        self.late_start = 1
        self.late_finish = duration
        self.task_id = None
        self.slack = 0
        self.connected = {self}

    def add_prev_task(self, task):
        if type(task) == Task:
            if task in (self.connected & task.connected - {task}):
                print("These tasks are already connected.")
                return
            self.prev_tasks.append(task)
            task.next_tasks.append(self)
            self.connected = self.connected & task.connected
            return
        else:
            print("You can only add other tasks. You tried to add a {}".format(str(type(task))))
            return

    def add_next_task(self, task):

        if type(task) == Task:
            if task in (self.connected & task.connected - {task}):
                print("These tasks are already connected.")
                return
            self.next_tasks.append(task)
            task.prev_tasks.append(self)
            self.connected = self.connected & task.connected
            return
        else:
            print("You can only add other tasks. You tried to add a {}".format(str(type(task))))
            return

    def __str__(self):
        return "Name: {0}\nDuration: {1}".format(self.name, self.duration)

def Testing():

    p = create_test_project(10, 20, 2)
    print_project(p)

def create_test_project(num_tasks, max_len, max_prev):
    import random
    p = Project("Project")
    for i in range(num_tasks):
        p.new_task("Task {}".format(str(i)), randint(1, max_len))
        die = randint(0, 10) #Randomly select start tasks
        if die == 0 or len(p.tasks) == 1:
            continue
        else:
            for i in range(randint(1, max_prev)):
                prev = randint(0, len(p.tasks) - 2)
                p.set_prev_task(p.tasks[-1], p.tasks[prev])

    return p

def print_project(project):
    print("{:<5}{:<10}{:<5}{:<10}{:<5}{:<5}{:<5}{:<5}{:<5}".format("ID",    "Name",     "Dur.",
                                                                   "Prev",  "ES",       "EF",
                                                                   "LS",    "LF",       "Slack"))
    for t in project.tasks:
        prev = [x.task_id for x in t.prev_tasks]
        print("{:<5}{:<10}{:<5}{:<10}{:<5}{:<5}{:<5}{:<5}{:<5}".format(t.task_id,       t.name,         t.duration,
                                                                       str(prev),       t.early_start,  t.early_finish,
                                                                       t.late_start,    t.late_finish,  t.slack))
    print("Total project duration: {}".format(project.duration))

    print("Critical path: {}".format([task.task_id for task in project.critical_path]))

if __name__ == "__main__":
    Testing()