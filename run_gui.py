from configs.config_base import ConfigBase
ConfigBase.load_config()

from translation import Translation
from factory import Factory

trans = Translation()
Factory.set('Translation',trans)

import ark.gui

ark.gui.init()