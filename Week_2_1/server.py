import socketserver
from http.server import SimpleHTTPRequestHandler as SimpleHandler
from DataProvider import DataProvider


class ServerHandler(SimpleHandler):

    def do_GET(self):
        try:
            if(len(self.path) == 0):
                self.send_error(404)
            if(self.path.split("/")[1].lower() != "data"):
                self.send_error(404)

            if not self.path.startswith("/Data"):
                self.send_error(404)
            result = None
            dataProvider = DataProvider()

            pathParts = self.path.split("/")
            if self.path.startswith("/Data/all"):
                # See? Here you need to give all the parameters of Get_data
                # and empty string. You could (should) have changed that 
                # api so that it would be more flexible...
                # Also, you use empty strings and False for kind of the same function.
                result = dataProvider.Get_data(True, "", "", "")
            elif self.check_is_number(pathParts[len(pathParts)-1]) and not self.check_is_number(pathParts[len(pathParts)-2]):
                result = dataProvider.Get_data(
                    False, pathParts[len(pathParts)-1], "", "")
            elif self.check_is_number(pathParts[len(pathParts)-1]) and self.check_is_number(pathParts[len(pathParts)-2]):
                result = dataProvider.Get_data(
                    False, "", pathParts[len(pathParts)-2], pathParts[len(pathParts)-1])
            else:
                self.send_error(404)
            print(self.path)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(result.encode('utf-8'))
        except:
            self.send_error(404)

    def check_is_number(self, val):
        try:
            a = float(val)
            return True
        except ValueError:
            # Actually, it would be better to raise an error here and in the calling code
            # return a status-code 400 (illegal request). 
            return False


PORT = 9000
socketserver.TCPServer.allow_reuse_address = True
http = socketserver.TCPServer(('localhost', PORT), ServerHandler)
print(f'serving on port {PORT}')
http.serve_forever()
