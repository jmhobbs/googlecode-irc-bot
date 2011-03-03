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

from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, task
from twisted.python import log

import shared

def announce ( feed ):
	new = feed.update()
	for entry in new:
		msg = feed.get_message( entry )
		if GoogleCodeIRCBot.instance:
			GoogleCodeIRCBot.instance.trysay( msg.replace( '\n', '' ).encode( 'utf-8' ) )
		else:
			print "No Bot", msg

class GoogleCodeIRCBot ( irc.IRCClient ):

	username = "%s-%s" % ( shared.NAME, shared.VERSION )

	versionName = shared.NAME
	versionNum = shared.VERSION
	sourceURL = shared.SOURCE_URL

	instance = None
	gdata = None
	channel = None
	lineRate = 2
	logger = None
	privmsg_ignore = []

	def connectionMade ( self ):
		irc.IRCClient.connectionMade( self )
		log.msg( self.nickname + ": Connected" )
		if self.logger:
			self.logger.connected()

	def connectionLost( self, reason ):
		irc.IRCClient.connectionLost( self, reason )
		log.msg( self.nickname + ": Connection Lost" )
		if self.logger:
			self.logger.disconnected()

	def signedOn( self ):
		self.join( self.factory.channel )
		log.msg( self.nickname + ": Signed On" )
		GoogleCodeIRCBot.instance = self

	def joined( self, channel ):
		self.channel = self.factory.channel

		log.msg( self.nickname + ": Joined " + self.channel )
		if self.logger:
			self.logger.joined( channel )

		self.lineRate = None
		self.trysay( "Hello, I'm a Google Code IRC Bot, Version %s" % shared.VERSION )
		self.trysay( "More details are available at %s" % shared.SOURCE_URL )
		self.lineRate = 2

	def left( self, channel ):
		log.msg( self.nickname + ": Left Channel " + channel )
		self.channel = None

	def trysay( self, msg ):
		"""
		Attempts to send the given message to the channel.
		"""
		if self.channel:
			try:
				self.say( self.channel, msg )
				log.msg( self.nickname + ": Say : " + msg )
				if self.logger:
					self.logger.message( self.nickname, msg )
				return True
			except e:
				log.msg( self.nickname + ": Error saying : " + e )

	def privmsg ( self, user, channel, msg ):
		user = user.split('!', 1)[0]

		log.msg( self.nickname + ": Private Message : " + user + " says: " + msg )
		if self.logger:
			self.logger.message( user, msg )

		if user in self.privmsg_ignore:
			log.msg( self.nickname + ": Ignoring Private Message From " + user )
			return

		if channel == self.nickname:
				msg = "It isn't nice to whisper!  Play nice with the group."
				self.msg( user, msg )
				return

		if channel == self.channel:
			if msg.startswith( self.nickname + ":" ):
				args = msg.split( ' ')
				if 'OPEN' == args[1]:
					if self.gdata:
						msg = "%s: There are %d open issues." % ( user, self.gdata.get_issue_count() )
					else:
						msg = "Sorry, I have no connection to the issue tracker."
				elif 'HELP' == args[1]:
					msg = "%s: Valid commands are [ OPEN, HELP ]. Please visit %s for more help." % ( user, shared.SOURCE_URL )
				else:
					msg = "%s: Um, what? Try HELP." % user
				self.trysay( msg )

	def action ( self, user, channel, msg ):
		if self.logger:
			self.logger.action( user, msg )

	def irc_NICK ( self, prefix, params ):
		if self.logger:
			old_nick = prefix.split('!')[0]
			new_nick = params[0]
			self.logger.nick_change( old_nick, new_nick )

class GoogleCodeIRCBotFactory( protocol.ReconnectingClientFactory ):

	protocol = GoogleCodeIRCBot

	def __init__( self, channel ):
		self.channel = channel

	def clientConnectionFailed( self, connector, reason ):
		print "connection failed:", reason
		reactor.stop()