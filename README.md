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
python-llfuse | 165MB/s (1% of /dev/zero)
go-fuse | 315MB/s (2% of /dev/zero)


