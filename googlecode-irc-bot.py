# -*- coding: utf-8 -*-

# http://github.com/jmhobbs/googlecode-irc-bot

# Copyright (c) 2009 Steven Robertson.
# Copyright (c) 2010 John Hobbs
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 or
# later, as published by the Free Software Foundation.

NAME="Google_Code_IRC_Bot"
VERSION="0.1"

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, task

import feedparser

import re
import sys
import urllib2

class AnnounceBot( irc.IRCClient ):

	username = "%s-%s" % (NAME, VERSION)
	sourceURL = "http://strobe.cc/"

	# I am a terrible person.
	instance = None

	# Intentionally 'None' until we join a channel
	channel = None

	# Prevent flooding
	lineRate = 3

	def signedOn( self ):
		self.join( self.factory.channel )
		AnnounceBot.instance = self

	def joined( self, channel ):
		self.channel = self.factory.channel

	def left( self, channel ):
		self.channel = None

	def trysay( self, msg ):
		"""Attempts to send the given message to the channel."""
		if self.channel:
			try:
				self.say( self.channel, msg )
				return True
			except: pass

class AnnounceBotFactory( protocol.ReconnectingClientFactory ):
	protocol = AnnounceBot
	def __init__( self, channel ):
		self.channel = channel

	def clientConnectionFailed( self, connector, reason ):
		print "connection failed:", reason
		reactor.stop()

class GoogleCodeFeedReader:
	_schema = 'http://code.google.com/feeds/p/%s/updates/basic'

	def __init__( self, project ):
		self.project = project
		self.entries = {}

	def update(self):
		"""Returns list of new items."""
		feed = feedparser.parse( self._schema % self.project )
		added = []
		for entry in feed['entries']:
			if entry['id'] not in self.entries:
				self.entries[entry['id']] = entry
				added.append( entry )
		return added

def strip_tags(value):
	return re.sub( r'<[^>]*?>', '', value )

def announce( feed ):
	new = feed.update()
	for entry in new:
		msg = '%s: %s' % ( strip_tags( entry['title'] ), entry['link'] )
		if AnnounceBot.instance:
			AnnounceBot.instance.trysay( msg.replace( '\n', '' ).encode( 'utf-8' ) )

def run_bot ( settings ):

	AnnounceBot.nickname = settings['project']['bot']['name']
	
	fact = AnnounceBotFactory( settings['project']['bot']['channel'] )
	
	feed = GoogleCodeFeedReader( settings['project']['name'] )
	
	reactor.connectTCP( settings['project']['bot']['server'], settings['project']['bot']['port'], fact )

	feed.update() # No flood on load

	update_task = task.LoopingCall( announce, feed )
	update_task.start( settings['project']['feed']['refresh'], now=False )

	reactor.callLater( 10, announce, feed )
	reactor.run()

if __name__ == '__main__':
	import os, sys
	import yaml
	from time import sleep
	from multiprocessing import Process

	procs = {}

	# Load the bot description files
	for filename in os.listdir( str( sys.path[0] ) + '/bots' ):
		if ".yaml" == filename[-5:]:
			try:
				f = open( str( sys.path[0] ) + '/bots/' + filename )
				settings = yaml.safe_load( f.read() )
				f.close()
				
				# Make sure what we need is there
				if 'project' not in settings.keys():
					raise KeyError( '/project' )
				
				for key in ( 'name', 'bot', 'feed' ):
					if key not in settings['project'].keys():
						raise KeyError( '/project/' + key )

				for key in ( 'name', 'channel', 'server', 'port' ):
					if key not in settings['project']['bot'].keys():
						raise KeyError( '/project/bot/' + key )

				if 'refresh' not in settings['project']['feed'].keys():
					raise KeyError( '/project/feed/refresh' )

				# Now spawn the necessary process
				if settings['project']['name'] not in procs.keys():
					procs[settings['project']['name']] = Process( target=run_bot, args=( settings, ) )
					procs[settings['project']['name']].daemon = True
					procs[settings['project']['name']].start()
					print "Started", settings['project']['name']

			except IOError, e:
				print "Error Opening Bot Description -", filename, " -", e
			except KeyError, e:
				print "Error In Bot Description, Missing Required Key:", e
	
	 # Sleep forever so the children can run
	 # Eventually this should become a load/check/reload cycle
	while True:
		sleep( 999999 )