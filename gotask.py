#! /usr/bin/env python
# -*- coding:utf-8 -*-

import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

class GoTask:

    def __init__(self):
        
        FLAGS = gflags.FLAGS

        # Set up a Flow object to be used if we need to authenticate. This
        # sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
        # the information it needs to authenticate. Note that it is called
        # the Web Server Flow, but it can also handle the flow for native
        # applications
        # The client_id and client_secret are copied from the API Access tab on
        # the Google APIs Console
        FLOW = OAuth2WebServerFlow(
        client_id='350392034727-p663o1j04sepb3ik4sp67u384o1jjee6.apps.googleusercontent.com',
        client_secret='o8V6_dLLJ-S5QKKxidE_Z0Yg',
        scope='https://www.googleapis.com/auth/tasks',
        user_agent='google-task-ui/v1')

        # To disable the local server feature, uncomment the following line:
        FLAGS.auth_local_webserver = False

        # If the Credentials don't exist or are invalid, run through the native client
        # flow. The Storage object will ensure that if successful the good
        # Credentials will get written back to a file.
        storage = Storage('tasks.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid == True:
            credentials = run(FLOW, storage)

        # Create an httplib2.Http object to handle our HTTP requests and authorize it
        # with our good Credentials.
        http = httplib2.Http()
        http = credentials.authorize(http)

        # Build a service object for interacting with the API. Visit
        # the Google APIs Console
        # to get a developerKey for your own application.
        self.service = build(serviceName='tasks', version='v1', 
                        http=http, developerKey='AIzaSyAwrNJT65OhdkwuxWEdh-ZUPP3kkPOk804')

    def list_tasklists(self):
        """List an user's all tasklists

        """
        response = self.service.tasklists().list().execute()
        return response['items']

    def rename_tasklist(self, tasklist, new_name):
        """Rename the specified tasklist

        """
        tasklist['title'] = new_name
        result = self.service.tasklists().update(tasklist=tasklist['id'], body=tasklist).execute()
        if result['title'] == new_name:
            return True
        else:
            return False

    def del_tasklist(self, tasklist_id):
        """Delete the specified tasklist

        """
        self.service.tasklists().delete(tasklist=tasklist_id).execute()
    
    def new_tasklist(self, tasklist_title):
        """Create a new tasklist

        """
        new_tasklist = {
            'title': tasklist_title
        }
        result = self.service.tasklists().insert(body=new_tasklist).execute()
        return result['id']
    
    def list_tasks(self, tasklist_id):
        tasks = self.service.tasks().list(tasklist=tasklist_id).execute()
        if 'items' in tasks:
            return tasks['items']
        else:
            return []

    def get_task(self, tasklist_id, task_id):
        task = self.service.tasks().get(tasklist=tasklist_id, task=task_id).execute()
        return task

#if __name__ == '__main__':
#    gotask = GoTask()
#    gotask.list_tasklists()
