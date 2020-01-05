import tornado.web
# waiting for result
import tornado.ioloop

class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world this is april from backend!")
        self.write({"name": "April", "Age": 10})

class listRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class queryParamRequestHandler(tornado.web.RequestHandler):
    def get(self):
        num = self.get_argument("num")
        if num.isdigit():
            r = "odd" if int(num) % 2 else "even"
            self.write(f"The number {num} is {r}")
        else:
            self.write(f"{num} is not a valid number.")


if __name__ == "__main__":
    app = tornado.web.Application([
        (r"/", basicRequestHandler),
        (r"/animal", listRequestHandler),
        (r"/iseven", queryParamRequestHandler)
    ])

    port = 8882
    app.listen(port)

    print(f"Application is ready and listening to port {port}")
    tornado.ioloop.IOLoop.current().start()