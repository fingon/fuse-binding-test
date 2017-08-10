Assorted tests of FUSE language bindings.
-----------------------------------------

I am mostly interested in two things _for reading_. Therefore, the
language binding provided fake file systems provide following:

* file reading performance
    * 'infinite' file; can be used to play with dd

* directory iteration performance (TBD)


backend | read perf
------- | ------------------
native ( /dev/zero ) | 16GB/s
go-fuse | 315MB/s
python-llfuse | 165MB/s

Also, testing with real 'testfile' (raspbian installation image) on my laptop;

backend | read perf
------- | ------------------
native | ~900MB/s
go-fuse | 290MB/s
python-llfuse | 115MB/s

It seems that Python binding uses at most 4kb block size, even with
appropriate mount options, on OS X. It renders it relatively .. slow.


