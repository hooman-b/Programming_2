import socketserver
from http.server import SimpleHTTPRequestHandler as SimpleHandler
from DataProvider import DataProvider

class ServerHandler(SimpleHandler):
    """
    Type: Inherits from SimpleHandler to handle HTTP GET requests.
    Explanation: Custom request handler for the server.
    """

    def do_GET(self):
        """
        Explanation: Handle incoming HTTP GET requests. Parses the request path,
                     processes query parameters, and communicates with DataProvider.
                     Responds with data or appropriate error messages.
        """
        try:
            # Split the path and validate the initial path segment
            path_parts = self.path[1:].split("/")
            if path_parts[0].lower() != "data":
                self.send_error(404)

            # Initialize DataProvider
            data_provider = DataProvider()

            # Initialize query parameters
            query_params = {
                "get_all": False,
                "single_year": "",
                "year_low": "",
                "year_high": ""
            }

            # Determine the type of request and populate query parameters accordingly
            if path_parts[1].lower() == "all":
                query_params["get_all"] = True
            elif self.check_is_number(path_parts[-1]) and not self.check_is_number(path_parts[-2]):
                query_params["single_year"] = path_parts[-1]
            elif self.check_is_number(path_parts[-1]) and self.check_is_number(path_parts[-2]):
                query_params["year_low"] = path_parts[-2]
                query_params["year_high"] = path_parts[-1]
            else:
                self.send_error(400, "Bad Request")

            # Fetch data using DataProvider based on query parameters
            result = data_provider.get_data(query_params)

            # Send HTTP response with data
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(result.encode('utf-8'))

        except ValueError:
            # Handle invalid request data with appropriate error response
            self.send_error(400, "Bad Request")
    
    def check_is_number(self, val):
        """
        Input: val (str): The value to be checked.
        Explanation: Check if the provided value can be converted to a number.
        Output: bool: True if the value can be converted to a number, False otherwise.
        """
        try:
            float(val)
            return True
        except ValueError:
            return False

if __name__ == '__main__':
    PORT = 9000
    socketserver.TCPServer.allow_reuse_address = True
    http = socketserver.TCPServer(('localhost', PORT), ServerHandler)
    print(f'serving on port {PORT}')
    http.serve_forever()