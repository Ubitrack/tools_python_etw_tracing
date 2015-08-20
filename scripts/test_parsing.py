

from etw import TraceEventSource, EventConsumer, EventHandler
from etw.descriptors import image
import exceptions
import os
import numpy as np

from etw.descriptors import uteventqueue

class TestConsumer(EventConsumer):

    def __init__(self):
        self.eventqueue_stats = {}

    # @EventHandler(uteventqueue.Event.DispatchBegin)
    # def OnDispatchBegin(self, event_data):
    #   print event_data.time_stamp, event_data.EventDomain, event_data.Priority, event_data.ComponentName, event_data.PortName

    @EventHandler(uteventqueue.Event.DispatchEnd)
    def OnDispatchEnd(self, event_data):
        key = (event_data.EventDomain, event_data.ComponentName, event_data.PortName)
        samples = self.eventqueue_stats.setdefault(key, [])
        samples.append(np.asarray((event_data.time_stamp, event_data.Priority, event_data.Duration)))


ts = TestConsumer()
tes = TraceEventSource([ts], True)

print "open tracefile"
tes.OpenFileSession("C:/Users/Ulrich/Documents/xperftraces/2015-20-08_17-49-25_Ulrich.etl")

print"parsing entries ..."
tes.Consume()

print "average time (ms)"
for k in sorted(ts.eventqueue_stats.keys()):
    values = ts.eventqueue_stats[k]
    data = np.vstack(values)
    ed, cn, pn = k
    print "%s:%s-%s (%d) = %0.5f" % (ed, cn, pn, len(values), data[:,2].mean())

