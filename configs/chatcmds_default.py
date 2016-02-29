from ark.chat_commands_handler import ChatCommands
from ark.chat_commands.other import CmdsOther
from ark.chat_commands.admin import CmdsAdmin

def init():

    #Admin cmds
    ChatCommands.register_chat_command_regex('!admin_filter_add.*',CmdsAdmin.admin_filter_add)
    ChatCommands.register_chat_command_regex('!admin_filter_remove.*',CmdsAdmin.admin_filter_remove)
    ChatCommands.register_chat_command_regex('!admin_restart.*',CmdsAdmin.admin_restart)
    ChatCommands.register_chat_command('!admin_check_version',CmdsAdmin.admin_check_version)
    ChatCommands.register_chat_command('!admin_update_now',CmdsAdmin.admin_update_now)
    ChatCommands.register_chat_command_regex('!admin_survey_add.*',CmdsAdmin.admin_survey_add)
    ChatCommands.register_chat_command_regex('!admin_stop_survey.*',CmdsAdmin.admin_stop_survey)
    ChatCommands.register_chat_command_regex('!admin_start_survey.*',CmdsAdmin.admin_start_survey)

    #Player cmds
    ChatCommands.register_chat_command_regex('!lastseen.*',CmdsOther.last_seen)
    ChatCommands.register_chat_command_regex('!quote.*',CmdsOther.quote)
    ChatCommands.register_chat_command('!online',CmdsOther.list_online)
    ChatCommands.register_chat_command('!next_restart',CmdsOther.next_restart)
    ChatCommands.register_chat_command_regex('!survey.*',CmdsOther.survey)
    ChatCommands.register_chat_command_regex('!vote.*',CmdsOther.vote)
    ChatCommands.register_chat_command('!help',CmdsOther.help)
    pass
