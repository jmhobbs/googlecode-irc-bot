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

# Gracious credit goes to Steven Robertson, whose Quodlibot provided inspiration and foundation
# http://strobe.cc/quodlibot/


from twisted.internet import reactor, task
from gib import ircbot, issues, project, readers, shared, logger
import sys
from time import sleep
from multiprocessing import Process
from twisted.python import log

def run_bot ( project ):
	"""
	Run an ircbot in another process.
	"""
	ircbot.GoogleCodeIRCBot.nickname = project.settings['project']['bot']['name']

	if project.settings['project']['issues']['username'] != '' and project.settings['project']['issues']['password'] != '':
		try:
			ircbot.GoogleCodeIRCBot.gdata = issues.GoogleIssueTracker( project.settings['project']['issues']['username'], project.settings['project']['issues']['password'], project.name )
		except:
			ircbot.GoogleCodeIRCBot.gdata = None

	ircbot.GoogleCodeIRCBot.privmsg_ignore = project.settings['project']['privignore']

	if project.settings['project']['logging']:
		ircbot.GoogleCodeIRCBot.logger = logger.IRCLogger( shared.IRC_LOGS, project.name )

	factory = ircbot.GoogleCodeIRCBotFactory( project.settings['project']['bot']['channel'] )

	issues_feed = None
	downloads_feed = None
	wiki_feed = None
	code_feed = None

	if 0 != project.settings['project']['feeds']['issues']:
		issues_feed = readers.IssueUpdatesReader( project.name )

	if 0 != project.settings['project']['feeds']['downloads']:
		downloads_feed = readers.DownloadsReader( project.name )

	if 0 != project.settings['project']['feeds']['wiki']:
		wiki_feed = readers.WikiReader( project.name, project.vcs )
        
	if 0 != project.settings['project']['feeds']['code']:
		code_feed = readers.CodeUpdatesReader( project.name, project.vcs )

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

	if None != code_feed:
		code_update_task = task.LoopingCall( ircbot.announce, code_feed )
		code_update_task.start( project.settings['project']['feeds']['code'], now=False )
		reactor.callLater( 20, ircbot.announce, code_feed )

	reactor.run()


def main ():

	bot_processes = {}
	bots = project.Project.load_all_from_path( sys.path[0] + "/bots/" )

	if len(sys.argv) > 1 and sys.argv[1] == "-debug":
		log.startLogging(sys.stdout)

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

if __name__ != '__main__':
	print "This can only be run as a main entry point."
	exit()
else:
	main()
