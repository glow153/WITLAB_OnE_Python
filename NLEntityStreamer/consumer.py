from kafka import KafkaConsumer

consumer = KafkaConsumer('natural_light_entity',
                         bootstrap_servers='localhost:7777',
                         consumer_timeout_ms=1000)
consumer.subscribe(['natural_light_entity'])

for message in consumer:
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))


