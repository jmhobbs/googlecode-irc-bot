# -*- coding: utf-8 -*-

# http://twistedmatrix.com/documents/8.2.0/api/twisted.words.protocols.irc.IRCClient.html
# http://www.eflorenzano.com/blog/post/writing-markov-chain-irc-bot-twisted-and-python/

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, task

import shared
		#def strip_tags(value):
		#return re.sub( r'<[^>]*?>', '', value )

#def announce( feed ):
	#new = feed.update()
	#for entry in new:
		#msg = '%s: %s' % ( strip_tags( entry['title'] ), entry['link'] )
		#if AnnounceBot.instance:
			#AnnounceBot.instance.trysay( msg.replace( '\n', '' ).encode( 'utf-8' ) )
	
class GoogleCodeIRCBot ( irc.IRCClient ):
	
	username = "%s-%s" % ( shared.NAME, shared.VERSION )
	
	versionName = shared.NAME
	versionNum = shared.VERSION
	sourceURL = shared.SOURCE_URL
	
	instance = None
	channel = None
	lineRate = 3

	#def __init__ ( self, project ):
		#irc.IRCClient.__init__( self )
		#self.nickname = project.settings['bot']['name']

	def signedOn( self ):
		self.join( self.factory.channel )
		GoogleCodeIRCBot.instance = self

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

class GoogleCodeIRCBotFactory( protocol.ReconnectingClientFactory ):

	protocol = GoogleCodeIRCBot
	
	def __init__( self, channel ):
		self.channel = channel

	def clientConnectionFailed( self, connector, reason ):
		print "connection failed:", reason
		reactor.stop()