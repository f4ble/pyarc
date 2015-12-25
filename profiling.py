import cProfile
import pstats
from io import StringIO

import ark

cProfile.run('ark.init()', sort='cumulative')


def extensive():
    pr = cProfile.Profile()
    pr.enable()
    ark.init()
    pr.disable()
    s = StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

    # extensive()
