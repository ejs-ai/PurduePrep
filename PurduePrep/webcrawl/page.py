class Page:
    def __init__(self, url, body):
        self.url = url
        self.body = body

    def info(self):
        print("URL: " + self.url)
        print("\n")
        print("BODY: " + self.body)