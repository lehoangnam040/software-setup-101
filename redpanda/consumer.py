from confluent_kafka import Consumer, TopicPartition
import time
import json

c = Consumer({
    'bootstrap.servers': 'localhost:19092,localhost:29092,localhost:39092',
    'group.id': 'train-worker-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,
})

TOPIC = "train-model"

c.subscribe([TOPIC])

try:
    while True:
        print("wait for message")
        messages = c.consume(num_messages=1, timeout=-1)
        if not messages:
            continue
        msg = messages[0]
        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        _data = json.loads(msg.value().decode('utf-8'))
        print('Received message: {}'.format(_data))
        offset = msg.offset()
        partition = msg.partition()
        print(f"offset: {msg.offset()} in partition: {msg.partition()}")
        # processing
        print("process message")
        for i in range(5):
            print("------------")
            # raise exception here if want to test message interrupt
            # a = 1 / 0
            time.sleep(5)
        try:
            res = c.commit(asynchronous=False)
        except Exception as err:
            print("error on commit", err)
        else:
            print(res)
            print("commited, wait new message")
        # break
except Exception as err:
    print(err, "*********************")
finally:
    c.close()
