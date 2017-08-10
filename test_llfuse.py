#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- Python -*-
#
# $Id: test_llfuse.py $
#
# Author: Markus Stenberg <fingon@iki.fi>
#
# Copyright (c) 2017 Markus Stenberg
#
# Created:       Thu Aug 10 14:48:26 2017 mstenber
# Last modified: Thu Aug 10 16:43:04 2017 mstenber
# Edit time:     24 min
#
"""This module provides test filesystem for measing performance of llfuse
Python binding ( https://github.com/python-llfuse/python-llfuse )

"""

MOUNTPOINT = '/tmp/x'

import errno
import os
import stat

import llfuse

file_inode = llfuse.ROOT_INODE + 1
file_name = b'testfile'


class TestOperations(llfuse.Operations):
    def getattr(self, inode, ctx=None):
        entry = llfuse.EntryAttributes()
        if inode == file_inode:
            entry.st_mode = stat.S_IFREG | 0o644
        elif inode == llfuse.ROOT_INODE:
            entry.st_mode = stat.S_IFDIR | 0o755
        entry.st_nlink = 1
        entry.generation = 0
        entry.entry_timeout = 5
        entry.attr_timeout = 5
        entry.st_gid = os.getgid()
        entry.st_uid = os.getuid()
        entry.st_ino = inode
        entry.st_blksize = 512  # 9 bits
        entry.st_size = os.stat('../testfile').st_size
        entry.st_blocks = entry.st_size / entry.st_blksize
        return entry

    def lookup(self, parent_inode, name, ctx):
        assert parent_inode == llfuse.ROOT_INODE
        if name in ['.', '..']:
            return self.getattr(llfuse.ROOT_INODE)
        if name != file_name:
            raise llfuse.FUSEError(errno.ENOENT)
        return self.getattr(file_inode)

    def open(self, inode, flags, ctx):
        assert inode == file_inode
        global _f
        _f = open('../testfile', 'rb')
        return inode

    def opendir(self, inode, ctx):
        assert inode == llfuse.ROOT_INODE
        return inode

    def read(self, fh, off, size):
        assert fh == file_inode
        global _f
        _f.seek(off)
        return _f.read(size)

    def readdir(self, fh, off):
        assert fh == llfuse.ROOT_INODE
        if off == 0:
            yield file_name, self.getattr(file_inode), 1

    def statfs(self, ctx):
        d = llfuse.StatvfsData()
        return d


def main():
    ops = TestOperations()
    fuse_options = set(llfuse.default_options)
    fuse_options.add('fsname=test_fs')
    fuse_options.discard('nonempty')
    fuse_options.add('max_read=60000')
    # fuse_options.add('debug')
    llfuse.init(ops, MOUNTPOINT, fuse_options)
    r = llfuse.main()
    if r is None:
        llfuse.close()


if __name__ == '__main__':
    main()
