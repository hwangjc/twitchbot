# User Guide

This is a user facing guide on how to interact with this twitch bot.

- [Command Management](#command-management)
- [Queue Commands](#queue-commands)
- [Generic Commands](#generic-commands)


## Command Management
Commands to add, modify, or remove user-defined commands. Built-in commands cannot be removed (as of now).
### Adding a new command
> :warning: mod-only command

Usage:
```
!addcommand !COMMAND_NAME CONTENT
```
Example:
- `!addcommand !test This is a test`

### Removing a command
> :warning: mod-only command

Usage:
```
!rmcommand !COMMAND_NAME
```
Example:
- `!rmcommand !test`

### Editing a command
> :warning: mod-only command

Usage:
```
!editcommand !COMMAND_NAME NEW_CONTENT
```
Example:
- `!editcommand !test this is a new test`


## Queue Commands
Here we have a set of commands to interact with a generic queue. The generic queue can only contain unique users (i.e. users cannot be in the queue 
multiple times without first leaving the queue).

Users may also insert a message when joining the queue, which will be displayed when it is the users turn to be popped out of the queue.
### Opening the queue
> :warning: mod-only command

Usage:
```
!open
```
### Closing the queue
> :warning: mod-only command

Closing the queue does **NOT** clear the queue. If you close the queue and then re-open the queue, all of the users in the queue will remain there until
cleared or all users are popped. See [how to clear the queue](#closing-the-queue) if you want to also clear a queue.

Usage:
```
!close
```
### Clearing the queue
> :warning: mod-only command

Remove all users from the queue.

Usage:
```
!clear
```
### Joining the queue
Join the queue with an optional message.

Usage:
```
!join [MESSAGE]
```
Examples:
- `!join`: add yourself to the queue with no message
- `!join this is my custom message`: add yourself to the queue with a message

## Generic Commands
