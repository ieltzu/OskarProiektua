
import webapp2
from webapp2_extras import sessions
import os


#from webapp2_extras import sessions

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'some-secret-key',
}
class BaseHandler(webapp2.RequestHandler):

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()



class MainHandler(BaseHandler):
    def get(self):
        f = open('index.html')
        self.response.write(f.read())






app = webapp2.WSGIApplication([
    ("/", MainHandler),
],config=config, debug=True)
