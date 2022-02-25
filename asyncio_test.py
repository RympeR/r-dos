import asyncio

SIZE = 100000


class Counter():
  def __init__(self):
    self.values = [0] * SIZE

  async def count(self):
    while True:
      await asyncio.sleep(0)  # Explicitly yield to other coroutines.
      for i in range(SIZE):
        self.values[i] += 1

  async def heartbeat(self):
    loop = asyncio.get_event_loop()
    t0 = loop.time()

    while True:
      await asyncio.sleep(1.0)

      # Check for consistency.
      for i in range(SIZE):
        assert self.values[i] == self.values[0]

      now = loop.time()
      print(f'All values are {self.values[0]} at +{now - t0:.5f}s')


async def main():
    counter = Counter()

    tasks = map(asyncio.create_task, [counter.count(), counter.heartbeat()])
    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == '__main__':
    asyncio.run(main())