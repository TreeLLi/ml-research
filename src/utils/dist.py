'''
Parallel computing interface

'''

import random, signal
import torch as tc
import torch.backends.cudnn as cudnn
import torch.distributed as dist

from src.utils.sys import monitor_signals

'''
Distribution interface

'''

def run(fn, args):
    if args.seed is not None:
        random.seed(args.seed)
        tc.manual_seed(args.seed)
        cudnn.deterministic = True
        warn('You have chosen to seed training. '
             'This will turn on the CUDNN deterministic setting, '
             'which can slow down your training considerably! '
             'You may see unexpected behavior when restarting '
             'from checkpoints.')

    cudnn.benchmark = True

    if args.parallel:
        tc.multiprocessing.spawn(init_dist, nprocs=args.nprocs, args=(fn, args))
    else:
        fn(args)

        
def init_dist(rank, fn, args):
    args.track_signals()
    
    args.use_device(rank)
    args.rank = rank
    printer.set_rank(rank)
    print("worker {} runs on the device {}".format(rank, args.device))
    
    fargs = args.func_arguments(dist.init_process_group)
    dist.init_process_group(**fargs)

    args.batch_size = int(args.batch_size / args.world_size)
    
    fn(args)

    args.end()
