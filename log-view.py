# -*- coding: utf-8 -*-

import web
import os
import sys

urls = (
	"/", "index",
	"/list/(.*)", "list",
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
	def GET ( self, project, date ):
		return render.view()

app.run()