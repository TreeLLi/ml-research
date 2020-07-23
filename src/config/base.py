'''
The base configuration shared by all specific experiments

'''
import os, sys
from warnings import warn
from addict import Dict
from argparse import ArgumentParser

curr_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.join(curr_path, "../..")
if root_path not in sys.path:
    sys.path.insert(0, root_path)


'''
Global path

'''

PATH = Dict()


'''
Dataset

'''

DATA = Dict()


'''
Hyper-parameters

'''

SHARED = ArgumentParser(description='hyper-parameters SHARED by all experiments')

# Global control
SHARED.add_argument('--seed', type=int,
                    help="setting random seed to fix the random generator")

# Devices and Parallel
SHARED.add_argument('--cpu', dest='device', action='store_false',
                    help="force the program to use CPU while the default device is GPU")
SHARED.add_argument('--parallel', action='store_true',
                    help="enable multiprocessing parallel computing")
SHARED.add_argument('--nprocs', type=int, default=0,
                    help="number of subprocesses to be used in parallel computing")
SHARED.add_argument('--world_size', type=int, default=0,
                    help="total number of devices to be distributed on")
SHARED.add_argument('--local_rank', dest='rank', type=int, default=None,
                    help="the rank of process in the parallel group")
SHARED.add_argument('--init_method',
                    help='url used when distributed among various machines')


# Debugging



'''
Configuration

'''

class Configuration:
    def __init__(self, parser):
        parser.parse_args(namespace=self)

        # configurate PATH

        # configurate the selected dataset

        # setting the appropriate device and parallel mode according to the available resources
        if self.device:
            # the initial value of self.device is boolean, true for GPU
            self.device = 'cuda'
            avail_cudas = get_avail_cudas()
            ncudas = len(avail_cudas)
            if ncudas == 0:
                self.device = 'cpu'
                warn("Using CPUs since no accessible CUDA found.")
            elif ncudas>1 and not self.parallel:
                # when multiple cudas available and not parallel computing
                # use the first cuda with maximum free memory 
                free_mem = get_memory_info(self.avail_cudas)
                max_free_idx = free_mem.index(max(free_mem))
                use_device(max_free_idx)
        else:
            self.device = 'cpu'

        if self.parallel:
            ncpus = tc.multiprocessing.cpu_count()
            max_nprocs = ncpus if self.device=='cpu' else min(ncpus, ncudas)
            self.nprocs = min(max_nprocs, self.nprocs) if self.nprocs>0 else max_nprocs
            if self.nprocs <=1:
                self.parallel = False
                warn("Parallel computing is disabled since no multiple devices accessible.")
            else:
                # TODO - support distribution via the network
                self.world_size = self.nprocs
                self.backend = 'gloo' if self.device=='cpu' else 'nccl'
            print("=> Multiprocess distributed on {} {}s".format(self.world_size, self.device.upper()))
        else:
            print("=> Running on single {}".format(self.device.upper()))
            
