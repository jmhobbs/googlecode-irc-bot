# -*- coding: utf-8 -*-

import os, sys
import yaml

class Project:

	settings = None
	name = ''

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
			
			for key in ( 'name', 'bot', 'feed' ):
				if key not in self.settings['project'].keys():
					raise KeyError( '/project/' + key )

			for key in ( 'name', 'channel', 'server', 'port' ):
				if key not in self.settings['project']['bot'].keys():
					raise KeyError( '/project/bot/' + key )

			if 'refresh' not in self.settings['project']['feed'].keys():
				raise KeyError( '/project/feed/refresh' )

			self.name = self.settings['project']['name']

		except IOError, e:
			raise Exception ( "Error Opening Bot Description - " + path + " : " + str( e ) )
		except KeyError, e:
			raise Exception ( "Error In Bot Description, Missing Required Key: " + str( e ) )
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
					continue
		return projects