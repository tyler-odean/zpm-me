import logging

import os
import webapp2

import jinja2
JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates/')))


class Templater(webapp2.RequestHandler):

  def get(self):

    ########## REDIRECTS ###########

    # ignore everything past the .
    templatePath = self.request.path.split('.')[0]

    # hard redirects actually refresh the page
    hardRedirects = {
      '/r': 'https://docs.google.com/document/d/1UB7mlQreqOiqDCILi_fsd2yi9WviFDcCQDJSTojlt6I/edit',
    }
    if templatePath in hardRedirects:
      self.redirect(hardRedirects[templatePath])
      return

    # soft redirects leave the url intact and load a template different than the name
    softRedirects = {
      '/': '/index',
    }
    if templatePath in softRedirects:
      templatePath = softRedirects[templatePath]

    ########## TEMPLATING ###########

    if templatePath == '/index':
      pageTitle = 'zpm.me'      
      pageUrl = 'http://www.zpm.me/'
    else:
      pageTitle = templatePath[1:] + ' - zpm.me'
      pageUrl = 'http://www.zpm.me' + templatePath

    try:
      template = JINJA_ENVIRONMENT.get_template(templatePath + '.html')
      finalHtml = template.render({
        'pageUrl': pageUrl,
        'pageTitle': pageTitle,
      })
    except jinja2.TemplateNotFound as e:
      self.redirect('/')
      return

    self.response.out.write(finalHtml)


## redirect the app to this to override the entire site
#class SOPA(webapp.RequestHandler):
#
#  def get(self):
#
#    content = open(os.path.join(os.path.dirname(__file__), 'content/sopa.html'), 'r')
#    self.response.out.write(content.read())


################################################################################


app = webapp2.WSGIApplication([
  ('/.*', Templater),
], debug=True)

