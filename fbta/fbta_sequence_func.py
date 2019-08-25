import time

from fbta_difftime import FBTADifftime
from fbta_log import log, log_header, log_summery
from fbta_settings import FBTASettings
from fbta_configs import FBTAConfigs


class FBTASequenceFunction:
    def __init__(self, settings:FBTASettings, configs:FBTAConfigs):
        self._settings = settings
        self._configs = configs

        self._time_start_all = time.time()
        self._time_start_process = time.time()

    def _warnningTimeOptimize(self):
        if self._settings.renew_index:
            print('>> WARNNING: IndexRenew is TRUE <<')

    def _showFinishedProcessEndNotify(self, order):

        stra = ':Sequence: Procress {order} START {start} FINISHED {fin} SPEND {spend} ALL {spendall}'
        log_summery(stra.format(
            order=order,
            start=FBTADifftime.timestamp2date(self._time_start_all),
            fin=FBTADifftime.timestamp2date(time.time()),
            spend=FBTADifftime.printTimeDiff(self._time_start_process),
            spendall=FBTADifftime.printTimeDiff(self._time_start_process)
        ))
        self._time_start_process = time.time()

    def _isInTestStep(self, step):
        test_step = self._settings.test_step
        is_run = -99 if not test_step else test_step

        if type(is_run) == int and is_run == -99:
            log_header(f':Sequence: Run All Case in step = {step}')
            return True
        elif type(is_run) == list and step in is_run:
            log_header(f':Sequence: Run Some Case in step = {step} of {test_step}')
            return True
        else:
            return False
