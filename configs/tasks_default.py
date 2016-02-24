from ark.tasks.task_check_for_update import Task_CheckForUpdates
from ark.tasks.task_list_players import Task_ListPlayers
from ark.tasks.task_get_chat import Task_GetChat
from ark.tasks.task_daily_restart import Task_DailyRestart
from ark.tasks.task_daily_restart import Task_DailyRestartRepopulate
from ark.tasks.task_sql_keep_alive import Task_SQL_keep_alive


def init():
    #Part of Core Features:

    Task_ListPlayers.run_interval(8,immediately=True)
    Task_GetChat.run_interval(5,immediately=True)
    Task_SQL_keep_alive.run_interval(60)

    #Extras:

    Task_CheckForUpdates.run_interval(1800)
    Task_DailyRestart.run_daily('15:00:00')
    Task_DailyRestartRepopulate.run_daily('06:00:00')

