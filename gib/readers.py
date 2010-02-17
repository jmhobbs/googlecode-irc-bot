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

import feedparser
import shelve
import shared

class GoogleFeedReader:

	_schema = ''
	_name = 'base'
	
	def __init__( self, project ):
		self.project = project
		self.shelf = shelve.open( shared.SHELF + project + '.shelf' )
		try:
			if dict != type( self.shelf[self._name] ):
				raise KeyError ( 'not a dict' )
		except KeyError, e:
			self.shelf[self._name] = {}
		
		self.last_id = self.read( 'last_id' )
		
		# Prevent first run spamming
		if None == self.read( 'first_run' ):
			self.update()
			self.write( 'first_run', False )
	
	def __del__ ( self ):
		self.write( 'last_id', self.last_id )
		self.shelf.close()

	def read ( self, key ):
		"""
		Get a value for a key from the shelf data store.
		"""
		if self.shelf[self._name].has_key( key ):
			return self.shelf[self._name][key]
		else:
			return None
	
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

	def get_message ( self, entry ):
		return '%s: %s' % ( shared.strip_tags( entry['title'] ), entry['link'] )

class IssueUpdatesReader ( GoogleFeedReader ):

	_schema = 'http://code.google.com/feeds/p/%s/issueupdates/basic'
	_name = 'issues'
	
	def __init__( self, project ):
		GoogleFeedReader.__init__( self, project )
		
	def get_message ( self, entry ):
		return '[Issues] %s: %s' % ( shared.strip_tags( entry['title'] ), entry['link'] )

class DownloadsReader ( GoogleFeedReader ):

	_schema = 'http://code.google.com/feeds/p/%s/downloads/basic'
	_name = 'downloads'

	def __init__( self, project ):
		GoogleFeedReader.__init__( self, project )

	def get_message ( self, entry ):
		return '[Downloads] %s: %s' % ( shared.strip_tags( entry['title'] ), entry['link'] )

class WikiReader ( GoogleFeedReader ):

	_schema = 'http://code.google.com/feeds/p/%s/svnchanges/basic?path=/wiki/'
	_name = 'wiki'

	def __init__( self, project ):
		GoogleFeedReader.__init__( self, project )

	def get_message ( self, entry ):
		return '[Wiki] %s: %s' % ( shared.strip_tags( entry['title'] ), entry['link'] )