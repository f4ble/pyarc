# PyArc
Cross-platform terminal Server Control for Ark: Survival written in Python

Written by Torgrim "Fable" Ruud - torgrim.ruud@gmail.com

Huge thanks to Gildas Lepennetier and Thomas Girardeau for assisting in bugfixing as well as developing chat filter,
voting, quotes and translation to French and German! Awesome guys :D

__This code is released under the Apache License 2.0 license.__

Main purpose is as a service. Monitoring the server and adding features.
Cron-like commands give you great deal of control.

In addition this tool is interactive so you don't need a second instance
to issue commands to the server.

Runs in command line / terminal. Python v3.5

Requires:
- python modules: pymysql3, SQLAlchemy
- SQL server / sqlite (untested)
- Ark Survival RCON access (duh)

Installation:
- Set up a mysql server. Other SQL servers not tested, but may work.
- Copy example_config.py to config.py and edit. More settings from config_base.py can be overriden if needed.
- Run install.py - This will check your config and create database tables if they don't exist. 
- configs/tasks_default.py contain the scheduled tasks. Disable or edit your scheduled restarts here.

Current features:
- Interactive mode:
    * Custom commands (default_input_commands.py)
        * check_version - Checks for new build id
        * version - Returns Server Game Version
        * exit - Quit this program
        * shutdown - Shutdown server
        * online - List players online
        * restart [now/10/30/60]- Restart server (with a countdown if you want). Does so gently with saveworld and doExit and an update after shutdown.
        * etc
    * Add your own commands with InputHandler.registerCommand('command',callback)
        * This enables you to add more than one callback for a single command.
    * Issue commands directly to the server with:
        * raw [command.....]
  
  
- Service mode:
    * Hardcoded scheduled tasks. Get players, Get Chat, Run version check
    * Mysql storage of users and chat.
    * Chat commands. Prefix with !
        * lastseen PlayerName - Last time player was online.
        * online - List players online
        * next_restart - If a delayed restart is active gives the player the proper countdown.
        * [Waiting for game support] killme - Suicide
        * [Planned] mail PlayerName Message - Ingame mailing system
    * Scheduled tasks can be customized through the files in the "tasks" folder.
    * Players logging on are immediately notified of any delayed restarts.
    * Check with OS if server is running and alter behavior accordingly.
    * Server restarts / shutdown puts the service on hold. Resumes when server is detected.
    * Savegame integrity check. Ark saves are corrupted now and then, but easily fixed by restoring one of the backups.
      The integrity check compares filesize between current savegame and older ones and notifies loudly if failed.
  
- Other:
  * Server version check. PyArc will notify you if there is a new version of the game. 
  * Background UDP query (Steam query protocol) to Ark Server to get version number. 
  * Event Callback registration lets you easily add more functionality when something happens.
        * Many different types: players connected/disconnected, chat, server update and more.


Installation:
[...]



__Explanation for coders:__

Keep in mind: Things are done a bit differently as I've used this as a learning project coming from php to python.


__Scheduled tasks__

To create a task run at an interval, time of day or just once at a specific time see the "Tasks" folder.
Create your own class, which inherits scheduled.py and create a run() function with cls as only param.

Tasks are defined in the tasks package and initialized in configs/tasks_default.py.
Which file to load (tasks_default.py) can be customized per config using the Config.tasks_default filename variable

In configs/tasks_default.py you define the interval or time you wish this task to run by using one of three functions:
The only code inside tasks_default.py that is executed is the init() function - so put any changes you want there.

* run_daily
* run_interval
* run_once

Example:

    from ark.tasks.task_my_task_class import MyTaskClass
    MyTaskClass.run_interval(30) #30 seconds

Arguments should be well documented if you have code completion and tooltips.
These functions are defined in class Scheduler and inherited to your task class.


__Events__

You can add more events handlers to predefined events.
This easily lets you improve functionality when a specific event occurs.
You can also add more than one callback to an event - giving you nice and tidy execution without
having to edit (and understand) my code.

* E_CONNECT / E_DISCONNECT (player_list):
* E_CHAT (steam_name, player_name, text, line):
* E_NEW_ARK_VERSION ():
* E_NEW_PLAYER (steam_id, name):
* E_CHAT_FROM_SERVER (text, line):


These event constants and needed methods are defined in event_handler.py
Events are defined in the events package and initialized in configs/events_default.py.
Which file to load (events_default.py) can be customized per config using the Config.events_default filename variable
The only code inside events_default.py that is executed is the init() function - so put any changes you want there.


__Input handling from Terminal (not chat commands)__

Add more commands to your terminal window by using the class InputHandler

In default_input_commands you add the callbacks and in init() you register these callbacks with a specific command:

    InputHandler.register_command('stats',callback)

If the line of terminal input starts with "stats" then callback(text) is triggered with the entire line of text.



__Chat Commands__

The file chat_commands is the least impressive of these designs and contains triggers from ingame chat to respond to.

Chat commands are always prefixed with exclamation mark !

ChatCommands.parse()
    Add your commands in this function

Add your logic as a seperate function in ChatCommands called within parse()
