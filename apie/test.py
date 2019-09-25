import service

s = service.Service()


@s.route(path="test/file/api")
def test():
    return "lol"

@s.route(path="test/file/anothapi/meme")
def test():
    return "lol"


print(s.visit_route("test/file/anothapi/meme"))