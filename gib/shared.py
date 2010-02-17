# -*- coding: utf-8 -*-

import sys
import re

NAME="Google_Code_IRC_Bot"
VERSION="0.2"
SOURCE_URL="http://github.com/jmhobbs/googlecode-irc-bot"

SHELF=sys.path[0] + "/shelf/"

def strip_tags ( value ):
	return re.sub( r'<[^>]*?>', '', value )