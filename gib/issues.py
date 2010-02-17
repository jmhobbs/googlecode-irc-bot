# -*- coding: utf-8 -*-

import gdata.projecthosting.client
import gdata.projecthosting.data
import gdata.client
import gdata.data
import atom.http_core
import atom.core

# http://code.google.com/p/support/wiki/IssueTrackerAPIPython

class GoogleIssueTracker:
	def __init__ ( self, username, password, project ):
		self.project = project
		self.client = gdata.projecthosting.client.ProjectHostingClient()
		if False == self.client.client_login( username, password, source='Google_Code_IRC_Bot', service='code' ):
			raise Exception( 'Could not log in to Google Issue Tracker. Bad Credentials.' )
	
	def get_all_issues ( self ):
		"""
		Retrieve all the issues in a project.
		"""
		feed = self.client.get_issues( self.project )
		issues = []
		for issue in feed.entry:
			issues.append( issue )
	
	def get_issue_count ( self ):
		"""
		Get a count of all the open issues.
		"""
		return len( self.get_all_issues() )
	
	#def retrieving_issues_using_query_parameters(self, client, project_name):
		#"""Retrieve a set of issues in a project."""
		#query = gdata.projecthosting.client.Query(label='label0')
		#feed = client.get_issues(project_name, query=query)
		#for issue in feed.entry:
			#print issue.title.text
		#return feed
		
	#def retrieving_issues_comments_for_an_issue(self, client, project_name,
																							#issue_id):
		#"""Retrieve all issue comments for an issue."""
		#comments_feed = client.get_comments(project_name, issue_id)
		#for comment in comments_feed.entry:
			#print comment.content
		#return comments_feed
		
	#def creating_issues(self, client, project_name, owner):
		#"""Create an issue."""
		#return client.add_issue(
				#project_name,
				#'my title',
				#'my summary',
				#owner,
				#labels=['label0'])

	#def modifying_an_issue_or_creating_issue_comments(self, client, project_name,
																										#issue_id, owner, assignee):
		#"""Add a comment and update metadata in an issue."""
		#return client.update_issue(
				#project_name,
				#issue_id,
				#owner,
				#comment='My comment here.',
				#summary='New Summary',
				#status='Accepted',
				#owner=assignee,
				#labels=['-label0', 'label1'],
				#ccs=[owner])