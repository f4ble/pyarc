from ark.config import Config
Config.disable_output = True

# Player list update: Player connect/disconnect
from ark_unit_tests.scheduled_tasks import list_players

list_players()
