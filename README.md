# Arkon
All-purpose RCON tool for Ark: Survival.

Main purpose is as a service. Monitoring the server and adding features.
Cron-like commands give you great deal of control.

In addition this tool is interactive so you don't need a second instance
to issue commands to the server.

Runs in command line / terminal. Python v3.5

Requires:
- python modules: pymysql3, SQLAlchemy
- SQL server / sqlite (untested)
- Ark Survival RCON access (duh)

Current features:
- Interactive mode:
    * Custom commands (default_input_commands.py)
        * check_version - Checks for new build id
        * version - Returns Server Game Version
        * exit - Quit this program
        * shutdown - Shutdown server
        * online - List players online
        * restart - Restart server. Does so gently with saveworld and doExit
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
        * [Waiting for game support] killme - Suicide
        * [Planned] mail PlayerName Message - Ingame mailing system
    * [Planned] Cron-like commands. Schedule your restart with a broadcast command prior.
    * Check with OS if server is running and alter behavior accordingly.
    * Server restarts / shutdown puts the service on hold. Resumes when server is detected.
  
- Other:
  * Server version check. Arkon will notify you if there is a new version of the game. 
    Current method is a bit crappy, but hoping for better solutions soon.
  * Background UDP query (Steam query protocol) to Ark Server to get version number. 
  * Event Callback registration lets you easily add more functionality when something happens.
        * Many different types: players connected/disconnected, chat, server update and more.


Installation:
[...]