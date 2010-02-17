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
	channel = None
	lineRate = 2

	def signedOn( self ):
		self.join( self.factory.channel )
		GoogleCodeIRCBot.instance = self

	def joined( self, channel ):
		self.channel = self.factory.channel
		self.lineRate = None
		self.trysay( "Hello, I'm a Google Code IRC Bot, Version %s" % shared.VERSION )
		self.trysay( "More details are available at %s" % shared.SOURCE_URL )
		self.lineRate = 2

	def left( self, channel ):
		self.channel = None

	def trysay( self, msg ):
		"""
		Attempts to send the given message to the channel.
		"""
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