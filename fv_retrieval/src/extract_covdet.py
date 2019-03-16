#!/usr/bin/env python
# encoding: utf-8
# Author: yongyuan.name

import os
import multiprocessing
from multiprocessing import Process, freeze_support, Pool


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ]


def cpu_task(img_names, bbin, db_dir, save_dir):
    try:
        for i, line in enumerate(img_names):
            img_path = os.path.join(db_dir, line)
            cmd = bbin + ' ' + img_path + ' ' + save_dir
            os.system(cmd) # returns the exit status
            print "%d(%d), %s" %(i+1, len(img_names), line)
    except:
        import traceback
        traceback.print_exc()
        raise


if __name__ == '__main__':

    multiprocessing.freeze_support()
    pool = multiprocessing.Pool()

    parts = 10
    bbin = '/home/yuanyong/cpp/covdet/build/demo'
    from score_retrieval.data import datasets_str
    txt_path = './data/{}.txt'.format(datasets_str)
    db_dir = ''  # ./datasets/oxford
    save_dir = './covdet_sifts/'

    with open(txt_path, 'r') as f:
        content = f.readlines()
        content = [x.strip() for x in content]
    blocks = split_list(content, wanted_parts = parts)

    for i in xrange(0, parts):
        pool.apply_async(cpu_task, args=(blocks[i], bbin, db_dir, save_dir,))
    pool.close()
    pool.join()
