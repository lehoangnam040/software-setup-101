from confluent_kafka import Producer
import json

p = Producer({'bootstrap.servers': 'localhost:19092,localhost:29092,localhost:39092'})

TOPIC = "train-model"

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

for i in range(10):
    # Trigger any available delivery report callbacks from previous produce() calls
    p.poll(0)

    # Asynchronously produce a message. The delivery report callback will
    # be triggered from the call to poll() above, or flush() below, when the
    # message has been successfully delivered or failed permanently.
    data = {"model-name": f"XYZ-{i}", "config": {"batchsize": 10, "epoch": 400}, "image_size": [400, 600]}
    p.produce(TOPIC, json.dumps(data).encode('utf-8'), callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()

print("Finished producer")