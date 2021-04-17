from xmlrpc.server import SimpleXMLRPCServer


def temp_resolver(temp):
    if temp > -1 and temp < 10:
        return 'cold'

    elif temp >= 11 and temp <= 20:
        return 'warm'

    else:
        return


server = SimpleXMLRPCServer(("localhost", 8001))
print("Listening on port 8001...")
server.register_function(temp_resolver, "temp_resolver")
server.serve_forever()