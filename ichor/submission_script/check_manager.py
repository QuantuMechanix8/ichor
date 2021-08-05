import os
from typing import List, Optional

from ichor.batch_system import BATCH_SYSTEM
from ichor.common.functools import classproperty
from ichor.logging import logger
from ichor.submission_script.ichor import ICHORCommand
from ichor.submission_script.submision_script import SubmissionScript


class CheckManager:
    def __init__(
        self,
        check_function: str = "default_check",
        check_args: Optional[List[str]] = None,
        ntimes: Optional[int] = None,
    ):
        self.check_function = check_function
        self.check_args = check_args if check_args is not None else []
        self.ntimes = ntimes

    @classproperty
    def NTRIES(self):
        return "ICHOR_N_TRIES"

    @classproperty
    def TASK_COMPLETED(self):
        return "ICHOR_TASK_COMPLETED"

    def check(self, runcmd: str) -> str:
        new_runcmd = ""
        if self.ntimes is not None:
            new_runcmd += f"{self.NTRIES}=0\n"
        new_runcmd += f"export {self.TASK_COMPLETED}=false\n"
        new_runcmd += f'while [ "${self.TASK_COMPLETED}" == false ]\n'
        new_runcmd += "do\n"
        new_runcmd += "\n"

        new_runcmd += runcmd

        new_runcmd += "\n"
        if self.ntimes:
            new_runcmd += f"let {self.NTRIES}++\n"
            new_runcmd += f'if [ "${self.NTRIES}" == {self.ntimes} ]\n'
            new_runcmd += "then\n"
            new_runcmd += "break\n"
            new_runcmd += "fi\n"
        python_job = ICHORCommand()
        if self.check_args:
            python_job.run_function(self.check_function, *self.check_args)
        else:
            python_job.run_function(self.check_function)
        new_runcmd += f"eval $({python_job.repr()})\n"
        new_runcmd += "done\n"
        return new_runcmd


def print_completed():
    ntasks = 0
    if SubmissionScript.datafile_var in os.environ.keys():
        datafile = os.environ[SubmissionScript.datafile_var]
        try:
            with open(datafile, "r") as f:
                for _ in f:
                    ntasks += 1
        except FileNotFoundError:
            # If the datafile hasn't been created then there is no tasks to complete
            pass
    task_id = 1
    if BATCH_SYSTEM.TaskID in os.environ.keys():
        task_id = int(os.environ[BATCH_SYSTEM.TaskID])
    task_last = 1
    if BATCH_SYSTEM.TaskLast in os.environ.keys():
        try:
            task_last = int(os.environ[BATCH_SYSTEM.TaskLast])
        except TypeError:
            pass  # In case SGE_TASK_LAST is undefined
    if task_last < ntasks and task_id + task_last <= ntasks:
        logger.info(f"Running Task {task_id} as {task_id + task_last}")
        task_id += task_last
        logger.info(
            f"ntasks: {ntasks} | task_id: {task_id} | task_last: {task_last}"
        )
        print(f"export {BATCH_SYSTEM.TaskID}={task_id}")
    else:
        print(f"export {CheckManager.TASK_COMPLETED}=true")


def default_check(*args):
    print_completed()
