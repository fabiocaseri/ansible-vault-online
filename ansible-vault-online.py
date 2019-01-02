
import os
from twisted.application import internet, service
from twisted.web import server

from scripts import resources

app = service.MultiService()
web_root = resources.Root('./web')
web_root.putChild(b'crypt', resources.Crypt())
web_factory = server.Site(web_root)
web_service = internet.TCPServer(8081, web_factory, interface='0.0.0.0')
web_service.setServiceParent(app)

application = service.Application("ansible-vault")

app.setServiceParent(application)

