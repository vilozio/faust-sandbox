from statistics import median

import faust
from faust.app.base import BootStrategy
from pyctuator.pyctuator import Pyctuator
from pyctuator.metrics.metrics_provider import MetricsProvider, Metric, Measurement

PREFIX = "faust."


class FaustMonitorProvider(MetricsProvider):
    def __init__(self, monitor):
        self.monitor = monitor

    def get_prefix(self) -> str:
        return PREFIX

    def get_supported_metric_names(self):
        if not self.monitor:
            return []
        return [f'{PREFIX}events_s', f'{PREFIX}events_total', f'{PREFIX}commit_latency.median']

    def get_metric(self, metric_name: str) -> Metric:
        measurements = []
        if self.monitor:
            name = metric_name[len(PREFIX):]
            if 'commit_latency' in name:
                value = median(self.monitor.commit_latency) if self.monitor.commit_latency else 0
                measurements = [Measurement("VALUE", value)]
            else:
                measurements = [Measurement("VALUE", getattr(self.monitor, name))]
        return Metric(metric_name, None, "number", measurements, [])


# Workaround for starting Faust App without Kafka.
# See https://github.com/robinhood/faust/issues/234
class App(faust.App):

    producer_only = True

    class BootStrategy(BootStrategy):
         enable_kafka = False

app = App('demo1')

pyctuator = Pyctuator(
    app.web.web_app,
    "aiohttp Pyctuator",
    app_url="http://localhost:6066",
    pyctuator_endpoint_url="http://localhost:6066/pyctuator",
    registration_url=None
)

pyctuator.pyctuator_impl.register_metrics_provider(FaustMonitorProvider(app.monitor))

@app.crontab('*/2 * * * *')
async def test_message():
    print('EVERY MINUTE I MESSAGE')

if __name__ == '__main__':
    app.main()
