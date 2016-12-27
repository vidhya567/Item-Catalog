from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base,Restaurant,MenuItem
engine=create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBsession=sessionmaker(bind = engine)
ses=DBsession()

def main():
     try:
        port=8080
        server=HTTPServer(('',port),WebServerHandler)
        print("Web Server running on port %s"%port)
        engine=create_engine('sqlite:///restaurantmenu.db')
        server.serve_forever()
     except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

class WebServerHandler(BaseHTTPRequestHandler):
    ##def create_session(self):
    ##  engine=create_engine('sqlite:///restaurantmenu.db')
    ##  Base.metadata.bind=engine
    ##  DBsession=sessionmaker(bind=engine)
    ##  ses=DBsession()
    ##  return ses


    def do_GET(self):
         try:
            # Objective 3 Step 2 - Create /restarants/new page
           if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return
           if self.path.endswith("/edit"):
              restid=self.path.split('/')[2]
              print restid
              q=ses.query(Restaurant).filter_by(id=restid).one()
              if q:
                self.send_response(200)
                self.send_header('Content-Type','text/html')
                self.end_headers()
                output=""
                output+="<html><body>"
                output+="<h1>Change the restaurant name</h1>"
                output+="<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>"%restid
                output+="<input name='Updaterestaurantname' type='text' placeholder='New Restaurant Name'>"
                output+="<input type='submit' value='Update'>"
                output+="</form></body></html>"
                print output
                self.wfile.write(output)
                return
           if self.path.endswith("/delete"):
              restid=self.path.split('/')[2]
              print restid
              quer=ses.query(Restaurant).filter_by(id=restid).one()
              if quer:
                self.send_response(200)
                self.send_header('Content-Type','text/html')
                self.end_headers()
                output=""
                output+="<html><body>"
                output+="<h1>Are you sure you want to delete this Restaurnat entry</h1>"
                output+="<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>"%restid
                output+="<input type='submit' value='Delete'>"
                output+="</form>"
                output+="<a href='/restaurants'>Go Baack to home page</a>"
                output+="</body></html>"
                self.wfile.write(output)
                
                
                #return 
           if self.path.endswith("/restaurants"):
               self.send_response(200)
               self.send_header('Content-Type','text/html')
               self.end_headers()
               ##ses=create_session()
               output=""
               output+="<html><body>"
               output+="<a href='/restaurants/new'>Create a New Restaurant Here</a>"
               output+="</br>"
               rests=ses.query(Restaurant).all()
               for r in rests:
                 output+= r.name
                 hashqi="#"
                 output+="</br>"
                 output+="<a href='/restaurants/%s/edit'>Edit</a>"%r.id
                 output+="</br>"
                 output+="<a href='/restaurants/%s/delete'>Delete</a>"%r.id
                 output+= "</br></br>"
               output+="</body></html>"
               self.wfile.write(output)
               return
    

         except IOError:
            self.send_error(404,"File Not Found %s"%self.path)

    def do_POST(self):
        try:
           if(self.path.endswith("/restaurants/new")):
            ctype,pdict=cgi.parse_header(self.headers.getheader('content-type'))
            if(ctype=='multipart/form-data'):
                fields=cgi.parse_multipart(self.rfile,pdict)
                messagecontent=fields.get('newRestaurantName')
            newrest=Restaurant(name=messagecontent[0])
            ses.add(newrest)
            ses.commit()
            self.send_response(301)
            self.send_header('Content-Type','text/html')
            self.send_header('Location','/restaurants')
            self.end_headers()
            

           if(self.path.endswith("/edit")):
              restid=self.path.split('/')[2]
              print restid
              ctype,pdict=cgi.parse_header(self.headers.getheader('content-type'))
              if(ctype=='multipart/form-data'):
                 fields=cgi.parse_multipart(self.rfile,pdict)
                 updatename=fields.get('Updaterestaurantname') 
              entry=ses.query(Restaurant).filter_by(id = restid).one()
              entry.name=updatename[0]
              ses.add(entry)
              ses.commit()
              self.send_response(301)
              self.send_header('Content-Type','text/html')
              self.send_header('Location','/restaurants')
              self.end_headers()

           if(self.path.endswith("/delete")):
                restid=self.path.split('/')[2]
                entry=ses.query(Restaurant).filter_by(id = restid).one()
                if entry:
                    ses.delete(entry)
                    ses.commit()
                    self.send_response(301)
                    self.send_header('Content-Type','text/html')
                    self.send_header('Location','/restaurants')
                    self.end_headers()
                

        except:
            pass


if __name__ == '__main__':
    main()
# #if self.path.endswith("/hello"):
#           self.send_response(200)
#           self.send_header('Content-Type','text/html')
#           self.end_headers()
#           message=""
#           message+="<html><body>"
#           message+="<h1>Hello!</h1>"
#           message+='''<form method='POST' enctype='multipart/form-data' action='/hello' ><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value="Submit">'''
#           message+="</html></body>"
#           self.wfile.write(message)
#           print message
#           return
#          if self.path.endswith("/hola"):
#           self.send_response(200)
#           self.send_header('Content-Type','text/html')
#           self.end_headers()
#           message=""
#           message+="<html><body>"
#           message+="<h1>&#161 Hola !</h1>"
#           ##message+="<a href='/hello'>Back to Hello</a>"
#           message+='''<form method='POST' enctype='multipart/form-data' action='/hello' ><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value="Sumbit">'''
#           message+="</body></html>"
#           self.wfile.write(message)
#           print message
#           return #

