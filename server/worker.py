import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = "redis://redistogo:436473da6c8d57832bbf8ac3235490a0@sculpin.redistogo.com:10283"

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
