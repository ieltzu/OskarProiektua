
import webapp2
from webapp2_extras import sessions
import os
import jinja2
import urllib
import httplib2
import httplib
import hmac
import random
import time
import urlparse
import binascii
import hashlib


#from webapp2_extras import sessions

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

JINJA_ENVIROMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True
)

app_id = "upvweather"

consumer_key='IgmyMb1s1BvV2FaGUJJKWXmnE'
consumer_secret='QaF3mMpXhlInjIqs5kHBKn70JRvtdOvpb1LoegqenB2GHSiAYc'

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'some-secret-key',
}

class TwitterLogin(BaseHandler):
    def get(self):
            url="https://api.twitter.com/oauth/request_token"
            metodoa = "POST"

            callback_url ='https://upvweather.appspot.com/twitter_callback'
            oauth_parametroak = {'oauth_callback':callback_url}

            helper = createAuthHeader(metodoa, url, oauth_parametroak, "" , None)

            goiburuak={'Authorization':helper}

            #Lehenengo Post bidalketa
            http = httplib2.Http()
            response , body = http.request(url,method=metodoa,body=None,headers=goiburuak)

            datuak = dict(urlparse.parse_qsl(body))
            if datuak['oauth_callback_confirmed']=='true':
                berbideraketa_url="https://api.twitter.com/oauth/authenticate"
                self.session['oauth_token'] = datuak['oauth_token']
                self.redirect(berbideraketa_url+'?'+'oauth_token='+datuak['oauth_token'])
            else:
                self.response.write('Error')
            #berbideraketa_url="https://api.twitter.com/oauth/authenticate"
            #self.redirect(berbideraketa_url+'?'+'oauth_token='+datuak['oauth_token'])

class OAuthCallback(BaseHandler):
    def get(self):
            oauth_token=self.session['oauth_token']

            if (self.session['oauth_token'] == oauth_token):

                oauth_verifier=self.request.get("oauth_verifier")
                url="https://api.twitter.com/oauth/access_token"
                metodoa = "POST"

                oauth_parametroak = {'oauth_token':oauth_token}
                helper = createAuthHeader(metodoa, url, oauth_parametroak, "" , None)

                goiburuak={}
                goiburuak['Authorization'] = helper
                goiburuak['Content-Type'] = 'application/x-www-form-urlencoded'
                goiburuak['Content-Length'] = str(len("oauth_verifier="+oauth_verifier))

                http = httplib2.Http()
                response , body = http.request(url,method=metodoa,headers=goiburuak,body="oauth_verifier="+oauth_verifier)

                self.response.write('//')
                self.response.write(response.status)
                self.response.write('//')


                datuak = dict(urlparse.parse_qsl(body))
                oauth_token = datuak['oauth_token']
                oauth_token_secret=datuak['oauth_token_secret']

                self.session['oauth_token']=oauth_token
                self.session['oauth_token_secret']=oauth_token_secret
                self.session['screen_name']=datuak['screen_name']

                self.redirect('https://upvweather.appspot.com/')

            else:
                self.response.write('Error:')
                self.response.write(self.session['oauth_token'])

class SendATweet(BaseHandler):
    def get(self):
        status=self.request.get("Tweet")
        status=urllib.unquote(status)
        oauth_token=self.session['oauth_token']
        oauth_token_secret=self.session['oauth_token_secret']
        url='https://api.twitter.com/1.1/statuses/update.json'
        goiburuak={'status':status,}
        oauth_parametroak={'oauth_token':oauth_token,}
        metodoa = 'POST'
        goiburuak['Authorization']= createAuthHeader(metodoa, url, oauth_parametroak, goiburuak , oauth_token_secret)
        http = httplib2.Http()
        response , body = http.request(url+'?status='+urllib.quote(status,''),method=metodoa,headers=goiburuak,body=None)

class MainHandler(BaseHandler):
    def get(self):
        f = open('index.html')
        self.response.write(f.read())

def createAuthHeader(method, base_url, oauth_header, http_params, oauth_token_secret):
    oauth_header.update({ 'oauth_consumer_key': consumer_key,
                      'oauth_nonce': str(random.randint(0, 999999999)),
                      'oauth_signature_method': "HMAC-SHA1",
                      'oauth_timestamp': str(int(time.time())),
                      'oauth_version': "1.0"})
    oauth_header['oauth_signature'] = urllib.quote(createRequestSignature(method, base_url, oauth_header, http_params, oauth_token_secret), "")

    if oauth_header.has_key('oauth_callback'):
        oauth_header['oauth_callback'] = urllib.quote_plus(oauth_header['oauth_callback'])
    authorization_header = "OAuth "
    for each in sorted(oauth_header.keys()):
        if each == sorted(oauth_header.keys())[-1]:
            authorization_header = authorization_header \
                                 + each + "=" + "\"" \
                                 + oauth_header[each] + "\""
        else:
            authorization_header = authorization_header \
                                 + each + "=" + "\"" \
                                 + oauth_header[each] + "\"" + ", "

    return authorization_header


def createRequestSignature(method, base_url, oauth_header, http_params, oauth_token_secret):
    encoded_params = ''
    params = {}
    params.update(oauth_header)
    if http_params:
        params.update(http_params)
    for each in sorted(params.keys()):
        key = urllib.quote(each, "")
        value = urllib.quote(params[each], "")
        if each == sorted(params.keys())[-1]:
            encoded_params = encoded_params + key + "=" + value
        else:
            encoded_params = encoded_params + key + "=" + value + "&"

    signature_base = method.upper() + \
                   "&" + urllib.quote(base_url, "") + \
                   "&" + urllib.quote(encoded_params, "")
    #print signature_base
    signing_key = ''
    if oauth_token_secret == None:
        signing_key = urllib.quote(consumer_secret, "") + "&"
    else:
        signing_key = urllib.quote(consumer_secret, "") + "&" + urllib.quote(oauth_token_secret, "")

    hashed = hmac.new(signing_key, signature_base, hashlib.sha1)
    oauth_signature = binascii.b2a_base64(hashed.digest())

    return oauth_signature[:-1]






app = webapp2.WSGIApplication([
    ("/", MainHandler),
    ('/twitter_callback', OAuthCallback),
    ('/TwitterLogin',TwitterLogin),
    ('/SendATweet',SendATweet),
],config=config, debug=True)
