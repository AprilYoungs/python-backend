# web application module
import tornado.web
# input and output loop module
import tornado.ioloop
import json
import os

class rootRequestHandler(tornado.web.RequestHandler):
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
            # read file
            content = f.read().splitlines()
            # to json
            jsonContent = json.dumps(content)
            # return a json read from server
            self.write(jsonContent)
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


class videosRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("videos.html")

class listVideosRequestHandler(tornado.web.RequestHandler):
    def get(self):
        list = os.listdir("./video")
        result = {'msg': 'success', 'list': list}
        self.write(json.dumps(result))

if __name__ == "__main__":
    app = tornado.web.Application([
        # create the root request, return a html
        (r"/", rootRequestHandler),
        # the basic get, no parameter
        (r"/quoting", quotingRequestHandler),
        # get with query params
        (r"/isEven", queryParamRequestHandler),
        # [A-z] A to z, "+" infinity
        (r"/students/([A-z]+)/([0-9]+)", resourceParamRequestHandler),
        # load and show server file
        (r"/list", listRequestHandler),
        
        # images 
        (r"/uploadImg", uploadPageRequestHandler),
        #  read server's files
        #  The handler constructor requires a ``path`` argument, which specifies the
        #  local root directory of the content to be served.
        (r"/img/(.*)", tornado.web.StaticFileHandler, {"path": "img"}),

        # videos
        (r"/videos", videosRequestHandler),
        (r"/videosList", listVideosRequestHandler),
        (r"/video/(.*)", tornado.web.StaticFileHandler, {"path": "video"})
    ])

    port = 8801
    app.listen(port)

    print(f"Application is ready and listening to port {port}")
    tornado.ioloop.IOLoop.current().start()
