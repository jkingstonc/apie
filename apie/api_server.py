import service

s = service.Service()

@s.route(path="test/folder/api_first")
def first_api():
    return ["This is the first api return! (In a list wow!)"]

@s.route(path="test/folder/api_second")
def second_api():
    return "This is the second api return!"

if __name__ == "__main__":
    s.start()