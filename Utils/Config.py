import os
import logging

#----------------------------------------------------------------
class Config :
  JIRAURL='https://jira.itsm.atosworldline.com' if 'JIRAURL' not in os.environ else os.environ['JIRAURL']
  JIRAURL='https://jira.worldline.com' if 'JIRAURL' not in os.environ else os.environ['JIRAURL']
  JIRAUSER=os.environ['JIRAUSER']
  JIRAID=os.environ['JIRAID']
  JIRAPW=os.environ['JIRAPW']
  JIRAPROJECTLIST='SDCOBENCH or project=SUPPORT and component=DIP' if 'JIRAPROJECTLIST' not in os.environ else os.environ['JIRAPROJECTLIST']
  JIRAPROJECT='SDCOBENCH' if 'JIRAPROJECT' not in os.environ else os.environ['JIRAPROJECT']
  JIRANAME=JIRAUSER if 'JIRANAME' not in os.environ else os.environ['JIRANAME']
  CURL='curl -k -s -D- -u ' + JIRAUSER
  CURLPOST=CURL + ' -X POST -H "Content-Type: application/json"' 
  logging.warning("JIRAUSER {:s} JIRAID {:s} JIRAPW {:s}".format(JIRAUSER,JIRAID,JIRAPW))
  @staticmethod
  def guessProjectNameFromNum(jirano=-1) :
    logging.debug(jirano)
    if int(jirano) > 9000 :
      logging.debug("Jirano " + str(jirano) + " greater than 9000")
      return('SUPPORT')
    return('SDCOBENCH')
    
