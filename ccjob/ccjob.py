import subprocess as sp
import string
import os
import json
import re
from ccjob.templates import defaults
from ccjob.queue import queue_factory
from ccjob.utils import split_path, module_exists

class Input(object):
    def __init__(self, fpath, inp_string=None, to_file=True):
        self.input_string = inp_string

        # Caution!
        # Assuming $PWD for working directory if not
        # stated otherwise!
        wdir, infile = split_path(fpath)
        base, ext = os.path.splitext(infile)
        self.filepath = os.path.join(wdir, infile)
        self.wdir = wdir
        self.filename = infile
        self.extension = ext
        self.basename = base

        if to_file:
            self.save_input()

    @classmethod
    def from_template(cls, template, fpath, **kwargs):
        """ Alternative constructor using string.Template

        Parameters
        ----------
        template : string.Template
            Template of input file
        fpath : str
            Requested path to input file.
        **kwargs : key-value pairs
            keyworded arguments which have to match template
        """

        try:
            #use defaults first and overwrite with user's specs
            inp = template.substitute(defaults, **kwargs)
            return cls(fpath, inp_string=inp)
        except (KeyError, ValueError) as error:
            print(error)
            print(error.args)
            quit(0)

    @classmethod
    def from_file(cls, path_src):
        """ Alternative constructor just copying an existing input.

        Parameters
        ----------
        path_src : str
            Path to existing input file (source).
        """
        cp_cond = [os.path.exists(path_src), os.path.isfile(path_src),
                   len(path_new) != 0]
        content = ""

        # read input from file
        if cp_cond[0] and cp_cond[1]:
            with open(path_src) as f:
                content = f.read()

        # connect object with file content
        return cls(path_src, inp_string=content, to_file=False)

    def save_input(self):
        """ Save input to file. """
        if not os.path.exists(self.wdir):
            os.makedirs(self.wdir)

        with open(self.filepath, "w") as f:
            f.write(self.input_string)
        print(f"-- Input file [{self.filename}] written successfully.")

