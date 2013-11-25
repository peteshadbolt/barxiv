import re
import webapp2
import json, time, logging, os
import jinja2

# Set up the templating engine
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class MainPage(webapp2.RequestHandler):
    def get(self):
        ''' Build the page and send it over '''
        # Construct a string detailing the access token state
        #access_token_state=database.check_token(self.request.get('accessToken').strip())

        # Template the page and send it back to the user
        template = JINJA_ENVIRONMENT.get_template('index.html')
        #template_values={'access_token_message': access_token_state['message']}
        template_values={}
        self.response.out.write(template.render(template_values))

class GetChipPage(webapp2.RequestHandler):
    def get(self):
        ''' User asked for a chip '''
        chip = self.request.get('chipName')
        chip_json = chip_library.chip_data[chip]
        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write(json.dumps(chip_json))

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/chip', GetChipPage),
], debug=False)

