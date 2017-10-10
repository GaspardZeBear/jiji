import os

#----------------------------------------------------------------
class Config :
  JIRAURL='https://jira.itsm.atosworldline.com' if 'JIRAURL' not in os.environ else os.environ['JIRAURL']
  JIRAUSER=os.environ['JIRAUSER']
  JIRAID=os.environ['JIRAID']
  JIRAPW=os.environ['JIRAPW']
  JIRAPROJECT='SDCOBENCH' if 'JIRAPROJECT' not in os.environ else os.environ['JIRAPROJECT']
  JIRANAME=JIRAUSER if 'JIRANAME' not in os.environ else os.environ['JIRANAME']
  CURL='curl -s -D- -u ' + JIRAUSER
  CURLPOST=CURL + ' -X POST -H "Content-Type: application/json"' 
