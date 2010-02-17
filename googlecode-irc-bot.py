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
from gib import ircbot, issues, project, readers, shared
import sys
from time import sleep
from multiprocessing import Process

def run_bot ( project ):
	"""
	Run an ircbot in another process.
	"""
	ircbot.GoogleCodeIRCBot.nickname = project.settings['project']['bot']['name']
	
	factory = ircbot.GoogleCodeIRCBotFactory( project.settings['project']['bot']['channel'] )
	
	issues_feed = None
	downloads_feed = None
	wiki_feed = None
	
	if 0 != project.settings['project']['feeds']['issues']:
		issues_feed = readers.IssueUpdatesReader( project.name )
	
	if 0 != project.settings['project']['feeds']['downloads']:
		downloads_feed = readers.DownloadsReader( project.name )
	
	if 0 != project.settings['project']['feeds']['wiki']:
		wiki_feed = readers.WikiReader( project.name )
	
	reactor.connectTCP( project.settings['project']['bot']['server'], project.settings['project']['bot']['port'], factory )

	if None != issues_feed:
		issues_update_task = task.LoopingCall( ircbot.announce, issues_feed )
		issues_update_task.start( project.settings['project']['feeds']['issues'], now=False )
		reactor.callLater( 20, ircbot.announce, issues_feed )

	if None != downloads_feed:
		downloads_update_task = task.LoopingCall( ircbot.announce, downloads_feed )
		downloads_update_task.start( project.settings['project']['feeds']['downloads'], now=False )
		reactor.callLater( 20, ircbot.announce, downloads_feed )

	if None != wiki_feed:
		wiki_update_task = task.LoopingCall( ircbot.announce, wiki_feed )
		wiki_update_task.start( project.settings['project']['feeds']['wiki'], now=False )
		reactor.callLater( 20, ircbot.announce, wiki_feed )

	reactor.run()

bot_processes = {}

bots = project.Project.load_all_from_path( sys.path[0] + "/bots/" )

for bot in bots:
	if bot.name not in bot_processes.keys():
		bot_processes[bot.name] = Process( target=run_bot, args=( bot, ) )
		bot_processes[bot.name].daemon = True
		bot_processes[bot.name].start()
		print "Started", bot.name

while True:
	try:
		sleep( 60 ) # TODO: Make configurable
		for key, process in bot_processes.items():
			if not process.is_alive():
				print "Bot", key, "has died!"
	except KeyboardInterrupt, e:
		print "Shutting Down"
		exit()
	except Exception, e:
		print "Error:", e