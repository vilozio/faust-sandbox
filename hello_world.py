import faust

app = faust.App(
    'hello-world',
    broker='kafka://localhost:9092',
    # We are not allowed to create internal topics in Kafka.
    # So we cannot create Faust Tables.
    # See reference https://faust.readthedocs.io/en/latest/userguide/settings.html#topic-allow-declare
    topic_allow_declare=False,
    # We don't use `on_leader=True` and we don't want to create the leader election topic in Kafka.
    # See reference https://faust.readthedocs.io/en/latest/userguide/settings.html#topic-disable-leader
    topic_disable_leader=True,
    # value_serializer='raw',
)

greetings_topic = app.topic('quickstart-events')


@app.agent(greetings_topic)
async def greet(greetings):
    async for greeting in greetings:
        print(greeting)


# @app.agent()
# async def add(stream):
#     async for op in stream:
#         yield op['x'] + op['y']
