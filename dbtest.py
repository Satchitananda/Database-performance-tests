from tornado import gen
from tornado.web import asynchronous
import tornado.ioloop
import tornado.web
import MySQLdb
#import pymongo
from pymongo import Connection
from bson.dbref import DBRef
from pymongo.database import Database
from datetime import datetime
#from threadpool import ThreadPool
#import adb
#from functools import partial
import asyncmongo
import apymongo
import mongoengine


enginedb = mongoengine.connect("enginedb2", alias="enginedb")
#MongoEngine views
class User(mongoengine.Document):
    login = mongoengine.StringField(max_length=None)
    name = mongoengine.StringField(max_length=None)
    surname = mongoengine.StringField(max_length=None)
    meta = {"db_alias": "enginedb"}

class Tag(mongoengine.Document):
    tag = mongoengine.StringField(max_length=None)
    meta = {"db_alias": "enginedb"}

class Content(mongoengine.Document):
    author = mongoengine.ReferenceField(User)
    content = mongoengine.StringField(max_length=None)
    tags = mongoengine.ListField(mongoengine.ReferenceField(Tag))
    meta = {"db_alias": "enginedb"}

#MySQL sync connection
mysqlconn = MySQLdb.connect(host = "localhost",
                        user = "root",
                        passwd = "GoG0G6G3",
                        db = "test")
cursor = mysqlconn.cursor()


#MongoDB sync connection
mongoconn = Connection('localhost',27017)
db = mongoconn.testdb
db.content.create_index("author")
db.content.create_index("tags")

_db = mongoconn.testdba
#MySQL async connection
#mysqlaconn = MySQLdb.connect(host = "localhost",
#    user = "root",
#    passwd = "Op3nit3Proj3ct",
#    db = "testa")

#cursora = mysqlaconn.cursor()
#Async mongo

#adb_mysql = adb.Database(driver="MySQLdb", database="test", user="root",
#        password="Op3nit3Proj3ct", host="localhost")

#MongoDB async connection
def get_args(self):
    return {
        "do":self.get_argument("do",""),
        "login":self.get_argument("login","tes"),
        "name":self.get_argument("name","test"),
        "surname":self.get_argument("surname","test"),
        "content":self.get_argument("content",
            """Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of  (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum,  comes from a line in section 1.10.32. The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham. There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which dont look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isnt anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc."""),
        "tag1":self.get_argument("tag1","lorem"),
        "tag2":self.get_argument("tag2","ipsum"),
        "tag3":self.get_argument("tag3","dolor"),
        }

def MySQLInsertData(args, connection=None, callback = None, thread_state=None ):
    docommit = False
    if not connection:
        docommit = True
        connection = thread_state

    cursor = connection.cursor()


    query = "INSERT INTO users (login,name,surname) VALUES('%s','%s','%s');"%(args["login"],args["name"],args["surname"])
    cursor.execute(query)
    nId = cursor.lastrowid
    cursor.execute("INSERT INTO content (user_id,content) VALUES('%d','%s');"%(nId,args["content"]))
    nId = cursor.lastrowid
    cursor.execute("""INSERT INTO tags (content_id,tag) VALUES('%d','%s'),
                                                                           ('%d','%s'),
                                                                           ('%d','%s');"""%(nId,args["tag1"],nId,args["tag2"],nId,args["tag3"]))
    if (docommit):
        connection.commit()

    cursor.close()

    if (callback):
        return callback()


class MySQLHandler(tornado.web.RequestHandler):
    def get(self):
        args = get_args(self)
        #print "Arguments:",args
        #print "Starting MySQL writing database test..."
        #start = datetime.now()
        if args and args["do"]=="post":
            for i in xrange(1):
                MySQLInsertData(args,mysqlconn)

            mysqlconn.commit()
         #   finish = datetime.now() - start
         #   print finish
            return self.write("1")
        elif args and args["do"]=="get":
            print "Starting MySQL reading database test..."
            start = datetime.now()
            fetchdata = cursor.execute("""SELECT c.id as content_id,login,name,surname,content FROM users u
                              INNER JOIN content c ON c.user_id=u.id
                              INNER JOIN tags t ON t.content_id=c.id""")
            
            for row in fetchdata:
                tags = cursor.execute("SELECT tag from tags WHERE content_id = %s"%row[0])
                #print col
            
            finish = datetime.now() - start
            print "Elapsed time",finish
            #return self.write("1")

class MySQLAsyncHandler(tornado.web.RequestHandler):
    pass
