# -*- coding: utf-8 -*-

# http://github.com/jmhobbs/googlecode-irc-bot

# Copyright (c) 2009 Steven Robertson.
# Copyright (c) 2010 John Hobbs
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 or
# later, as published by the Free Software Foundation.

if __name__ != '__main__':
	print "This can only be run as a main entry point."
	exit()

from twisted.internet import reactor, task
from gib import issues, project, readers, shared
import sys
from time import sleep
from multiprocessing import Process

def run_bot ( project ):
	print "Run Bot:", project.name
	#AnnounceBot.nickname = settings['project']['bot']['name']
	
	#fact = AnnounceBotFactory( settings['project']['bot']['channel'] )
	
	#feed = GoogleCodeFeedReader( settings['project']['name'] )
	
	#reactor.connectTCP( settings['project']['bot']['server'], settings['project']['bot']['port'], fact )

	#feed.update() # No flood on load

	#update_task = task.LoopingCall( announce, feed )
	#update_task.start( settings['project']['feed']['refresh'], now=False )

	#reactor.callLater( 10, announce, feed )
	#reactor.run()

bot_processes = {}

bots = project.Project.load_all_from_path( sys.path[0] + "/bots/" )

# Now spawn the necessary process
for bot in bots:
	if bot.name not in bot_processes.keys():
		bot_processes[bot.name] = Process( target=run_bot, args=( bot, ) )
		bot_processes[bot.name].daemon = True
		bot_processes[bot.name].start()
		print "Started", bot.name