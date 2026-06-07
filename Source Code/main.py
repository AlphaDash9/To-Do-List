import datetime as d

class InvalidKeyError(Exception):
    print("Invalid code entered...")

def display_task_dictionary_generator(task_test):
    task_dict = {}
    final_test_string = task_test.replace("{", "")
    final_test_string = final_test_string.replace("}", "")
    
    keys = []
    for index, element in enumerate(final_test_string):
        if element == "\'":
            key_assume = final_test_string[index + 1 : index + 7]
            if key_assume.isdigit():
                keys.append(key_assume)
            else :
                key_assume = ""
        else :
            continue
    
    for element in keys :
        index_start = int(final_test_string.find(element)) + 10
        index_end = int(final_test_string.find("]", index_start))
        value_string = final_test_string[index_start : index_end]

        final_test_string = final_test_string.replace("\'", "")
        value = final_test_string[final_test_string.find(element) + 9 : final_test_string.find("]", final_test_string.find(element))] + ","
        value_list = list()
        value_string = ""
        for index, element1 in enumerate(value):
            if element1 == ",":
                value_list.append(value_string)
                value_string = ""
            else :
                value_string += element1
        task_dict[element] = value_list
    
    for keys, values in task_dict.items():
        print("Task Code -> ", keys, " :", "\n")
        print("\t", "Priority :", values[0].replace("[", ""), ", Date :", values[1].rstrip(), ", Deadline :", values[2].rstrip(), ", Task :", values[3][1:], "\n")

class Tasks_List :
    
    __Temporary_Dictionary = {}
    __Not_Completed_Tasks = {}
    __Completed_Tasks = {}
    
    def __init__(self, do_or_not=True):
        lines = []
        with open("data_list.txt", 'r') as file :
            for line in file :
                lines.append(line.rstrip())
        for string in lines :
            key = string[0:6]
            value = string[9:len(string)]
            if value in self.__Not_Completed_Tasks.values():
                continue
            self.__Not_Completed_Tasks[key] = value

    code = ""

    def list_gen(self, task_name, priority, deadline):
        date = d.datetime.now()
        nth = 0
        for i in self.__Not_Completed_Tasks.keys():
            nth += 1
        self.code = f"{priority}{date.year}{nth}"
        list_generated = [priority, d.datetime.now().strftime("%Y-%m-%d"), deadline, task_name]
        return list_generated

    def add_task(self, task_name, priority=1, deadline="Today"):
        self.__Not_Completed_Tasks[self.code] = self.list_gen(task_name, priority, deadline)
        return self.code

    def remove_task(self, code):
        if code in self.__Not_Completed_Tasks.keys():
            self.__Temporary_Dictionary[code] = self.__Not_Completed_Tasks[code]
            self.__Not_Completed_Tasks.pop(code)
        else :
            raise InvalidKeyError("Invalid code entered...")

    def update_task(self, code, task_name="Nothing", priority=1, deadline="Today"):
        self.__Not_Completed_Tasks[code] = self.list_gen(task_name, priority, deadline)
        return self.__Not_Completed_Tasks[code]
    
    def display_task_list(self, list_name):
        if list_name.upper() == "COMPLETED":
            return str(self.__Completed_Tasks)
        elif list_name.upper() == "NOT-COMPLETED":
            return str(self.__Not_Completed_Tasks)
        else :
            raise ValueError("Incorrect Task list name")

    def mark_done(self, code):
        self.__Completed_Tasks[code] = self.__Not_Completed_Tasks[code]
        self.__Not_Completed_Tasks.pop(code)

    def undo_task(self, code='0', action='r'):
        if action == 'u':
            self.__Not_Completed_Tasks[code] = self.__Completed_Tasks[code]
            self.__Completed_Tasks.pop(code)
        else :
            raise InvalidKeyError("Invalid action entered...")

    def __del__(self):
        with open("data_list.txt", 'a') as file :
            file.truncate(0)
            file.seek(0)
            for keys, value in self.__Not_Completed_Tasks.items():
                file.write(keys + " : " + str(value) + "\n")                

task_list = Tasks_List(True)
while True :
    print("What do you want to do? (Add Task (1), Remove Task (2), Update Task (3), Display Tasks (4), Mark Task Done (5), Undo (6)) -> ")
    task = int(input("Enter the task number : "))
    if task == 1:
        task_name = input("Enter the task you want to add : ")
        priority = int(input("Enter its priority (1-4) : "))
        deadline = input("Enter the deadline (Today, etc) : ")
        task_list.add_task(task_name, priority, deadline)
    elif task == 2:
        user_code = input("Enter the code of the task : ")
        task_list.remove_task(user_code)
    elif task == 3:
        user_code_update = input("Enter the code of the task : ")
        task_name_update = input("Enter the new task : ")
        priority_update = int(input("Enter the priority of the task (1-4) : "))
        deadline_update = input("Enter the deadline of the task (Today, etc) : ")
        task_list.update_task(user_code_update, task_name_update, priority_update, deadline_update)
    elif task == 4:
        done_or_not = input("Have you done the task (y/n) : ")
        if done_or_not.upper() == 'Y':
            task_completed = task_list.display_task_list("completed")
            display_task_dictionary_generator(task_completed)
        elif done_or_not.upper() == 'N':
            task_not_completed = task_list.display_task_list("not-completed")
            display_task_dictionary_generator(task_not_completed)
        else :
            raise InvalidKeyError("Unexpected Value Entered...")
    elif task == 5:
        code_mark_done = input("Enter the code of the task : ")
        task_list.mark_done(code_mark_done)
    elif task == 6:
        code_undo = input("Enter the code of the task : ")
        task_list.undo_task(code_undo, 'u')
    else :
        print("Invalid Input...")
    print("Do you want to continue? (y/n) -> ")
    continue_or_not = input()
    if continue_or_not.upper() == 'Y':
        continue
    elif continue_or_not.upper == 'N':
        break
    else :
        break
del task_list