class Job(object):
    """ Job Constructor.

        Holds job information.

        Parameters
        ----------
        ccinput : CCJob.Input
            CCJob.Input instance.
        mem : int
            Memory in MB.
        cpus : int
            Number of CPUs.
        time : string
            Time in the format that SLURM accepts (dd-hh, hh:mm:ss).
        partition : string
            Partition name.

        Returns
        -------
        CCJob
            CCJob instance.
        """

    def __init__(self, ccinput, script=None, queue="slurm", mem=500,
                 cpus=1, time="00:15:00", partition=None, jobname="CCJob",
                 software=None, meta_file="meta.json"):
        """ Contructor for Job object.

        Parameters
        ----------
        ccinput : ccjob.Input
            Input object (ccjob).
        script : str
            Submission script (has to be in $PATH) (default: None).
        queue : str, SLURM, PBS
            Name of job scheduler or ccj.Queue instance (default: 'slurm').
        mem : int
            Memory in MB (default: 500).
        cpus : int
            Number of CPUs (default: 1).
        time : str
            Time in scheduler format (default: '00:15:00').
        partition : str
            Partition on which job should be run (default: None).
        jobname : str
            Job name (default: CCJob).
        software : None
            Name of software binary (has to be in $PATH) (default: None).
        meta_file : str
            Name of file used to save meta info (default: 'meta.json').
        """
        self.ccinput = ccinput
        self.script = script
        self.software = software
        if type(queue) == str:
            self.queue = queue_factory(queue)
        elif type(queue) == ccjob.Queue.SLURM:
            self.queue = queue

        self.jobid = None

        self.meta = {"status": None,
            "wdir"     : self.ccinput.wdir,
            "infile"   : self.ccinput.filename,
            "basename" : self.ccinput.basename
        }
        self.meta_filename = os.path.basename(meta_file)
        self.meta_filepath = os.path.join(self.ccinput.wdir, meta_file)

        # submit options
        self.options = {"memory": mem, "cpus": cpus, "time": time,
                        "partition": partition, "jobname": jobname}
        self.custom_options = []
        self.software_options = []

    def get_job_options(self):
        """Prepare the string that holds all options for the queuing manager

        Returns
        -------
        argument : list
            Option string for queuing manager.
        """
        argument = [string.Template(self.queue.template[key]).substitute(
                    {key : value}) for key, value in self.options.items()]

        if len(self.custom_options) > 0:
            argument += self.custom_options

        return argument

    def set_custom_options(self, *args, use_long=True, silent=True, **kwargs):
        """Adds custom queueing manager options.

        Parameters
        ----------
        use_long : bool
            Whether to use long option names which are usually prepended with
            "`--`". The key and value pair is then separated by "=".
            (Default: ``True``)
        silent : bool
            Whether to print the custom options to screen.

        Other Parameters
        ----------------
        args   : tuple
            Tuple of additional flags (no key-value-pair).
        kwargs : dict
            Keywords and their values.

        """
        # TODO: need to automatically decide whether long or short format
        # keyworded arguments
        if use_long:
            self.custom_options.extend(["{0}={1}".format(k, v) for k, v in
                                        kwargs.items()])
        else:
            self.custom_options.extend(["{0} {1}".format(k, v) for k, v in
                                        kwargs.items()])
        # flags
        self.custom_options.extend(args)

        if not silent:
            print("-- Custom options specified: ", " ".join(self.custom_options))

    def is_running(self):
        """ Check whether job is still running.

        This function also changes the status variable. """
        # do we have a job ID to work with?
        if self.jobid == None:
            return False
        else:
            q_status = self.queue.get_status(self.jobid)

        if q_status == self.queue.state["active"]:
            self.meta["status"] = 'PENDING'
            return True
        else:
            return False

    def good_output(self, path_to_outfile,
                   success_string="Have a nice day.",
                   success_fct=None,
                   use_CCParser=True):
        """ Determines whether job terminated successfully.

        This function determines if the quantum chemistry software ended
        normally. It also changes the status variable.

        Parameters
        ----------
        path_to_outfile : str
            Absolute path to output file.
        success_string : str
            String to match in output regarding successful job completion
            (default: 'Have a nice day.').
        success_fct : function(path_to_output)
            Function object for custom parsing (default: None). Has to take
            output path as an input and has to return a boolean.
        use_CCParser : bool
            Use CCParser module if possible (defautl: True).
        """

        # do we have an output file?
        out_exists = os.path.exists(path_to_outfile)
        if not out_exists:
            # status then stays the default, i.e. 'None'
            return False

        normal = False
        # parse output file
        if use_CCParser and module_exists("CCParser"):
            import CCParser as ccp
            #get has_finished
            p = ccp.Parser(path_to_outfile, to_console=False, to_file=False)
            normal = p.results.has_finished[-1]
        else:
            # manual implementation of has_finished
            if success_fct == None:
                with open(path_to_outfile) as out:
                    for line in out:
                        if success_string in line:
                            normal = True
            else:
                normal = success_fct(path_to_outfile)
                if type(gg) != bool:
                    raise TypeError("Success_fct does not yield boolean!")

        if normal:
            self.meta["status"] = 'FIN'
        else:
            self.meta["status"] = 'FAIL'
        return normal

    def is_successful(self, out_extension='out',
                      success_string="Have a nice day.",
                      success_fct=None,
                      ignore_meta=False,
                      use_CCParser=True):
        """ Checks whether job finished with good output.

        In principle there are three cases to be considered:
         (1) Was the job completed and good output written to meta?
         (2) Is the job still running?
         (3) If it finished, did the quantum chemistry software end normally?

        The function changes the state of `self.meta["status"]` and possibly
        serializes `self.meta`.

        Parameters
        ----------
        out_extension : str
            File extension of output file (default: 'out').
        success_string : str
            String to match in output regarding successful job completion
            (default: 'Have a nice day.').
        success_fct : function(path_to_output)
            Function object for custom parsing (default: None). Has to take
            output path as an input and has to return a boolean.
        ignore_meta : bool
            Ignore existing meta file (default: False). Effectively overwrites
            old meta with new one.
        use_CCParser : bool
            Use CCParser module if possible (defautl: True).
        """
        # output info
        outfile = ".".join([self.meta["basename"], out_extension])
        path_to_out = os.path.join(self.meta["wdir"], outfile)

        # Case (1) - output checked previously
        is_fin = os.path.exists(self.meta_filepath) and \
                 self.load_status() == "FIN" and \
                 not ignore_meta

        if not is_fin:
            # Case (2) - active job
            is_running = self.is_running()
            successful = False
            if not is_running:
                # Case (3) - parse output
                successful = self.good_output(path_to_out,
                                        success_string=success_string,
                                        success_fct=success_fct,
                                        use_CCParser=use_CCParser)
            # update meta file
            self.save_meta()
            return not is_running and successful
        else:
            return True

    def submit(self, dry_run=False, silent=False):
        """Submit job to queuing manager in batch mode.

        Parameters
        ----------
        dry_run : bool
            Whether to perform a dry-run job submission (default: False).
        silent : bool
            Whether to print additional information (default: False).
        """
        q_arg = self.get_job_options()

        args = [self.queue.job_submit] \
               + q_arg \
               + [self.script, self.ccinput.filename]
        arg_str = " ".join(args)
        if dry_run:
            print("-- dry-run: ", arg_str)
        else:
            if not silent:
                print("-- running: ", arg_str)
            p = sp.run(arg_str, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
            out = p.stdout.decode("utf-8")
            if len(p.stderr) > 0:
                print("-- stderr: ", p.stderr)
            try:
                self.jobid = self.queue.parse_jobid_batch(out)
            except ValueError:
                print("!! Could not parse Job ID, showing stdout instead:")
                print("-- stdout: ", out)

    def smart_submit(self, dry_run=False, silent=False,
                     out_extension='out',
                     success_string="Have a nice day.",
                     success_fct=None,
                     ignore_meta=False,
                     use_CCParser=True):
        """ Safe-submit job based on meta conditions.

        In principle there are three cases to be considered:
         (1) Was the job completed and we already wrote it to meta?
         (2) Is the job still running?
         (3) If it finished, did the quantum chemistry software end normally?

        Parameters
        ----------
        dry_run : bool
            Whether to perform a dry-run job submission (default: False).
        silent : bool
            Whether to print additional information (default: False).
        out_extension : str
            File extension of output file (default: 'out').
        success_string : str
            String to match in output regarding successful job completion
            (default: 'Have a nice day.').
        success_fct : function(path_to_output)
            Function object for custom parsing (default: None). Has to take
            output path as an input and has to return a boolean.
        ignore_meta : bool
            Ignore existing meta file (default: False). Effectively overwrites
            old meta with new one.
        use_CCParser : bool
            Use CCParser module if possible (defautl: True).
        """
        origin = os.getcwd()
        if not self.is_successful(out_extension=out_extension,
                                  success_string=success_string,
                                  success_fct=success_fct,
                                  ignore_meta=ignore_meta,
                                  use_CCParser=use_CCParser):
            # change directory to wdir (submit needs to be run from there)
            os.chdir(self.meta["wdir"])
            self.submit(dry_run=dry_run, silent=silent)
            # take care of new status info
            self.meta["status"] = 'PENDING'
            self.save_meta()
            # change back to origin folder
            os.chdir(origin)
        elif not silent:
            wdir = self.meta["wdir"]
            print(f"All good. Skipping folder {wdir}/")

    def run(self, dry_run=False, silent=False):
        """Submit job to queuing manager in live mode.

        This function uses the following commmand line structure:

        ``srun <SLURM options> script <input>``

        Parameters
        ----------
        dry_run : bool
            Whether to perform a dry-run job submission (default: False).
        silent : bool
            Whether to print additional information (default: False).
        """
        q_arg = self.get_job_options()

        args = [self.queue.job_run] \
               + q_arg \
               + [self.script, self.ccinput.filename]
        arg_str = " ".join(args)
        if dry_run:
            print("-- dry-run: ", arg_str)
        else:
            if not silent:
                print("-- running: ", arg_str)
            stdout = open("stdout.txt", "w")
            stderr = open("stderr.txt", "w")

            p = sp.run(arg_str, stdout=stdout, stderr=stderr, shell=True)

            stderr.close()
            stdout.close()

    def smart_run(self, dry_run=False, silent=False,
                  out_extension='out',
                  success_string="Have a nice day.",
                  success_fct=None,
                  ignore_meta=False,
                  use_CCParser=True):
        """ Safe-run job interactively based on meta conditions.

        Parameters
        ----------
        dry_run : bool
            Whether to perform a dry-run job submission (default: False).
        silent : bool
            Whether to print additional information (default: False).
        out_extension : str
            File extension of output file (default: 'out').
        success_string : str
            String to match in output regarding successful job completion
            (default: 'Have a nice day.').
        success_fct : function(path_to_output)
            Function object for custom parsing (default: None). Has to take
            output path as an input and has to return a boolean.
        ignore_meta : bool
            Ignore existing meta file (default: False). Effectively overwrites
            old meta with new one.
        use_CCParser : bool
                Use CCParser module if possible (defautl: True).
        """
        origin = os.getcwd()
        if not self.is_successful(out_extension=out_extension,
                                  success_string=success_string,
                                  success_fct=success_fct,
                                  ignore_meta=ignore_meta,
                                  use_CCParser=use_CCParser):
            # change directory to wdir (submit needs to be run from there)
            os.chdir(self.meta["wdir"])
            self.run(dry_run=dry_run, silent=silent)
            # take care of new status information
            self.meta["status"] = 'PENDING'
            self.save_meta()
            # change back to origin folder
            os.chdir(origin)

    def save_meta(self):
        """Dump meta information in json format.
        """
        # jOut = os.path.join(self.meta["wdir"], meta_file)
        with open(self.meta_filepath, "w") as f:
            json.dump(self.meta, f)

    def load_status(self):
        """Read status from meta file.
        """
        # jIn = os.path.join(self.meta["wdir"], meta_file)
        with open(self.meta_filepath, "r") as f:
            tmp = json.load(f)
        if "status" in tmp.keys():
            # self.meta["status"] = tmp["status"]
            return tmp["status"]
