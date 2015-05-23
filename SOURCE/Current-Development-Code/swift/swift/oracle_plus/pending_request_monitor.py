__author__ = 'mcouceiro'

from threading import Lock
import time
from swift.oracle_plus.utility import log_oracle_plus
from swift.oracle_plus.config import REPLICA_COUNT,PENDING_REQ_MONITOR_TIMEOUT

class PendingRequestMonitor(object):

    _old_pile = None
    _new_pile = []
    _new_pile_lock = Lock()
    _num_replicas = 0
    _timeout = 0

    def init(self, num_replicas, timeout):
        self._num_replicas = num_replicas
        self._timeout = timeout

    def add_new_request(self, request):
        if self._is_request_pending(request):
            self._new_pile_lock.acquire()
            self._new_pile.append(request)
            self._new_pile_lock.release()

    def check_pending_requests(self, discard_old):
        self._new_pile_lock.acquire()
        log_oracle_plus("New Pile count = "+str(len(self._new_pile)))
        self._old_pile =list(self._new_pile)
        log_oracle_plus("Old Pile count = "+str(len(self._old_pile)))
        self._new_pile = []
        self._new_pile_lock.release()

        if not discard_old:
            attempt=0
            while attempt > 3:
                attempt+=1
                still_pending_requests = []
                for request in self._old_pile:
                    if self._is_request_pending(request):
                        still_pending_requests.append(request)
                pending_req_count=len(still_pending_requests)
                log_oracle_plus("Pending requests monitor Attempt = "+str(attempt)+" Pending request count = "+str(pending_req_count))
                if pending_req_count > 0:
                    time.sleep(self._timeout) #after this assume the nodes are dead and move on
                else:
                    break

        self._old_pile = []

    def _is_request_pending(self, req):
        num_resp = 0
        for response in req:
            if response:
                num_resp += 1
        return num_resp < self._num_replicas


#pseudo_singleton
_replica_recon = PendingRequestMonitor()
_replica_recon.init(REPLICA_COUNT,PENDING_REQ_MONITOR_TIMEOUT)


def get_pending_req_monitor():
    return _replica_recon



