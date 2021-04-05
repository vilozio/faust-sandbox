import faust

app = faust.App(
    'topic-monitor',
    broker='kafka://localhost:9092',
    # We are not allowed to create internal topics in Kafka.
    # So we cannot create Faust Tables.
    # See reference https://faust.readthedocs.io/en/latest/userguide/settings.html#topic-allow-declare
    topic_allow_declare=False,
    # We don't use `on_leader=True` and we don't want to create the leader election topic in Kafka.
    # See reference https://faust.readthedocs.io/en/latest/userguide/settings.html#topic-disable-leader
    topic_disable_leader=True,
    value_serializer='raw',
)

greetings_topic = app.topic('quickstart-events')


@app.agent(greetings_topic)
async def greet(greetings):
    async for greeting in greetings:
        print(greeting)


# https://faust.readthedocs.io/en/latest/userguide/sensors.html
@app.page('/stats')
async def get_stats(self, request):
    return self.json({
        'events_s': app.monitor.events_s,
        'events_total': app.monitor.events_total,
        'commit_latency': app.monitor.commit_latency,
        'assignment_latency': app.monitor.assignment_latency,
        'assignments_failed': app.monitor.assignments_failed,
    })
