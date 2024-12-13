import logging
from rq import Worker, Queue, Connection
from dotenv import load_dotenv
from app import create_app

load_dotenv()
logger = logging.getLogger(__name__)


if __name__ == '__main__':

    app = create_app()

    with app.app_context():
        app.run(host='0.0.0.0', port=5000, debug=True)
        
        # Connect to Redis and start listening to the queue
        listen = ['default']
        conn = app.config['SESSION_REDIS']

        with Connection(conn):
            worker = Worker(list(map(Queue, listen)))
            worker.work()
