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
    """
    def __init__(self, version: str="1.1", save_file=None):
        self.tasks = {}
        self.important_tasks = {}
        self.complete = 0
        self.unfinished = 0
        self.trash = []
        self.version = version

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

    def add_task(self, task: str):
        """
        Add a new task to the user tasks.
        """
        task = " ".join(task)
        if task not in self.tasks:
            self.tasks[task] = "Unfinished"
            self.unfinished += 1
        else:
            print("Task already added.")

    def remove_task(self, task: str):
        """
        Move a task to the trash.
        """
        task = " ".join(task)
        if task in self.tasks:
            removed_task = self.tasks.pop(task)
            self.trash.append(task)
            if removed_task == "Complete":
                self.complete -= 1
            else:
                self.unfinished -= 1
        elif task in self.important_tasks:
            removed_task = self.important_tasks.pop(task)
            self.trash.append(task)
            if removed_task == "Complete":
                self.complete -= 1
            else:
                self.unfinished -= 1
        else:
            print("This task doesn't exist.")

    def complete_task(self, task: str):
        """
        Complete a task.
        """
        task = " ".join(task)
        if task in self.tasks:
            if self.tasks[task] != "Complete":
                self.tasks[task] = "Complete"
                self.complete += 1
                self.unfinished -= 1
            else:
                print("Task already complete.")
        elif task in self.important_tasks:
            if self.important_tasks[task] != "Complete":
                self.important_tasks[task] = "Complete"
                self.complete += 1
                self.unfinished -= 1
            else:
                print("Task already complete.")
        else:
            print("This task doesn't exist.")

    def unfinish_task(self, task: str):
        """
        Unfinish a task.
        """
        task = " ".join(task)
        if task in self.tasks:
            if self.tasks[task] != "Unfinished":
                self.tasks[task] = "Unfinished"
                self.complete -= 1
                self.unfinished += 1
            else:
                print("This task is already unfinished.")
        elif task in self.important_tasks:
            if self.important_tasks[task] != "Unfinished":
                self.important_tasks[task] = "Unfinished"
                self.complete -= 1
                self.unfinished += 1
            else:
                print("This task is already unfinished.")
        else:
            print("This task doesn't exist.")

    def recover_task(self, task: str):
        """
        Recover a task from the trash.
        """
        task = " ".join(task)
        if task in self.trash:
            self.trash.remove(task)
            self.tasks[task] = "Unfinished"
            self.unfinished += 1
        elif task in self.tasks:
            print("This task is not in the trash.")
        else:
            print("This task doesn't exist.")

    def destroy_task(self, task: str):
        """
        Remove a task from the trash.
        The task cannot be recovered.
        """
        task = " ".join(task)
        if task in self.trash:
            self.trash.remove(task)
        elif task in self.tasks:
            print("This task is not in the trash.")
        else:
            print("This task doesn't exist.")

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
        print("Saving...")
        data = {
            "tasks": self.tasks,
            "trash": self.trash,
            "complete": self.complete,
            "unfinished": self.unfinished,
            'important':self.important_tasks
        }
        with open(self.save_file, 'w') as save_file:
            json.dump(data, save_file)
        print("Saved.")

    def load_tasks(self):
        """
        Load the save file.
        """
        print("Loading...")
        try:
            with open(self.save_file, 'r') as save_file:
                data = json.load(save_file)
                self.tasks = data.get("tasks", {})
                self.trash = data.get("trash", [])
                self.complete = data.get("complete", 0)
                self.unfinished = data.get("unfinished", 0)
                self.important_tasks = data.get("important", [])
            print("Tasks loaded successfully.")
        except FileNotFoundError:
            print("No saved tasks found.")
        except json.JSONDecodeError:
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
            print("You already pinned this task.")
        elif task in self.trash:
            print("This task is in the trash.")
        else:
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
            print("This task is not pinned.")
        elif task in self.trash:
            print("This task is in the trash.")
        else:
            print("This task doesn't exist.")

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
Pancake 1.1 is out!
----------------------
What's new?
- We can pin and unpin tasks
- Better display of the tasks command message
- Better installation in install.sh
        """)

    def exit(self):
        """
        Exit PanCake.
        """
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
            else:
                print("Invalid command. Type 'help' to see the commands list.")

# Run PanCake
pancake = PanCake()
