from project import *
PROJECTS = []

def main():
    #PROJECTS = []
    while True:
        cls()
        print("MAIN MENU")
        print("1: Create new project")
        if PROJECTS:
            print("2: Select project")
            print("3: Delete project")

        print("x: Exit")
        selection = input("Selection:")
        if str(selection) == 'x':
            return
        elif str(selection) == "1":
            name = input("Enter project name:")
            p = Project(name)
            PROJECTS.append(p)
        elif str(selection) == "2" and PROJECTS:
            project_selection_menu()
        elif str(selection) == "3" and PROJECTS:
            project_deletion_menu()
        else:
            print("Invalid input.  Please try again.")


def project_selection_menu():
    while True:
        cls()
        print("PROJECT SELECTION MENU")
        print("Select a project:")

        for p in PROJECTS:
            print("{:<3}: {}".format(PROJECTS.index(p) + 1, p.name))
        selection = input("Selection (x to return to the main menu):")
        if str(selection) == "x":
            return
        elif selection.isnumeric() and 1 <= int(selection) <= len(PROJECTS):
            project = PROJECTS[int(selection) - 1]
            project_menu(project)
        else:
            input("Invalid input. Press <Enter> to try again.")


def project_deletion_menu():
    while True:
        cls()
        print("PROJECT DELETION MENU")
        print("Select a project to delete:")

        for p in PROJECTS:
            print("{:<3}: {}".format(PROJECTS.index(p) + 1, p.name))
        selection = input("Selection (x to return to the main menu):")
        if str(selection) == "x":
            return
        if input("Are you sure? (y/n)") == "y":
            try:
                PROJECTS.pop(int(selection) - 1)
                print("Project deleted.")
                return
            except:
                print("Invalid input, try again.")


def project_menu(project):
    while True:
        cls()
        print("PROJECT MENU")
        print("CURRENT PROJECT: {}".format(project.name))

        print("1: View Project Information")
        print("2: Change Project Name")
        print("3: Create task")
        if project.tasks:
            print("4: Delete task")
            print("5: View all tasks")
            print("6: View/Modify a task")
        selection = input("Selection (x to return to the main menu):")
        if str(selection) == "x":
            return
        #####
        # VIEW PROJECT INFO
        #####
        elif str(selection) == "1":
            cls()
            print("{:<13}: {}".format("NAME", project.name))
            print("{:<13}: {}".format("DURATION", project.duration))
            print("{:<13}: {}".format("NUM OF TASKS", len(project.tasks)))
            print("{:<13}: ".format("CRITICAL PATH(S)"))
            for path in project.critical_path:
                print("->".join([str(task.task_id) for task in path]))
            print_tasks(project.tasks)
            input("Press <Enter> to continue.")

        #####
        # CHANGE PROJECT NAME
        #####
        elif str(selection) == "2":
            cls()
            print("Current project name: {}".format(project.name))
            project.name = input("New project name:")

        #####
        # CREATE A NEW TASK
        #####
        elif str(selection) == "3":
            create_task(project)

        #####
        # DELETE A TASK
        #####
        elif str(selection) == "4" and project.tasks:
            delete_task_menu(project)

        #####
        # VIEW ALL TASKS
        #####
        elif str(selection) == "5" and project.tasks:
            cls()
            print_tasks(project.tasks)
            input("Press <Enter> to continue.")

        #####
        # SELECT A TASK
        #####
        elif str(selection) == "6" and project.tasks:
            select_task(project)


def print_tasks(tasks):
    print("{:^28}".format("TASKS"))
    print("{:<3} {:<15} {:>8}".format("ID", "NAME", "DURATION"))
    for task in tasks:
        print("{:<3} {:<15} {:>8}".format(task.task_id, task.name[0:15], task.duration))


def create_task(project):
    cls()
    name = input("Task name:")
    while True:
        duration = input("Task duration:")
        if duration.isnumeric() and int(duration) >= 0:
            project.new_task(str(name), int(duration))
            return
        else:
            input("Invalid input: duration must be a positive integer. Press <Enter> to continue.")
            continue
    return


