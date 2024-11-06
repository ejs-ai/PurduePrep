class Page:
    def __init__(self, url, body, relevant_lines):
        self.url = url
        self.body = body
        self.relevant_lines = relevant_lines
        # How to use relevant_lines: each value in the list represents a line in the text body that is is suspected to contain a question.
        # Example use:
        #     lines = page_content.body[0].split("\n")
        #     for index in page_content.relevant_lines:
        #          print(lines[index])

    def info(self):
        print("URL: " + self.url)
        print("\n")
        print("BODY: " + str(self.body))
        print("\n")
        print("RELEVANT LINES: "+ str(self.relevant_lines))