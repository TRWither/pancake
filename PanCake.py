#!/usr/bin/env  python3

import sys
import json
import os

class PanCake:
    """
    PanCake class.
    :param tasks: the user tasks
    :param important_tasks: the important user tasks
    :param complete: the completed tasks
    :param unfinished: the unfinished tasks
    :param trash: the user trash
    :param version: the PanCake version
    :param save_file: the PanCake save file
    :param secret_tasks: the user secret tasks
    :param secret_tasks_password: the password for the secret tasks
    :param logs_status: the logs status (2 by default)
    """
    def __init__(self, version: str="1.3", save_file=None):
        self.tasks = {}
        self.important_tasks = {}
        self.complete = 0
        self.unfinished = 0
        self.trash = []
        self.version = version
        self.history = []
        self.secret_tasks = {}
        self.secret_tasks_password = ""
        self.logs_status = 2

        if save_file is None:
            script_dir = os.path.dirname(os.path.realpath(__file__))
            self.save_file = os.path.join(script_dir, "saved_tasks.json")
        else:
            self.save_file = save_file

        self.clear_screen()
        self.start()
        self.prompt()

    def __repr__(self):
        return f"TaskManager(tasks={self.tasks}, complete={self.complete}, unfinished={self.unfinished}, trash={self.trash})"

    def display_tasks(self):
        """
        Display an enumeration of all the user tasks.
        """
        if self.important_tasks:
            print("--> IMPORTANT TASKS")
            for i, (task, status) in enumerate(self.important_tasks.items(), start=1):
                print(f"* {i}. {task} - {status}")

        if self.tasks and self.important_tasks:
            print("--------------------------------------")

        if self.tasks:
            for i, (task, status) in enumerate(self.tasks.items(), start=1):
                print(f"{i}. {task} - {status}")

    def display_trash(self):
        """
        Display an enumeration of all the tasks which are in the trash.
        """
        for i, task in enumerate(self.trash, start=1):
            print(f"{i}. {task}")

    def display_secrets(self):
        """
        Display an enumeration of all the secret tasks.
        """
        password = input("Enter password: ")
        if password == self.secret_tasks_password:
            for i, (task, status) in enumerate(self.secret_tasks.items(), start=1):
                print(f"{i}. {task} - {status}")
        else:
            if self.logs_status == 1 or self.logs_status == 2:
                print("Wrong password.")

    def add_task(self, task: str):
        """
        Add a new task to the user tasks.
        """
        task = " ".join(task)
        if task not in self.tasks:
            self.tasks[task] = "Unfinished"
            self.unfinished += 1

            # LOG
            if self.logs_status == 2:
                print(f"'{task}' has been added to the tasks.")
            # ENDLOG

        else:
            if self.logs_status == 1 or self.logs_status == 2:
                print("Task already added.")

    def add_secret(self, task: str):
        """
        Add a new or an existing task to the secret tasks.
        """
        password = input("Enter password: ")
        if password == self.secret_tasks_password:
            task = " ".join(task)
            if task in self.tasks:
                self.secret_tasks[task] = self.tasks[task]
                self.tasks.pop(task)

                # LOG
                if self.logs_status == 2:
                    print(f"'{task}' has been added to the secret tasks")
                # ENDLOG

            elif task in self.important_tasks:
                self.secret_tasks[task] = self.important_tasks[task]
                self.important_tasks.pop(task)
            elif task in self.trash:
                if self.logs_status == 1 or self.logs_status == 2:
                    print("This task is in the trash.")
            else:
                self.secret_tasks[task] = "Unfinished"
        else:
            if self.logs_status == 1 or self.logs_status == 2:
                print("Wrong password.")

    def remove_secret(self, task: str):
        """
        Remove a task from the secret tasks.
        """
        password = input("Enter password: ")
        if password == self.secret_tasks_password:
            task = " ".join(task)
            if task in self.secret_tasks:
                if self.logs_status == 2:
                    print(f"Removing '{task}'...")
                self.tasks[task] = self.secret_tasks[task]
                self.secret_tasks.pop(task)
            else:
                if self.logs_status == 1 or self.logs_status == 2:
                    print("This task is not hidden.")
        else:
            if self.logs_status == 1 or self.logs_status == 2:
                print("Wrong password.")

    def remove_task(self, task: str):
        """
        Move a task to the trash.
        """
        task = " ".join(task)
        if task in self.tasks:
            if self.logs_status == 2:
                print(f"Removing '{task}'...")
            removed_task = self.tasks.pop(task)
            self.trash.append(task)
            if removed_task == "Complete":
                self.complete -= 1
            else:
                self.unfinished -= 1
        elif task in self.important_tasks:
            if self.logs_status == 2:
                print(f"Removing '{task}'...")
            removed_task = self.important_tasks.pop(task)
            self.trash.append(task)
            if removed_task == "Complete":
                self.complete -= 1
            else:
                self.unfinished -= 1
        else:
            if self.logs_status == 1 or self.logs_status == 2:
                print("This task doesn't exist.")

    def remove_all(self):
        """
        Move all the tasks to the trash.
        """
        for task in list(self.tasks):
            if self.logs_status == 2:
                print(f"Removing '{task}'...")
            removed_task = self.tasks.pop(task)
            self.trash.append(task)
            if removed_task == "Complete":
                self.complete -= 1
            else:
                self.unfinished -= 1

    def complete_task(self, task: str):
        """
        Complete a user task.
        """
        task = " ".join(task)
        if task in self.tasks:
            if self.tasks[task] != "Complete":
                self.tasks[task] = "Complete"
                self.complete += 1
                self.unfinished -= 1
            else:
                if self.logs_status == 1 or self.logs_status == 2:
                    print("Task already complete.")
        elif task in self.important_tasks:
            if self.important_tasks[task] != "Complete":
                self.important_tasks[task] = "Complete"
                self.complete += 1
                self.unfinished -= 1
            else:
                if self.logs_status == 1 or self.logs_status == 2:
                    print("Task already complete.")
        elif task in self.secret_tasks:
            password = input("Enter password: ")
            if password == self.secret_tasks_password:
                if self.secret_tasks[task] != "Complete":
                    self.secret_tasks[task] = "Complete"
                    self.complete += 1
                    self.unfinished -= 1
            else:
                if self.logs_status == 1 or self.logs_status == 2:
                    print("Wrong password.")
        else:
            if self.logs_status == 1 or self.logs_status == 2:
                print("This task doesn't exist.")

    def full_complete(self):
        """
        Complete all the user tasks.
        """
        for task in self.tasks:
            if self.logs_status == 2:
                print(f"Completing '{task}'...")
            if self.tasks[task] == "Unfinished":
                self.tasks[task] = "Complete"
                self.complete += 1
                self.unfinished -= 1
        for task in self.important_tasks:
            if self.logs_status == 2:
                print(f"Completing '{task}'...")
            if self.important_tasks[task] == "Unfinished":
                self.important_tasks[task] = "Complete"
                self.complete += 1
                self.unfinished -= 1

    def unfinish_task(self, task: str):
        """
        Mark a user task as unfinished.
        """
        task = " ".join(task)
        if task in self.tasks:
            if self.tasks[task] != "Unfinished":
                self.tasks[task] = "Unfinished"
                self.complete -= 1
                self.unfinished += 1
        elif task in self.important_tasks:
            if self.important_tasks[task] != "Unfinished":
                self.important_tasks[task] = "Unfinished"
                self.complete -= 1
                self.unfinished += 1
        elif task in self.secret_tasks:
            password = input("Enter password: ")
            if password == self.secret_tasks_password:
                if self.secret_tasks[task] != "Unfinished":
                    self.secret_tasks[task] = "Unfinished"
                    self.complete -= 1
                    self.unfinished += 1
            else:
                if self.logs_status == 1 or self.logs_status == 2:
                    print("Wrong password.")
        else:
            if self.logs_status == 1 or self.logs_status == 2:
                print("This task doesn't exist.")

    def full_unfinish(self):
        """
        Mark all the user tasks as unfinished.
        """
        for task in self.tasks:
            if self.logs_status == 2:
                print(f"Marking '{task}' as unfinished...")
            if self.tasks[task] == "Complete":
                self.tasks[task] = "Unfinished"
                self.complete -= 1
                self.unfinished += 1
        for task in self.important_tasks:
            if self.logs_status == 2:
                print(f"Marking '{task}' as unfinished...")
            if self.important_tasks[task] == "Complete":
                self.important_tasks[task] = "Unfinished"
                self.complete -= 1
                self.unfinished += 1

    def recover_task(self, task: str):
        """
        Recover a removed task.
        """
        task = " ".join(task)
        if task in self.trash:
            self.trash.remove(task)
            self.tasks[task] = "Unfinished"
            self.unfinished += 1
        elif task in self.tasks:
            if self.logs_status == 1 or self.logs_status == 2:
                print("This task is not in the trash.")
        else:
            if self.logs_status == 1 or self.logs_status == 2:
                print("This task doesn't exist.")

    def recover_all(self):
        """
        Recover all the removed tasks.
        """
        removed_tasks = self.trash
        for task in removed_tasks:
            print(f"Recovering '{task}'...")
            self.tasks[task] = "Unfinished"
        self.trash = []

    def destroy_task(self, task: str):
        """
        Remove a task from the trash.
        The task cannot be recovered.
        """
        task = " ".join(task)
        if task in self.trash:
            self.trash.remove(task)
        elif task in self.tasks:
            if self.logs_status == 1 or self.logs_status == 2:
                print("This task is not in the trash.")
        else:
            if self.logs_status == 1 or self.logs_status == 2:
                print("This task doesn't exist.")

    def empty_trash(self):
        """
        Remove all the tasks from the trash.
        The tasks cannot be recovered.
        """
        confirmation = input("The tasks cannot be recovered. Are you sure you want to do that (Y/n)? ")
        if confirmation == "Y":
            if self.logs_status == 2:
                print(f"Clearing trash...")
            self.trash.clear()

    def advancement(self):
        """
        Display the amount of completed and unfinished tasks.
        """
        print(f"You have completed {self.complete} tasks.")
        print(f"You have {self.unfinished} more tasks to complete.")

    def save_tasks(self):
        """
        Save the current session.
        """
        if self.logs_status == 1 or self.logs_status == 2:
            print("Saving...")
        data = {
            "tasks": self.tasks,
            "trash": self.trash,
            "complete": self.complete,
            "unfinished": self.unfinished,
            'important':self.important_tasks,
            'history': self.history,
            "secrets": self.secret_tasks,
            "secrets-password": self.secret_tasks_password,
            "logs-status": self.logs_status
        }
        with open(self.save_file, 'w') as save_file:
            json.dump(data, save_file)
        if self.logs_status == 1 or self.logs_status == 2:
            print("Saved.")

    def load_tasks(self):
        """
        Load the save file.
        """
        if self.logs_status == 1 or self.logs_status == 2:
            print("Loading...")
        try:
            with open(self.save_file, 'r') as save_file:
                data = json.load(save_file)
                self.tasks = data.get("tasks", {})
                self.trash = data.get("trash", [])
                self.complete = data.get("complete", 0)
                self.unfinished = data.get("unfinished", 0)
                self.important_tasks = data.get("important", [])
                self.history = data.get("history", [])
                self.secret_tasks = data.get("secrets", {})
                self.secret_tasks_password = data.get("secrets-password", "")
                self.logs_status = data.get("logs-status", 0)
            if self.logs_status == 1 or self.logs_status == 2:
                print("Tasks loaded successfully.")
        except FileNotFoundError:
            if self.logs_status == 1 or self.logs_status == 2:
                print("No saved tasks found.")
        except json.JSONDecodeError:
            if self.logs_status == 1 or self.logs_status == 2:
                print("Error loading tasks. File may be corrupted.")

    def clear_screen(self):
        """
        Clear the screen.
        """
        os.system('clear' if os.name == 'posix' else 'cls')

    def pin_task(self, task: str):
        """
        Add a :param task: to the important tasks and remove
        it from the user tasks.
        """
        task = " ".join(task)
        if task in self.tasks:
            self.tasks.pop(task)
            self.important_tasks[task] = "Unfinished"
        elif task in self.important_tasks:
            if self.logs_status == 1 or self.logs_status == 2:
                print("You already pinned this task.")
        elif task in self.trash:
            if self.logs_status == 1 or self.logs_status == 2:
                print("This task is in the trash.")
        else:
            if self.logs_status == 1 or self.logs_status == 2:
                print("This task doesn't exist.")

    def unpin_task(self, task: str):
        """
        Remove a task from the important tasks and add
        it to the user tasks.
        """
        task = " ".join(task)
        if task in self.important_tasks:
            self.important_tasks.pop(task)
            self.tasks[task] = "Unfinished"
        elif task in self.tasks:
            if self.logs_status == 1 or self.logs_status == 2:
                print("This task is not pinned.")
        elif task in self.trash:
            if self.logs_status == 1 or self.logs_status == 2:
                print("This task is in the trash.")
        else:
            if self.logs_status == 1 or self.logs_status == 2:
                print("This task doesn't exist.")

    def display_history(self):
        """
        Display the current commands history of the user.
        """
        for i, command in enumerate(self.history, start=1):
            print(f"{i}. {command}")

    def history_clear(self):
        """
        Clear the entire commands history of the user.
        """
        if self.logs_status == 2:
            print("Clearing the commands history...")
        self.history.clear()

    def set_secret_tasks_password(self):
        """
        Change the password of the secret tasks.
        """
        precedent_password = input("Enter precedent password: ")
        if precedent_password == self.secret_tasks_password:
            new_password = input("Enter new password: ")
            new_password_repeat = input("Repeat new password: ")
            if new_password_repeat == new_password:
                self.secret_tasks_password = new_password_repeat
                confirm_save = input("Password has been modified. Do you want to save? (Y/n) ")
                if confirm_save == "Y":
                    self.save_tasks()
            else:
                if self.logs_status == 1 or self.logs_status == 2:
                    print("The two passwords are different.")
        else:
            if self.logs_status == 1 or self.logs_status == 2:
                print("Wrong password.")

    def help(self):
        """
        Display a help message.
        """
        print("PanCake Help -- see more at https://github.com/TRWIther/pancake")
        print("============================================================================")
        print("help                     ->        display this message")
        print("tasks                    ->        display all your tasks")
        print("trash                    ->        display the content of the trash")
        print("new <task>               ->        add a new task")
        print("remove <task>            ->        add a task to the trash")
        print("complete <task>          ->        complete a task")
        print("unfinish <task>          ->        unfinish a task")
        print("recover <task>           ->        recover a removed task")
        print("destroy <task>           ->        remove a task from the trash")
        print("advancement              ->        see the tasks advancement")
        print("exit                     ->        exit PanCake")
        print("license                  ->        display the MIT License terms for PanCake")
        print("save                     ->        save your current tasks")
        print("load                     ->        load a save file")
        print("clear                    ->        clear the screen")
        print("pin <task>               ->        pin a task")
        print("unpin <task>             ->        unpin a task")
        print("updated                  ->        show what's new in this version")
        print("empty                    ->        remove all the tasks from the trash")
        print("recoverall               ->        recover all the removed tasks")
        print("full-complete            ->        complete all the tasks")
        print("full-unfinish            ->        mark all the tasks as unfinished")
        print("history                  ->        show your commands history")
        print("history-clear            ->        clear your commands history")
        print("removeall                ->        remove all the tasks")
        print("secrets                  ->        display the secret tasks")
        print("hide <task>              ->        add a task to the secret tasks")
        print("show <task>              ->        remove a task from the secret tasks")
        print("secrets-setpw            ->        change the password of the secret tasks")
        print("log <text>               ->        print some text")
        print("setlogs <status>         ->        change the logs status (0, 1, 2)")

    def license(self):
        """
        Display the MIT License terms for PanCake.
        """
        print("""
Copyright (c) 2024 Wither__

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        """)

    def updated(self):
        print("""
PanCake 1.3 is out!
---------------------
What's new?
- You can now have secret tasks!
- Password for secret tasks
- Added a logs management

There is no pinning system for hidden (secret) tasks, and they must be put
back into normal tasks before they can be deleted. Every operation related
to secret tasks will require a password (empty by default, but you can
change it).
As far as log management is concerned, there are 3 logging levels: 0, which
completely cancels logs, 1, which displays only important messages, and 2,
which displays absolutely everything.
        """)

    def exit(self):
        """
        Exit PanCake.
        """
        confirm_save = input("All unsaved changes will be lost. Do you want to save before quitting? (Y/n) ")
        if confirm_save == "Y":
            self.save_tasks()
        self.clear_screen()
        sys.exit(0)

    def start(self):
        """
        Display the PanCake start messages.
        """
        print(f"Welcome in PanCake version {self.version}!")
        print("Type 'help' to see a list of the available commands.")

    def prompt(self):
        """
        Start the main PanCake prompt.
        """
        while True:
            command = input("> ")
            command_parts = command.split()
            if not command_parts:
                continue

            name = command_parts[0]
            argument = command_parts[1:] if len(command_parts) > 1 else None

            if name == "help":
                self.help()
            elif name == "license":
                self.license()
            elif name == "exit":
                self.exit()
            elif name == "tasks":
                self.display_tasks()
            elif name == "trash":
                self.display_trash()
            elif name == "new" and argument:
                self.add_task(argument)
            elif name == "remove" and argument:
                self.remove_task(argument)
            elif name == "complete" and argument:
                self.complete_task(argument)
            elif name == "unfinish" and argument:
                self.unfinish_task(argument)
            elif name == "recover" and argument:
                self.recover_task(argument)
            elif name == "destroy" and argument:
                self.destroy_task(argument)
            elif name == "advancement":
                self.advancement()
            elif name == "save":
                self.save_tasks()
            elif name == "load":
                self.load_tasks()
            elif name == "clear":
                self.clear_screen()
            elif name == "pin" and argument:
                self.pin_task(argument)
            elif name == "unpin" and argument:
                self.unpin_task(argument)
            elif name == "updated":
                self.updated()
            elif name == "empty":
                self.empty_trash()
            elif name == "recoverall":
                self.recover_all()
            elif name == "full-complete":
                self.full_complete()
            elif name == "full-unfinish":
                self.full_unfinish()
            elif name == "history":
                self.display_history()
            elif name == "history-clear":
                self.history_clear()
            elif name == "removeall":
                self.remove_all()
            elif name == "secrets":
                self.display_secrets()
            elif name == "hide" and argument:
                self.add_secret(argument)
            elif name == "show" and argument:
                self.remove_secret(argument)
            elif name == "secrets-setpw":
                self.set_secret_tasks_password()
            elif name == "setlogs" and argument:
                if argument[0] in {"0", "1", "2"}:
                    self.logs_status = int(argument[0])
                    if self.logs_status == 1 or self.logs_status == 2:
                        print(f"Logs status updated to {self.logs_status}.")
                else:
                    print("Invalid logs status. Please enter 0, 1, or 2.")
            elif name == "log" and argument:
                print(" ".join(argument))
            else:
                if self.logs_status == 1 or self.logs_status == 2:
                    print("Invalid command. Type 'help' to see the commands list.")

            self.history.append(command)

# Run PanCake
pancake = PanCake()
