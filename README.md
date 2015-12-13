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
  * Custom commands
        * check_version
        * version
        * exit
        * shutdown
        * listplayers,
        * etc)
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
  
- Other:
  * Server version check. Arkon will notify you if there is a new version of the game. 
    Current method is a bit crappy, but hoping for better solutions soon.
  * Background UDP query (Steam query protocol) to Ark Server to get version number. 
  * Event Callback registration lets you easily add more functionality when something happens.
        * Many different types: players connected/disconnected, chat, server update and more.
