## Purpose

To create an IRC bot that will publish Google Code changes to an IRC channel. Eventually we want to support queries and actions as well.

Additionally there is a log view web server included, log-view.py.  You can see an example of this server at <http://irclogs.velvetcache.org>

## Roadmap

  * Basic feed based IRC bot - **DONE**
  * Multiple project support with YAML & Multiprocessing - **DONE**
  * Daemon monitoring, auditing & dynamic loading. - __STARTED__
  * IRC logging - **DONE**
  * Query interaction. - __STARTED__

## Requirements

  * [Python >= 2.4](http://python.org/)
  * [Twisted](http://twistedmatrix.com/trac/)
  * [Feedparser](http://www.feedparser.org/)
  * [PyYAML](http://pyyaml.org/)
  * [GData >= 2.0.4](http://code.google.com/p/gdata-python-client/)
  * Intestinal Fortitude (if you are going to read the code)

  If you are going to use the log viewer you'll also need:

  * [Python >= 2.4](http://python.org/)
  * [web.py](http://www.webpy.org/)

## Usage

  * Create a bot yaml file in ./bots/
  * Run googlecode-irc-bot.py
  * Enjoy your bot
  * To view IRC logs, run log-view.py and visit http://localhost:8080/

### Configuration

	project:
	  name: 'example' // Name of your bot, used internally
	  bot:
	    name: 'example-gc-bot'       // The IRC handle of your bot
	    channel: '#example'          // The IRC channel to join
	    server: 'chat.freenode.net'  // The IRC server
	    port: 6667                   // The IRC port
	  feeds:
	    issues: 600      // Refresh issues feed interval (in seconds)
	    downloads: 600   // Refresh downloads feed interval (in seconds)
	    wiki: 600        // Refresh wiki changes feed interval (in seconds)
	  issues:
	    username: example@gmail.com  // Google login for access to issues API
	    password: example
	  logging: True   // Log all interactions on the channel to a file
	  privignore:  // All users in this list will be ignored by the bot
	  - ChanServ   // ChanServ can get into a loop if it asks your bot something
	  - NickServ
	  - jmhobbs    // Nobody listens to me anyway...
	  vcs: svn   // svn, hg, git...

### Debugging

Having problems?  You can tail the log, or you can pass -debug to the script to add stdout logging of the Twisted framework.

    $ python googlecode-irc-bot.py -debug

## Credits

Inspiration and foundations from Quodlibot by Steven Robertson - [http://strobe.cc/quodlibot/](http://strobe.cc/quodlibot/)

ChanServ loop bug identified by daenney - [https://github.com/daenney](https://github.com/daenney)

VCS options and code feed reader by daenney - [https://github.com/daenney](https://github.com/daenney)

## License

Copyright (c) 2010 John Hobbs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
