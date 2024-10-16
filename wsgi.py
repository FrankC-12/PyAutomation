import gevent
import gevent.monkey
from automation import PyAutomation, server

gevent.monkey.patch_all()

app = PyAutomation()
app.define_dash_app(server=server)
app.run(create_tables=True)