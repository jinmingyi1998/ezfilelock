import asyncio
import json
import threading

from filelock import filelock, rwopen

TESTOBJ = {"name": 0}
with open("test.json", "w") as f:
    json.dump(TESTOBJ, f, sort_keys=True, indent=4)
sem = threading.Semaphore(4)


def core(i):
    with filelock.FileLock("test.json") as l:
        with open("test.json", mode="r") as f:
            obj = json.load(f)
            obj["v"] = i
        with open("test.json", mode="w+") as f:
            json.dump(obj, f, indent=4, ensure_ascii=True)
        print(obj)


def core_with_lock(i):
    with filelock.open("test.json") as f:
        obj = json.load(f)
        obj["v"] = i
    with filelock.open("test.json", mode="w+") as f:
        json.dump(obj, f, indent=4, ensure_ascii=True)
    print(obj)


def core_rwlock(i):
    with filelock.open("test.json", mode="r") as f:
        obj = json.load(f)
    with rwopen("test.json", "w") as f:
        obj["name"] = obj["name"] + 1
        json.dump(obj, f, indent=4, ensure_ascii=True)
    print(obj)


async def async_core(i):
    async with filelock.AsyncFileLock("test.json"):
        with open("test.json", mode="r") as f:
            obj = json.load(f)
            obj["v"] = i
        with open("test.json", mode="w+") as f:
            json.dump(obj, f, indent=4, ensure_ascii=True)
        print(obj)


async def core_with_alock(i):
    async with filelock.aopen("test.json") as f:
        obj = json.load(f)
        obj["v"] = i
    async with filelock.aopen("test.json", mode="w+") as f:
        json.dump(obj, f, indent=4, ensure_ascii=True)
    print(obj)


async def amain():
    tasks = (core_with_alock(i) for i in range(1000))
    t = asyncio.gather(*tasks, return_exceptions=True)
    await t


def main():
    threads = [threading.Thread(target=core_rwlock, args=(i,)) for i in range(1000)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # asyncio.run(amain())


if __name__ == "__main__":
    main()
