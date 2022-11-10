import builtins
import contextlib
import threading
import time
from typing import Dict

from .filelock import FileLock


class RWLock:
    def __init__(self, filepath):
        self.filepath = filepath
        self.read_count = 0
        self.write_lock = FileLock(filepath)

    def read_acquire(self):
        with self.write_lock:
            self.read_count += 1
            assert self.read_count >= 0

    def read_release(self):
        with self.write_lock:
            self.read_count -= 1
            assert self.read_count >= 0

    def write_acquire(self, delay=0.05):
        while True:
            self.write_lock.acquire()
            if self.read_count == 0:
                return
            self.write_lock.release()
            time.sleep(delay)

    def write_release(self):
        self.write_lock.release()


class ReadWriteFileLock:
    lock_dict: Dict[str, RWLock] = {}
    share_lock = threading.Lock()

    def __init__(self, filepath):
        self.filepath = filepath
        with self.share_lock:
            if filepath not in self.lock_dict:
                self.lock_dict[filepath] = RWLock(filepath)

    def read_acquire(self):
        self.lock_dict[self.filepath].read_acquire()

    def read_release(self):
        self.lock_dict[self.filepath].read_release()

    def write_acquire(self):
        self.lock_dict[self.filepath].write_acquire()

    def write_release(self):
        self.lock_dict[self.filepath].write_release()


@contextlib.contextmanager
def rwopen(filepath, mode, *args, **kwargs):
    lock = ReadWriteFileLock(filepath)
    if "w" in mode or "a" in mode:
        lock.write_acquire()
        release_fn = lock.write_release
    else:
        lock.read_acquire()
        release_fn = lock.read_release
    with builtins.open(filepath, mode, *args, **kwargs) as fp:
        yield fp
    release_fn()
