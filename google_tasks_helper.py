from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client import gce

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/tasks'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Tasks Helper'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'tasks-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('tasks', 'v1', http=http)

def get_tasks(date):
    all_tasks = service.tasks().list(tasklist='@default').execute()
    tasks_completed = []
    tasks_not_completed = []
    for task in all_tasks['items']:
        if (datetime.datetime.strptime(task['due'][0:10], "%Y-%m-%d").date() == date.date()):
            if (task['status'] == "completed"):
                tasks_completed.append(task)
            else:
                tasks_not_completed.append(task)
    return (tasks_completed, tasks_not_completed)

def get_task_id(date, task_list_id, index):
    task_lists = get_tasks(date)
    task_id = ""
    if (task_list_id.lower() == "a"):
        task_id = task_lists[0][index]['id']
    else:
        task_id = task_lists[1][index]['id']
    return task_id

def print_tasks(date):
    tasks_lists = get_tasks(date)
    completed = tasks_lists[0]
    not_completed = tasks_lists[1]

    print("Tasks for " + date.date().isoformat() + ":")
    
    completed_counter = 0
    print("\t(A) Completed:")
    for task in completed:
        print("\t\t(" + str(completed_counter) + ") " + task['title'])
        completed_counter += 1
    
    incomplete_counter = 0
    print("\t(B) Not Completed:")
    for task in not_completed:
        print("\t\t(" + str(incomplete_counter) + ") " + task['title'])
        incomplete_counter += 1

def add_task(task_title, date):
    newTask = {'title' : task_title, 'due' : date.isoformat()+"Z"}
    result = service.tasks().insert(tasklist='@default', body=newTask).execute()

def remove_task(date, task_list_id, index):
    task_id = get_task_id(date, task_list_id, index)
    service.tasks().delete(tasklist='@default', task=task_id).execute()

def complete_task(date, task_list_id, index):
    task_id = get_task_id(date, task_list_id, index)
    task = service.tasks().get(tasklist='@default', task=task_id).execute()
    task['status'] = 'completed'
    result = service.tasks().update(tasklist='@default', task=task['id'], body=task).execute()

def uncomplete_task(date, task_list_id, index):
    task_id = get_task_id(date, task_list_id, index)
    task = service.tasks().get(tasklist='@default', task=task_id).execute()
    task['status'] = 'needsAction'
    result = service.tasks().update(tasklist='@default', task=task['id'], body=task).execute()
    
def move_task(from_date, to_date, task_list_id, index):
    task_id = get_task_id(from_date, task_list_id, index)
    task = service.tasks().get(tasklist='@default', task=task_id).execute()
    task['due'] = to_date.isoformat()+"Z"
    result = service.tasks().update(tasklist='@default', task=task['id'], body=task).execute()
