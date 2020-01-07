import tornado.web
# waiting for result
import tornado.ioloop
import json

class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        # return and a html from a file
        self.render("index.html")


class quotingRequestHandler(tornado.web.RequestHandler):
    def get(self):
        # just return a sentence
        self.write("Life begin at the end of comfort zone.")

class queryParamRequestHandler(tornado.web.RequestHandler):
    def get(self):
        # deal with arguments
        num = self.get_argument("num")
        if num.isdigit():
            r = "odd" if int(num) % 2 else "even"
            self.write(f"The number {num} is {r}")
        else:
            self.write(f"{num} is not a valid number.")

class resourceParamRequestHandler(tornado.web.RequestHandler):
    def get(self, studentName, courseId):
        # get regex path, this can just return html, or anything you like
        self.write(f"Welcome {studentName} the course you are enter is {courseId}")


class listRequestHandler(tornado.web.RequestHandler):
    def get(self):
        with open("data.txt", "r") as f:
            # return a json read from server
            self.write(json.dumps(f.read().splitlines()))
    def post(self):
        with open("data.txt", "a") as f:
            # just get the argument, body first then url
            print(f"{self.get_argument('animal')}")
            # just get the query argument in the url
            print(f"{self.get_query_argument('animal')}")
            # just get the body argument in "form-data"
            # print(f"{self.get_body_argument('animal')}")
            animal = self.get_argument("animal")
            f.write("\n"+animal)
            self.write({"msg": f"{animal} is successful added"})


class uploadPageRequestHandler(tornado.web.RequestHandler):
    """
        get: show the upload html page
        post: handler upload request
    """
    def get(self):
        # return and a html from a file
        self.render("uploadImg.html")
    
    def post(self):
        # save uploaded files
        remoteFiles = self.request.files["imageFile"]
        # {'body': binary file,
        # 'content_type': file type,
        # 'filename': remote file name}

        fileUrls = ""
        for f in remoteFiles:
            with open(f"img/{f.filename}", "wb") as newFile:
                newFile.write(f.body)
                fileUrls += f"<a href='./img/{f.filename}'>{f.filename}</a>\n"
        self.write(fileUrls)

if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", basicRequestHandler),
        (r"/quoting", quotingRequestHandler),
        (r"/isEven", queryParamRequestHandler),
        # [A-z] A to z, "+" infinity
        (r"/students/([A-z]+)/([0-9]+)", resourceParamRequestHandler),
        (r"/list", listRequestHandler),
        
        # images 
        (r"/uploadImg", uploadPageRequestHandler),
        #  read server's files
        #  The handler constructor requires a ``path`` argument, which specifies the
        #  local root directory of the content to be served.
        (r"/img/(.*)", tornado.web.StaticFileHandler, {"path": "img"})
    ])

    port = 9000
    app.listen(port)

    print(f"Application is ready and listening to port {port}")
    tornado.ioloop.IOLoop.current().start()
