__author__ = 'mcouceiro'

from threading import Lock
import time
import oracle


class ReplicaReconciliation(object):

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
        self._old_pile = self._new_pile
        self._new_pile = []
        self._new_pile_lock.release()

        if not discard_old:
            oracle.get_metrics_gatherer().set_reconciliation_clock_init()
            still_pending_requests = []
            for request in self._old_pile:
                if self._is_request_pending(request):
                    still_pending_requests.append(request)

            if len(still_pending_requests) > 0:
                time.sleep(self._timeout) #after this assume the nodes are dead and move on
            oracle.get_metrics_gatherer().set_reconciliation_clock_end()

        self._old_pile = []

    def _is_request_pending(self, req):
        num_resp = 0
        for response in req:
            if response:
                num_resp += 1
        return num_resp < self._num_replicas


#pseudo_singleton
_replica_recon = ReplicaReconciliation()


def get_replica_reconciliation():
    return _replica_recon


