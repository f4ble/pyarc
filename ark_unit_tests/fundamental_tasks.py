from ark.cli import out
from ark.config import Config
print("Unit tests: ",Config.disable_output)
def list_players():
    out('Testing "list players"')
    from ark.scheduled_tasks import TaskResponses
    from ark.rcon_packet import Packet
    
    test_packet = Packet()
    
    out('\nTest: Connect. Valid response: Alpha connected')
    test_packet.decoded['body'] = "1. Test Alpha, 10\n"
    if TaskResponses.list_players(test_packet) is False:
        raise Exception('Test failure')
    
    out('\nTest: Connect. Valid response: Alpha disconnected')
    test_packet.decoded['body'] = "No Players Connected!!\n"
    if TaskResponses.list_players(test_packet) is False:
        raise Exception('Test failure')
    
    out('\nTest: Connect. Valid response: Alpha connected')
    test_packet.decoded['body'] = "1. Test Alpha, 10\n"
    if TaskResponses.list_players(test_packet) is False:
        raise Exception('Test failure')
    
    out('\nTest: Disconnect. Valid response: Test Beta connected, Alpha disconnect')
    test_packet.decoded['body'] = "2. Test Beta, 11\n"
    if TaskResponses.list_players(test_packet) is False:
        raise Exception('Test failure')
    
    out('\nTest: Multi Connect. Valid response: Test Alpha connected')
    test_packet.decoded['body'] = "1. Test Alpha, 10\n2. Test Beta, 11\n"
    if TaskResponses.list_players(test_packet) is False:
        raise Exception('Test failure')
    
    out('\nTest: No players. Valid response: 2 disconnects')
    test_packet.decoded['body'] = "No Players Connected!!\n"
    if TaskResponses.list_players(test_packet) is False:
        raise Exception('Test failure')
    
    out('\nTest: No players. Valid response: Silent')
    test_packet.decoded['body'] = "No Players Connected!!\n"
    if TaskResponses.list_players(test_packet) is False:
        raise Exception('Test failure')
    
    out('\nTest: Malformed packet. Valid response: Silent')
    test_packet.decoded['body'] = "ASDKJASDKNMLQWKWERN\nASDASAA''(==))!%&!%/())L[]}["
    if TaskResponses.list_players(test_packet) is False:
        raise Exception('Test failure')
    
    
    print('list_players() test ended.')