import re
import subprocess as sp


class JobScheduler(object):
    """ Empty base class for job schedulers."""
    def __init__(self):
        pass

class SLURM(JobScheduler):
    job_submit = "sbatch"
    job_run = "srun"
    job_allocate = "salloc"

    template = {"partition" : "--partition=$partition",
                "memory"    : "--mem=$memory",
                "time"      : "--time=$time",
                "cpus"      : "--cpus-per-task=$cpus",
                "jobname"   : "--job-name=$jobname"
               }

    state = {"active": "RUNNING",
             "finished": "COMPLETE",
             "failed" : "FAILED",
             "cancelled" : "CANCELLED",
             "timeout" : "TIMEOUT"
            }

    inv_state = {v: k for k, v in state.items()}

    def __init__(self):
        pass

    def parse_jobid_batch(self, submit_string):
        p = r"Submitted batch job\s+(\d+)"
        match = re.search(p, submit_string)
        if match:
            return match.group(1)
        else:
            raise ValueError("Could not parse job ID!")

    def get_status(self, jobid):
        """ Get job status from 'sacct'
        """
        sacct = f"sacct -j {jobid}"
        p = sp.run(sacct, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        out = p.stdout.decode("utf-8")

        # process string
        lines = out.split('\n')
        istatus = lines[0].split().index("State")
        if len(lines) > 2:
            return lines[2].split()[istatus]
        else:
            raise IndexError(f"No status found for Job ID {jobid}!")

    def tformat(self, days=0, hours=0, minutes=0):
        if any([days < 0, hours < 0, minutes < 0]):
            raise ValueError("Only non-negative integers allowed for time format!")
        if all([days == 0, hours == 0, minutes == 0]):
            minutes = str(15)
        if days > 0:
            time_string = "{0}-{1}".format(days, hours)
        if days == 0 and hours > 0:
            time_string = "{0}:{1}".format(hours, minutes)
        if days == 0 and hours == 0:
            time_string =  str(minutes)
        return time_string

class PBS(JobScheduler):
    job_submit = "qsub"
    job_run = "qsub"
    job_interactive = "qsub -I"

    template = {"partition" : "-q $partition",
                "memory"    : "-l mem=$memory",
                "time"      : "-l walltime=$time",
                "cpus"      : "-l ncpus=$cpus",
                "jobname"   : "-N $jobname"
               }

def queue_factory(q_string):
    if q_string.lower() == "slurm":
        return SLURM()
    elif q_string.lower() == "pbs":
        return PBS()
    else:
        raise NotImplementedError("Currently only SLURM class is functional!")