'''    def initialize(self,*kwargs,**args):
        self.adb = adb_mysql
        #self._threadpool = ThreadPool(
        #    per_thread_init_func=self.create_connection,
        #    per_thread_close_func=self.close_connection,
        #    queue_timeout=0.1)

    @asynchronous
    def printAllAsync(self,what,callback = None):
        printAll(what,callback)
        callback()

    def create_connection(self):
        try:
            #import MySQLdb
            conn = MySQLdb.connect(db="testa",
                user="root",
                passwd="Op3nit3Proj3ct",
                host="localhost",
                port=3306)
        except Exception as ex:
            raise ex
        return conn

    def close_connection(self, conn):
        conn.close()

    @asynchronous
    def MySQLInsertDataAsync(self,args, connection = None, callback = None):
        self._threadpool.add_task(partial(MySQLInsertData, args, connection), callback)

    @asynchronous
    @gen.engine
    def get(self):
        args = get_args(self)
        start = datetime.now()
        print "This is funny begins"
        #yield gen.Task(printAll,str(datetime.now())+", this is funny begins")
        #self.finish()
        query = ""
        if args and args["do"]=="post":
            for i in xrange(1000):
                #query+="INSERT INTO users (login,name,surname) VALUES('test','test','test');"
                response = yield gen.Task(self.printAllAsync,i)
            #response = yield gen.Task(self.MySQLInsertDataAsync,args)

            finish = datetime.now() - start
            print finish
            self.finish("1")

        elif args and args["do"]=="get":
            start = datetime.now()
            query = """SELECT c.id as content_id,login,name,surname,content FROM users u
                              INNER JOIN content c ON c.user_id=u.id
                              INNER JOIN tags t ON t.content_id=c.id"""

            fetchdata = yield gen.Task(self.adb.runQuery,query)
            for row in fetchdata:
                tags = yield gen.Task(self.adb.runQuery,"SELECT tag from tags WHERE content_id = %s"%row[0])

            finish = datetime.now() - start
            print finish
            self.finish("1")
'''

class MongoAsyncHandler(tornado.web.RequestHandler):
    @asynchronous
    @gen.engine
    def get(self):
        #a_db = asyncmongo.Client(pool_id = "mine_pool",host="localhost",port=27017,dbname="testdb")
        a_conn = apymongo.Connection()
        a_db = a_conn["testdba"]
        args = get_args(self)
        #start = datetime.now()

        if (args and args["do"]=="post"):
            for i in xrange(1):
                login_info = {"login":args["login"],"name":args["name"],"surname":args["surname"]}
                uId = yield gen.Task(a_db.users.insert,login_info)

                tags = [{"tag":args["tag1"]},
                        {"tag":args["tag2"]},
                        {"tag":args["tag3"]}]       
                        
                tagsids = yield gen.Task(a_db.tags.insert,tags)

                content = {"author":DBRef(collection = "users",id = uId),
                           "content":args["content"],
                           "tags":[DBRef(collection = "tags",id = _id) for _id in tagsids]}
                yield gen.Task(a_db.content.insert,content)
                #print content
            #rows = db.content.count()
            #finish = datetime.now() - start
            self.finish("1")
        elif(args and args["do"]=="get"):
            start = datetime.now()
            as_db = asyncmongo.Client(pool_id = "mine_pool",host="localhost",port=27017,dbname="testdba")
            print "Starting MongoDB async reading database test..."
            response = yield gen.Task(as_db.content.find)
            for content in response[0][0]:
                author = _db.dereference(content["author"])
                tags = [_db.dereference(tag) for tag in content["tags"]]
                #print content["content"],author,tags
            finish = datetime.now() - start
            print "Elapsed time:",finish
            self.finish("1")
            
class MongoHandler(tornado.web.RequestHandler):
    def get(self):
        args = get_args(self)

        if (args and args["do"]=="post"):
            #start = datetime.now()
            for i in xrange(1):
                login_info = {"login":args["login"],"name":args["name"],"surname":args["surname"]}
                uId = db.users.insert(login_info)

                tags = [{"tag":args["tag1"]},
                        {"tag":args["tag2"]},
                        {"tag":args["tag3"]}]

                tagsids = db.tags.insert(tags)

                content = {"author":DBRef(collection = "users",id = uId),
                           "content":args["content"],
                           "tags":[DBRef(collection = "tags",id = _id) for _id in tagsids]}
            
                db.content.insert(content)
            #finish = datetime.now() - start
            #print finish
            return self.finish("1")
        elif (args and args["do"]=="get"):
            print "Starting MongoDB reading database test..."
            start = datetime.now() 
            contentlist = db.content.find()
            #print db.content.count()
            for content in contentlist:
                db.dereference(content["author"])
                tags = [db.dereference(tag) for tag in content["tags"]]
                #print author["login"],author["name"],author["surname"],content["content"],tags
            finish = datetime.now() - start
            print "Elapsed time:", finish
            return self.finish("1")

class MongoEngineHandler(tornado.web.RequestHandler):
    def get(self):   
        args = get_args(self)
        if (args and args["do"]=="post"):
            #start = datetime.now()
            for i in xrange(1):
                user = User(login = args["login"],name= args["name"],surname=args["surname"])
                user.save()
                tag1 = Tag(tag=args["tag1"])
                tag1.save()
                tag2 = Tag(tag=args["tag2"])
                tag2.save()
                tag3 = Tag(tag=args["tag3"])
                tag3.save()

                post = Content(content = args["content"],user=user,tags=[tag1,tag2,tag3])
                post.save()
            self.finish("1")
        elif(args and args["do"]=="get"):
            start = datetime.now()
            print "Starting MongoDB reading database test..."
            for post in Content.objects():
                post.author,post.tags

            finish = datetime.now() - start
            print "Elapsed time", finish
            return self.finish("1")

application = tornado.web.Application([
    (r"/my/", MySQLHandler),
    (r"/mya/",MySQLAsyncHandler ),
    (r"/m/",  MongoHandler),
    (r"/ma/", MongoAsyncHandler),
    (r"/me/", MongoEngineHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
