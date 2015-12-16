from .task_check_for_update import Task_CheckForUpdates
from .task_list_players import Task_ListPlayers
from .task_get_chat import Task_GetChat


Task_CheckForUpdates.run_interval(1800)
Task_ListPlayers.run_interval(5,immediately=True)
Task_GetChat.run_interval(2,immediately=True)
