from ark.cli import *


class Events(object):
    """
    
    Remember to add entry with corresponding integer key to _event_callbacks if you add another event!
    
    """
    E_CONNECT = 1
    E_DISCONNECT = 2
    E_CHAT = 3
    E_NEW_ARK_VERSION = 4
    E_NEW_PLAYER = 5
    E_CHAT_FROM_SERVER = 6
    E_RCON_CONNECTED = 7

    _event_callbacks = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: []
    }

    @staticmethod
    def _valid_event_type(event_type):
        """Validate event type argument
         
        Constants E_* use integer
        """

        assert type(event_type) is int, 'Recommend using constants Events.E_*'
        if event_type not in Events._event_callbacks.keys():
            raise TypeError('Unknown event type: {}. Recommend using constants Events.E_*'.format(event_type))

    @staticmethod
    def registerEvent(event_type, callback):
        """Register callback for event
        
        Args:
            event_type: of constant E_*
        
        Returns:
            None
        """

        Events._valid_event_type(event_type)
        if callable(callback) is False:
            raise TypeError('argument callback not callable()')

        Events._event_callbacks[event_type].append(callback)
        return None

    @classmethod
    def triggerEvent(cls, event_type, *args):
        """Run by Arkon core code.
        
        Triggers event and runs all callbacks registered with registerEvent()
        
        Args:
            event_type: of constant E_*
        
        Returns:
            None
        """

        cls._valid_event_type(event_type)

        debug_out(
            'Triggering event type: {} with {} callbacks'.format(event_type, len(cls._event_callbacks[event_type])),
            level=2)

        for callback in cls._event_callbacks[event_type]:
            callback(*args)

        return None
