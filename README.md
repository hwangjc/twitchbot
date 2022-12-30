# User Guide

This is a user facing guide on how to interact with this twitch bot.

- [Command Management](#command-management)
  - [Adding a new command](#adding-a-new-command)
  - [Removing a command](#removing-a-command)
  - [Editing a command](#editing-a-command)
- [Queue Commands](#queue-commands)
  - [Opening the queue](#opening-the-queue)
  - [Closing the queue](#closing-the-queue)
  - [Clearing the queue](#clearing-the-queue)
  - [Get next user in the queue](#get-next-user-in-the-queue)
  - [Joining the queue](#joining-the-queue)
  - [Leaving the queue](#leaving-the-queue)
  - [View users in the queue](#view-users-in-the-queue)
- [Generic Commands](#generic-commands)
  - [Shoutout](#shoutout)


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
### Get next user in the queue
> :warning: mod-only command

Display the next user in the queue and subsequently remove them from the queue. If the user joined with a custom message, the custom message will also 
be displayed.

Usage:
```
!next
```
### Joining the queue
Join the queue with an optional message. If you join with an optional message, the message will be displayed when it is your turn in the queue.

Usage:
```
!join [MESSAGE]
```
Examples:
- `!join`: add yourself to the queue with no message
- `!join this is my custom message`: add yourself to the queue with a message

### Leaving the queue
Usage:
```
!leave
```
### View users in the queue
List all users currently in the queue, as well as their position in the queue.

Usage:
```
!queue
```


## Generic Commands
Some generic commands that usually exist on most Twitch bots.

### Shoutout
> :warning: mod-only command

Shoutout a valid user by sending an announcment to the chat. The announcement message will contain both the target user's Twitch channel link 
as well as which game they were last seen playing on Twitch (if applicable).

Usage:
```
!shoutout TARGET_USER
!so TARGET_USER
```
Examples:
- `!shoutout @divinesenatorkelly`
- `!so @divinesenatorkelly`
- `!so divinesenatorkelly`
