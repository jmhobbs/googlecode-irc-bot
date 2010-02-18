# -*- coding: utf-8 -*-

import web
import os
import sys
import re

urls = (
	"/", "index",
	"/list/(.*)", "list",
	"/view/(.*)/(.*)/([0-9]*)", "view",
	"/view/(.*)/(.*)", "view"
)

web.config.debug = False

app = web.application( urls, locals() )
render = web.template.render( 'views/', base='layout' )

LOG_PATH = sys.path[0] + "/irc-logs/"

class index:
	def GET ( self ):
		projects = []
		for filename in os.listdir( LOG_PATH ):
			if ".log" == filename[-4:]:
				if filename[:-15] not in projects:
					projects.append( filename[:-15] )
		return render.index( sorted( projects ) )

class list:
	def GET ( self, project ):
		log_files = []
		for filename in os.listdir( LOG_PATH ):
			if ".log" == filename[-4:]:
				if project == filename[:len(project)]:
					if filename[-14:-4] not in log_files:
						log_files.append( filename[-14:-4] )
		return render.list( project, sorted( log_files ) )

class view:
	def GET ( self, project, date, page = 0 ):
		if page == '':
			page = 0
		lines = None
		path = "%s%s_%s.log" % ( LOG_PATH, project, date )
		if os.path.exists( path ):
			handle = open( path, 'r' )
			lines = handle.readlines( 1250 ) # Read the first 125k
			handle.close()
		markup_log_lines( lines )
		return render.view( lines, project, date, page )

def markup_log_lines ( lines ):
	# Hooray for mutable types!
	counter = 0
	users = []
	for line in lines:
		# We wont' be escaping it in the template!
		line = web.net.websafe( line )

		timestamp = line[:10]
		message = line[11:-1]

		# Look for distinct users, then add a class to them as needed
		user = re.match('&lt;(.*?)&gt; ', message )
		if None != user:
			user_number = 0
			user = user.group()[4:-5]
			i = 0
			found = False
			for u in users:
				if u == user:
					found = True
					break
				i = i + 1
			if not found:
				users.append( user )

			user_number = i
			i = len( user ) + 9
			message = '&lt;<span class="user user-' + str( user_number ) + '">' + user + '</span>&gt; ' + message[i:]

		line = '<div class="time">' + timestamp + '</div><div class="message">' + message + '</div>'
		lines[counter] = line
		counter = counter + 1;

app.run()