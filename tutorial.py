# The webapp2 framework
import webapp2

# The JSON library
import json

# Our JSON handler class
class JsonPage(webapp2.RequestHandler):
    # The POST handler
    def post(self):
        # Our POST Input
        txtinput = self.request.get('txtValue')
        
        # Create an array
        array = {'text': txtinput}
        
        # Output the JSON
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(array))

# URL map the JSON function
app = webapp2.WSGIApplication([('/tutorial', JsonPage)], debug=True)