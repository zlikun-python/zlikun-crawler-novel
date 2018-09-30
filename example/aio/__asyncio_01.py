"""
使用 asyncio.Queue 通讯，实现生产者、消息者
"""
import asyncio
from asyncio import Queue


async def producer(queue, workers):
    """
    生产者

    :param queue:
    :param workers:
    :return:
    """
    print("[producer] -- starting --")

    # 向队列中添加任务，这里一共添加16个任务
    for i in range(16):
        await queue.put(i)
        print("[producer] add a task {:02d} to queue".format(i))

    # 向队列中添加结束信号（None值），有几个消费者就要通知几次，否则可能有部分消费者不会退出
    for i in range(workers):
        await queue.put(None)

    print("[producer] waiting for queue to empty")
    # 阻塞住队列，等待队列被清空
    await queue.join()
    print("[producer] -- completed --")


async def consumer(queue, i):
    """
    消费者

    :param queue: 队列
    :param i: 消费者编号
    :return:
    """
    print("[consumer-{}] -- starting --".format(i))
    while True:
        print("[consumer-{}] waiting for item".format(i))
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        else:
            print("[consumer-{}] has item {:02d}".format(i, item))
            queue.task_done()

    print("[consumer-{}] -- completed --".format(i))


async def main(loop, consumer_nums):
    """
    创建一个队列，将队列传递给生产者、消费者任务，等待任务执行完成

    :param loop:
    :param consumer_nums:
    :return:
    """
    queue = Queue(maxsize=32)

    tasks = []
    for i in range(consumer_nums):
        tasks.append(loop.create_task(consumer(queue, i)))
    tasks.append(loop.create_task(producer(queue, consumer_nums)))

    await asyncio.wait(tasks)


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(event_loop, 4))
    finally:
        event_loop.close()
