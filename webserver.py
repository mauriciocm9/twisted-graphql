from twisted.web import server, resource
from twisted.internet import reactor, endpoints
from urllib.parse import unquote
from graphqlview import GraphQLView
from schema import schema

class Counter(resource.Resource):
    isLeaf = True

    def __init__(self, schema):
        self.schema = schema
        self.graphqlview = GraphQLView(self.schema)

    def render_GET(self, request):
        request.setHeader(b"content-type", b"text/plain")
        content = u"I am request #{}\n"
        return content.encode("ascii")

    def render_POST(self, request):
        # print(request.getAllHeaders())
        print(request.content.read())
        # print(request.content.getvalue())
        request.setHeader(b"content-type", b"application/json")
        return self.graphqlview.dispatch(request)



CounterInstance = Counter(schema)
endpoints.serverFromString(reactor, "tcp:8080").listen(server.Site(CounterInstance))
reactor.run()
