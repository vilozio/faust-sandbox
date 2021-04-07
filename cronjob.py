import faust
from faust.app.base import BootStrategy


# Workaround for starting Faust App without Kafka.
# See https://github.com/robinhood/faust/issues/234
class App(faust.App):

    producer_only = True

    class BootStrategy(BootStrategy):
         enable_kafka = False

app = App('demo1')

@app.crontab('*/2 * * * *')
async def test_message():
    print('EVERY MINUTE I MESSAGE')

if __name__ == '__main__':
    app.main()
