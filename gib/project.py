# -*- coding: utf-8 -*-

# Copyright (c) 2010 John Hobbs
#
# http://github.com/jmhobbs/googlecode-irc-bot
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os, sys
import yaml

class Project:

	settings = None
	name = ''
	vcs = ''

	def __init__ ( self, path ):
		"""
		Attempt to load the project settings from a given file.
		"""
		try:
			f = open( path )
			self.settings = yaml.safe_load( f.read() )
			f.close()

			# Make sure what we need is there
			if 'project' not in self.settings.keys():
				raise KeyError( '/project' )

			for key in ( 'name', 'bot', 'feeds', 'issues', 'logging', 'privignore', 'vcs' ):
				if key not in self.settings['project'].keys():
					raise KeyError( '/project/' + key )

			for key in ( 'name', 'channel', 'server', 'port' ):
				if key not in self.settings['project']['bot'].keys():
					raise KeyError( '/project/bot/' + key )

			for key in ( 'issues', 'downloads', 'wiki' ):
				if key not in self.settings['project']['feeds'].keys():
					raise KeyError( '/project/feeds/' + key )

			for key in ( 'username', 'password' ):
				if key not in self.settings['project']['issues'].keys():
					raise KeyError( '/project/issues/' + key )
            
			self.name = self.settings['project']['name']
			self.vcs = self.settings['project']['vcs']

		except IOError, e:
			raise Exception ( "Error Opening Bot Description - " + path + " : " + str( e ) )
		except KeyError, e:
			raise Exception ( "Error In Bot Description - " + path + " - Missing Required Key: " + str( e ) )
		return

	@staticmethod
	def load_all_from_path ( path ):
		"""
		Search for and load all of the project files on the given path.
		"""
		projects = []
		for filename in os.listdir( path ):
			if ".yaml" == filename[-5:]:
				try:
					project = Project( path + filename )
					projects.append( project )
				except Exception, e:
					print e
		return projects
