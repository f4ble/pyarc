# Arkon
Multifunctional RCON tool for Ark Survival. Both interactive and daemon

Runs in command line. Python v3.5

Current features:
- Interactive mode:
  * Some custom commands (check_version or version, exit, shutdown, listplayers, etc)
  * Issue commands directly to the server with: raw command.....
  
- Daemon mode:
  * Hardcoded scheduled tasks. Get players, Get Chat, Run version check
  * [Planned] Cron-like commands. Schedule your restart with a broadcast command prior.
  * [Planned] Mysql storage of users online and chat.
  * [Planned] Chat commands. !lastseen PlayerName will query mysql storage for last time player was online.
  
- Other:
  * Server version check. Arkon will notify you if there is a new version of the game. 
    Current method is a bit crappy, but hoping for better solutions soon.
  * Background UDP query (Steam query protocol) to Ark Server to get version number. 
  
