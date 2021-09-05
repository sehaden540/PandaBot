from flask import Flask
from multiprocessing import Process, freeze_support
from time import sleep
import GoLive

app = Flask(__name__)

def run_app():
    app.run(host='localhost', port=80)


if __name__ == '__main__':
    freeze_support()
    server = Process(target=run_app)
    server.start()
    sleep(1)
    with app.test_request_context('/'):
        GoLive.main()
    server.terminate()
    server.join()
