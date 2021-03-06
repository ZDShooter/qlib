# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import sys, traceback, signal, atexit
from . import R
from .recorder import Recorder
from ..log import get_module_logger

logger = get_module_logger("workflow", "INFO")


# function to handle the experiment when unusual program ending occurs
def experiment_exit_handler():
    """
    Method for handling the experiment when any unusual program ending occurs.
    The `atexit` handler should be put in the last, since, as long as the program ends, it will be called.
    Thus, if any exception or user interuption occurs beforehead, we should handle them first. Once `R` is
    ended, another call of `R.end_exp` will not take effect.
    """
    signal.signal(signal.SIGINT, experiment_kill_signal_handler)  # handle user keyboard interupt
    sys.excepthook = experiment_exception_hook  # handle uncaught exception
    atexit.register(R.end_exp, recorder_status=Recorder.STATUS_FI)  # will not take effect if experiment ends


def experiment_exception_hook(type, value, tb):
    """
    End an experiment with status to be "FAILED". This exception tries to catch those uncaught exception
    and end the experiment automatically.

    Parameters
    type: Exception type
    value: Exception's value
    tb: Exception's traceback
    """
    logger.error(f"An exception has been raised[{type.__name__}: {value}].")

    # Same as original format
    traceback.print_tb(tb)
    print(f"{type.__name__}: {value}")

    R.end_exp(recorder_status=Recorder.STATUS_FA)


def experiment_kill_signal_handler(signum, frame):
    """
    End an experiment when user kill the program through keyboard (CTRL+C, etc.).
    """
    R.end_exp(recorder_status=Recorder.STATUS_FA)
