import os

#----------------------------------------------------------------
class Config :
  JIRAURL='https://jira.itsm.atosworldline.com' if 'JIRAURL' not in os.environ else os.environ['JIRAURL']
  JIRAUSER=os.environ['JIRAUSER']
  JIRAPROJECT='SDCOBENCH' if 'JIRAPROJECT' not in os.environ else os.environ['JIRAPROJECT']
  CURL='curl -s -D- -u ' + JIRAUSER
