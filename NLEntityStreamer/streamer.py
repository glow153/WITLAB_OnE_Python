import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from nldc_entity.cas_entity import CasEntity
from kafka import KafkaProducer


class HttpSender:

    def __init__(self):
        pass

    def send(self, data):
        pass


class MyEventHandler(FileSystemEventHandler):
    kafka_producer = None

    def __init__(self, observer, filename):
        self.observer = observer
        self.filename = filename
        # self.kafka_producer = producer

    def on_created(self, event):
        # TODO: send nl entity to server
        if event.event_type == 'created':
            time.sleep(1)  # for waiting for creating completed
            entity = CasEntity(event.src_path)
            print('send>>', entity.get_element('time'), ':', entity.get_category())
            # self.kafka_producer.send('natural_light_entity',
            #                          str(entity.get_element('time') + ':' + entity.get_category()).encode('ascii'))
        else:
            pass


class NLEntityStreamer:
    def __init__(self):
        self.dirpath = 'D:/Desktop/20181212'

    def start_streaming(self):
        # producer = KafkaProducer(bootstrap_servers='210.102.142.14:9092')

        observer = Observer()
        event_handler = MyEventHandler(observer, self.dirpath)
        observer.schedule(event_handler, self.dirpath, recursive=True)
        observer.start()
        print('watchdog started.')
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


if __name__ == "__main__":
    NLEntityStreamer().start_streaming()