def select_task(project):
    while True:
        cls()
        print("TASK SELECTION MENU")
        task = task_selection(project)
        if task == "x":
            return
        else:
            task_menu(project, task)
    return


def task_selection(project):
    while True:
        cls()
        print("    {:<20}".format("TASK NAME"))
        for task in project.tasks:
            print("{: <2}: {}".format(task.task_id, task.name[:20]))
        selection = input("Selection (x to return to the previous menu):")
        if str(selection) == "x":
            return "x"
        try:
            task = project.tasks[int(selection)]
            return task
        except:
            input("Invalid entry. Please try again. (Press <Enter> to continue)")


def task_menu(project, task):
    while True:
        cls()
        #####
        # View Task Info
        #####
        print("{:<3} {:<}".format("ID", "NAME"))
        print("{:<3} {:<}".format(task.task_id, task.name))
        print("DURATION: {}".format(task.duration))
        print("ES: {:>5}   EF: {:>5}".format(task.early_start, task.early_finish))
        print("LS: {:>5}   LF: {:>5}".format(task.late_start, task.late_finish))
        print("PREVIOUS TASK(S):")
        if not task.prev_tasks:
            print("NONE")
        else:
            print("    {:<3} {:<}".format("ID", "NAME"))
            for t in task.prev_tasks:
                print("    {:<3} {:<}".format(t.task_id, t.name))
        print("NEXT TASK(S):")
        if not task.next_tasks:
            print("NONE")
        else:
            print("    {:<3} {:<}".format("ID", "NAME"))
            for t in task.next_tasks:
                print("    {:<3} {:<}".format(t.task_id, t.name))
        print("Menu:")
        print("1: Change task name")
        print("2: Change duration")
        print("3: Add previous task")
        print("4: Disconnect a task")
        selection = input("Selection (x to return to the previous menu):")
        if selection == "x":
            return
        #####
        # NEW TASK NAME
        #####
        elif str(selection) == "1":
            new_name = input("Enter a new task name:")
            if new_name:
                task.name = new_name
        #####
        # NEW TASK DURATION
        #####
        elif str(selection) == "2":
            new_duration = input("Enter a new task duration:")
            if new_duration.isnumeric():
                task.duration = int(new_duration)
                project.update()
        #####
        # NEW PREVIOUS TASK
        #####
        elif str(selection) == "3":
            cls()
            print_tasks(project.tasks)
            prev_task_id = input("Select the ID of the task you would like to connect to {}?:".format(task.name))
            project.set_prev_task(task, project.get_task(prev_task_id))
            project.update()
        #####
        # DISCONNECT TASKS
        #####
        elif str(selection) == "4":
            cls()
            print_tasks(task.prev_tasks + task.next_tasks)
            disconnect = input("Which tasks would you like to disconnect?:")
            if disconnect.isnumeric():
                project.disconnect_tasks(task, project.get_task(int(disconnect)))


def delete_task_menu(project):
    while True:
        cls()
        print("DELETE A TASK")
        task = task_selection(project)
        if task == "x":
            return
        else:
            verify = input("Are you sure you want to delete {}? (y/n):".format(task.name))
            if str(verify) == "y":
                project.del_task(task)
                return


def cls():
    print("\n" * 20)


def testing():
    p = Project("TEST PROJECT")
    t0 = p.new_task("Task 0", 1)
    t1 = p.new_task("Task 1", 2)
    t2 = p.new_task("Task 2", 3)
    t3 = p.new_task("Task 3", 4)
    t4 = p.new_task("Task 4", 5)
    p.set_prev_task(t1, t0)
    p.set_prev_task(t3, t1)
    p.set_prev_task(t2, t0)
    p.set_prev_task(t3, t2)
    PROJECTS.append(p)


if __name__ == "__main__":
    testing()
    main()