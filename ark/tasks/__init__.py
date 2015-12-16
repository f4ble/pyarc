from .task_check_for_update import Task_CheckForUpdates
from .task_list_players import Task_ListPlayers
from .task_get_chat import Task_GetChat
from .task_daily_restart import Task_DailyRestart


Task_CheckForUpdates.run_interval(1800)
Task_ListPlayers.run_interval(5,immediately=True)
Task_GetChat.run_interval(2,immediately=True)
Task_DailyRestart.run_daily('07:50:00') #Broadcasts warnings start 10 minutes prior to update and restart.
