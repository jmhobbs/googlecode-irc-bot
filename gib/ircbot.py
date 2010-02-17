# -*- coding: utf-8 -*-

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, task

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