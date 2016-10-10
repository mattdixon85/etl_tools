
import sys
import json as js
import datetime as dt
from itertools import groupby
from collections import defaultdict
from centricity_fns import wrange, tsdiff

class Centricity:
    def __init__(self, config):
        self.config = config
        self.metrics = dict(
                srcs=defaultdict(int)
                ,tsrcs=dict()
                ,wsrcs=dict()
                ,immu=dict()
                )
        self.tmp = dict(
                tsrcs = dict()
                ,wsrcs = defaultdict(list)
                )
        
    def process_lines(self, lines):
        for t, sublines in groupby(lines, lambda x : x.strip().split('\\t')[1]):
            sub = list()

            # update tsrc values                
            for k, v in self.tmp['tsrcs'].items():
                self.metrics['tsrcs'][k] = tsdiff(t, v)
            
            # metric gathering
            for line in sublines:
                cid, ts, src, data = line.strip().split('\\t')
                sub.append([cid, ts, src, data])
                
                # update lifetime src counts
                if src in self.config['srcs']:
                    self.metrics['srcs'][src] += 1

                # update window src list
                if src in self.config['wsrcs']:
                    self.tmp['wsrcs'][src].append(ts)
                    
                # update immu
                if src in self.config['immu']:
                    self.metrics['immu'][src] = js.loads(data)
                
                
            # calculate wsrc counts
            for k,v in self.tmp['wsrcs'].items():
                l = [i for i in v if i in wrange(ts,28)]
                self.metrics['wsrcs'][k] = len(l)
                self.tmp['wsrcs'][k] = l
                
            # emit
            for line in sub:
                if line[2] in self.config['emit']:
                    print '\t'.join(line + [js.dumps(self.metrics)])
    
            # update time-since src tmp storage
            for line in sub:
                if line[2] in self.config['tsrcs']:
                    self.tmp['tsrcs'][line[2]] = t
                
class Stream:
    def __init__(self, centricity, config):
        self.centricity = centricity
        self.config = config
        
    def run(self, data):
        for cid, lines in groupby(data, lambda x : x.strip().split('\\t')[0]):
            centricity = self.centricity(config)
            centricity.process_lines(lines)
            
