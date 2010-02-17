# -*- coding: utf-8 -*-

# http://github.com/jmhobbs/googlecode-irc-bot

# Copyright (c) 2009 Steven Robertson.
# Copyright (c) 2010 John Hobbs
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 or
# later, as published by the Free Software Foundation.

from twisted.internet import reactor, task
from gib import ircbot, issues, project, readers, shared

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

	# Now spawn the necessary process
	#if settings['project']['name'] not in procs.keys():
		#procs[settings['project']['name']] = Process( target=run_bot, args=( settings, ) )
		#procs[settings['project']['name']].daemon = True
		#procs[settings['project']['name']].start()
		#print "Started", settings['project']['name']
	
		#def strip_tags(value):
		#return re.sub( r'<[^>]*?>', '', value )

#def announce( feed ):
	#new = feed.update()
	#for entry in new:
		#msg = '%s: %s' % ( strip_tags( entry['title'] ), entry['link'] )
		#if AnnounceBot.instance:
			#AnnounceBot.instance.trysay( msg.replace( '\n', '' ).encode( 'utf-8' ) )
	
	 # Sleep forever so the children can run
	 # Eventually this should become a load/check/reload cycle
	while True:
		sleep( 999999 )