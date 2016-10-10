
import datetime as dt

def wrange(ts, i):
    d = dt.datetime.strptime(ts,'%Y-%m-%d')
    return map(lambda j : dt.datetime.strftime(d - dt.timedelta(j),'%Y-%m-%d'), range(i))
    
def tsdiff(a, b):
    x = dt.datetime.strptime(a,'%Y-%m-%d')
    y = dt.datetime.strptime(b,'%Y-%m-%d')
    return (x-y).days