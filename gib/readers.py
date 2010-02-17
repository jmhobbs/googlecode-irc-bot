# -*- coding: utf-8 -*-

import feedparser
import shelve
import shared

class GoogleFeedReader:

	_schema = ''
	_name = 'base'
	
	def __init__( self, project ):
		self.project = project
		self.last_id = 0
		self.shelf = shelve.open( shared.SHELF + project + '.shelf' )
		try:
			if dict != type( self.shelf[self._name] ):
				raise KeyError ( 'not a dict' )
		except KeyError, e:
			self.shelf[self._name] = {}
	
	def __del__ ( self ):
		self.shelf.close()

	def read ( self, key ):
		"""
		Get a value for a key from the shelf data store.
		"""
		return self.shelf[self._name][key]
	
	def write ( self, key, value ):
		"""
		Write a key/value pair to the shelf data store.
		"""
		self.shelf[self._name][key] = value

	def update ( self ):
		"""Returns list of new items."""
		# TODO: ETag & Last-Modified
		feed = feedparser.parse( self._schema % self.project )
		return self.parse( feed )

	def parse ( self, feed ):
		"""
		Parses the content returned from update()
		"""
		added = []
		for entry in feed['entries']:
			if entry['id'] == self.last_id:
				break
			added.append( entry )
		self.last_id = feed['entries'][0]['id']
		return added

class IssueUpdatesReader ( GoogleFeedReader ):

	_schema = 'http://code.google.com/feeds/p/%s/issueupdates/basic'
	_name = 'issues'
	
	def __init__( self, project ):
		GoogleFeedReader.__init__( self, project )

class DownloadsReader ( GoogleFeedReader ):

	_schema = 'http://code.google.com/feeds/p/%s/downloads/basic'
	_name = 'downloads'

	def __init__( self, project ):
		GoogleFeedReader.__init__( self, project )

class WikiReader ( GoogleFeedReader ):

	_schema = 'http://code.google.com/feeds/p/%s/svnchanges/basic?path=/wiki/'
	_name = 'wiki'

	def __init__( self, project ):
		GoogleFeedReader.__init__( self, project )