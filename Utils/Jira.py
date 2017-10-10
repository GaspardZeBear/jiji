import os
import json
import logging

from Config import *
from pprint import pprint,pformat
from jira import JIRA, JIRAError


#----------------------------------------------------------------
class Jirak :

  def __init__(self) :
    server={'server': Config.JIRAURL}
    #print(Config.JIRAID + " " + Config.JIRAPW)
    try :
      self.jira = JIRA(options=server,basic_auth=(Config.JIRAID,Config.JIRAPW))
    except Exception as e:
      print("JIRAError in class Jira ")
      pprint(e)
      if hasattr(e,'text') :
        print(e.text)
    self.getIssues() 

  def getIssues(self):
    fields=["id","key","summary","components","creator","created","updated","status","customfield_30941","customfield_10370","customfield_11730","assignee","reporter"]
    jql='project='+Config.JIRAPROJECT
    issues = self.jira.search_issues(jql,maxResults=1000,fields=fields,json_result=True)
    #for issue in issues :
    #  print(issue.key)
    return(issues)

  def getIssueKey(self,num):
    return(Config.JIRAPROJECT + '-' + str(num))

  def getIssue(self,num):
    return(self.jira.issue(self.getIssueKey(num)))

  def getTransitions(self,num):
    return(self.jira.transitions(self.getIssueKey(num)))

#----------------------------------------------------------------
class Jira :

  def jiraPost(self,request,url) :
    return(Config.CURLPOST + ' --data ' + request + ' ' +  Config.JIRAURL + url)

  def getJiraRestUri(self,num,suffix,prefix="/rest/api/latest/issue/") :
    return(url + '/' + Config.JIRAPROJECT + '-' + str(num) + suffix)

  def getSample(self):
    fields='["id","key","summary","components","creator","created","updated","status","customfield_30941","customfield_10370","customfield_11730"]'
    request='\'{"jql":"project =' + Config.JIRAPROJECT +'","startAt":0,"maxResults":1}\''
    cmd=Config.CURL + ' -X POST -H "Content-Type: application/json" --data ' + request + ' ' + Config.JIRAURL+'/rest/api/2/search'
    cmd=Config.CURL + ' ' + 'https://jira.itsm.atosworldline.com/rest/api/latest/issue/SDCOBENCH-243/'

    return(self.invoke(cmd))

  def getJiraList(self):
    fields='["id","key","summary","components","creator","created","updated","status","customfield_30941","customfield_10370","customfield_11730","assignee","reporter"]'
    request='\'{"jql":"project =' + Config.JIRAPROJECT +'","startAt":0,"maxResults":1000,"fields":' + fields + '}\''
    cmd=self.jiraPost(request,'/rest/api/2/search')
    return(self.invoke(cmd))

  def getIssue(self,num):
    cmd=Config.CURL + ' ' +  Config.JIRAURL +'/rest/api/latest/issue/' + Config.JIRAPROJECT + '-' + str(num) 
    return(self.invoke(cmd))

  def getComments(self,num):
    cmd=Config.CURL + ' ' +  Config.JIRAURL +'/rest/api/latest/issue/' + Config.JIRAPROJECT + '-' + str(num) + '/comment'
    cmd=Config.CURL + ' ' +  Config.JIRAURL + self.getJiraRestUri(num,'/comment')
    return(self.invoke(cmd))

  def addComment(self,num,comment):
    request='\'{"body": "' + 'From ' + Config.JIRANAME + ' : ' + comment[0] + '"}\''
    #cmd=Config.CURL + ' -X POST -H "Content-Type: application/json" --data ' + request + ' ' +  Config.JIRAURL+'/rest/api/latest/issue/' + Config.JIRAPROJECT + '-' + str(num) + '/comment'
    url='/rest/api/latest/issue/' + Config.JIRAPROJECT + '-' + str(num) + '/comment'
    cmd=self.jiraPost(request,url)
    return(self.invoke(cmd))

  def getTransitions(self,num):
    cmd=Config.CURL + ' ' +  Config.JIRAURL +'/rest/api/latest/issue/' + Config.JIRAPROJECT + '-' + str(num) + '/transitions'
    return(self.invoke(cmd))

  def transition(self,num,status):
    request='\'{"transition":{"id":"' + str(status[0])+'"}}\''
    cmd=self.jiraPost(request,'/rest/api/latest/issue/' + Config.JIRAPROJECT + '-' + str(num) + '/transitions')
    return(self.invoke(cmd,False))

  def invoke(self,cmd,returnDatas=True):
    jsonFile='exportJira.json'
    logging.debug(cmd)
    os.system(cmd+ '| grep "^{" > ' + jsonFile)
    if not returnDatas :
      return
    with open(jsonFile, 'r') as f:
      datas = json.load(f)
    logging.debug(pformat(datas))
    return(datas)

