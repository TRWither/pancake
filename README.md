# PanCake
*A text-based easy to use open-source task manager.*

## How does it work?
PanCake is very easy to use. Here's the full list of commands, which you can also find directly by using it.

`help`: display a help message

`license`: display the MIT License terms for PanCake

`exit`: exit PanCake

`clear`: clear the screen

`new <task name>`: create a new task

`remove <task name>`: move a task in the trash

`destroy <task name>`: remove a task from the trash (removed definetely)

`tasks`: display all the tasks

`trash`: display the content of the trash

`complete <task name>`: complete a task

`unfinish <task name>`: mark a task as unfinished

`save`: save your tasks, the trash and your advancement

`load`: load the save file (saved_tasks.json)

`advancements`: display the amount of completed and unfinished tasks

`pin <task name>`: pin a task

`unpin <task name>`: unpin a task

`updated`: see what is new in the last update

`empty`: clear the trash

`removeall`: move all the tasks to the trash

`full-complete`: complete all the tasks

`full-unfinish`: mark all the tasks as unfinished

`recoverall`: recover all the removed tasks

`history`: display the commands history

`history-clear`: clear the commands history

### New 1.3 commands

`secrets`: display a list of the secret tasks

`hide <task name>`: add a task to the secret tasks

`show <task name>`: remove a task from the secret tasks

`log <text>`: print some text

`secrets-setpw`: change the secret tasks password

`setlogs <status>`: set the logs status (0=desactivate, 1=important only, 2=everything)

WARNING: you must be root to save and load

## Notes
The password for secret (or hidden) tasks is empty by default, which means you don't have to enter anything if you're asked. However, this is not very secure, so it's advisable to set it up quickly.
The password and log status are included in the backup with the `save` command.

## Installation
1. Clone this repository
```bash
git clone https://github.com/TRWither/pancake
```
2. Run `install.sh` as root.
3. Run PanCake with `pancake1.2`!

NOTE: if you are on Windows, you cannot use install.sh

## Contributing
You are free to contribute! But please follow these steps:
1. Fork this repository
2. Add your changes
3. Commit your changes
4. Your changes will be added if I find them good!
