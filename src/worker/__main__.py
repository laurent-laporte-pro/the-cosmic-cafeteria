from . import create_worker

if __name__ == '__main__':
    worker = create_worker()
    worker.work()