#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi

form='''
<head>
	<title>Unit 2 Signup</title>
	<style type = "text/css">
		.label {text-align: right}
		.error {color: red}
		</style>
	</head>
<body>
	<h2>Signup</h2>
	<form method="post">
		<table>
			<tbody>
				<tr>
					<td class="label">
						Username
						</td>
					<td>
						<input type="text" name="username" value="%(username)s">
						</td>
					<td class="error">
						%(error_username)s
						</td>
					</tr>
				<tr>
					<td class="label">
						Password
						</td>
					<td>
						<input type="password" name="password" value="">
						</td>
					<td class="error">
						%(error_password)s
						</td>
					</tr>
				<tr>
					<td class="label">
						Verify Password
						</td>
					<td>
						<input type="password" name="verify" value="">
						</td>
					<td class="error">
						%(error_verify)s
						</td>
					</tr>
				<tr>
					<td class="label">
						Email (optional)
						</td>
					<td>
						<input type="text" name="email" value="%(email)s">
						</td>
					<td class="error">
						%(error_email)s
						</td>
					</tr>
				</tbody>
			</table>
		<input type="submit">
		</form>
	</body>
'''

form2='''
<head>
	<title>Unit2 Signup</title>
	</head>
<body>
	<h2>Welcome %(username)s!</h2>
	</body>
'''

class MainHandler(webapp2.RequestHandler):
	def write_form(self, error_username='', error_password='', error_verify='', error_email='',
					username='', email=''):
		self.response.out.write(form % {'error_username' : error_username,
										'error_password' : error_password,
										'error_verify'   : error_verify,
										'error_email'    : error_email,
										'username'       : escape_html(username),
										'email'          : escape_html(email)})

	def get(self):
		self.write_form()
	
	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')
		
		error_list = [valid_username(username),
					  valid_password(password),
					  password == verify,
					  valid_email(email)]
					  
		if	error_list[0] == None:
			self.write_form("That's not a valid username.", "", "", "", username, email)
		elif error_list[1] == None:
			self.write_form("", "That wasn't a valid password.", "", "", username, email)
		elif error_list[2] == False:
			self.write_form("", "", "Your passwords didn't match.", "", username, email)
		elif error_list[3] == False:
			self.write_form("", "", "", "That's not a valid email.", username, email)
		else:
			self.redirect('/welcome?username=' + username)
			
class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		username = self.request.get('username')
		self.response.out.write(form2 % {'username' : username})

USER_RE = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
PASS_RE = re.compile(r'^.{3,20}$')
MAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

def valid_username(username):
	return USER_RE.match(username)

def valid_password(password):
	return PASS_RE.match(password)
	
def valid_email(email):
	return (MAIL_RE.match(email) or (email==''))
		
def escape_html(s):
	return cgi.escape(s, quote=True)		

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/welcome', WelcomeHandler)
	], debug=True)
