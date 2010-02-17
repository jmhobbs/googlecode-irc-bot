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

import time

class IRCLogger:
	def __init__ ( self, path, prefix ):
		self.path = path
		self.prefix = prefix
		self.date = time.strftime( "%Y-%m-%d", time.localtime( time.time() ) )
		self.file = open( self.get_log_file_path(), "a" )

	def get_log_file_path ( self ):
		return self.path + self.prefix + "_" + self.date + ".log"

	def log ( self, message ):
		if self.date != time.strftime( "%Y-%m-%d", time.localtime( time.time() ) ):
			self.file.close()
			self.date = time.strftime( "%Y-%m-%d", time.localtime( time.time() ) )
			self.file = open( self.get_log_file_path(), "a" )
			self.log( '[log file rotation]' )
		self.file.write( '%s %s\n' % ( time.strftime( "[%H:%M:%S]", time.localtime( time.time() ) ), message ) )
		self.file.flush()

	def close ( self ):
		self.file.close()
		
	def connected ( self ):
		self.log( "[connected]" )
	
	def disconnected ( self, reason ):
		self.log( "[disconnected - %s]" % reason )

	def joined ( self, channel ):
		self.log( "[joined %s]" % channel )
	
	def message ( self, user, message ):
		self.log( "<%s> %s" % ( user, message ) )
	
	def action ( self, user, message ):
		self.log( "* %s %s" % ( user, message ) )
		
	def nick_change ( self, old_nick, new_nick ):
		self.log( "%s is now known as %s" % ( old_nick, new_nick ) )
