import os
import json
import logging

from Config import *
from pprint import pprint,pformat
from jira import JIRA, JIRAError
from Utils.Trace import *


#----------------------------------------------------------------
class Jirak :

  @Trace
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

  #@Trace
  def getIssues(self):
    fields=["id","key","issuetype","summary","components","creator","created","updated","status","customfield_30941","customfield_10370","customfield_11730","assignee","reporter"]
    jql='project='+Config.JIRAPROJECTLIST
    issues = self.jira.search_issues(jql,maxResults=1000,fields=fields,json_result=True)
    #for issue in issues :
    #  print(issue.key)
    return(issues)

  def getIssueKey(self,num):
    #return(Config.JIRAPROJECT + '-' + str(num))
    return(Config.guessProjectNameFromNum(num) + '-' + str(num))

  def getIssue(self,num):
    return(self.jira.issue(self.getIssueKey(num)))

  def getTransitions(self,num):
    return(self.jira.transitions(self.getIssueKey(num)))

#----------------------------------------------------------------
class Jira :

  #@Trace
  def __init__(self) :
    pass

  def jiraPost(self,request,url) :
    return(Config.CURLPOST + ' --data ' + request + ' ' +  Config.JIRAURL + url)

  def getJiraRestUri(self,num,suffix,prefix="/rest/api/latest/issue") :
    return(prefix + '/' + self.getIssueKey(num) + suffix)

  def getSample(self):
    request='\'{"jql":"project =' + Config.JIRAPROJECT +'","startAt":0,"maxResults":1}\''
    fields='["id","key","summary","components","creator","created","updated","status","customfield_30941","customfield_10370","customfield_11730","assignee","reporter"]'
    request='\'{"jql":"project =' + Config.JIRAPROJECT +'","startAt":0,"maxResults":1000,"fields":' + fields + '}\''
    cmd=Config.CURL + ' -X POST -H "Content-Type: application/json" --data ' + request + ' ' + Config.JIRAURL+'/rest/api/2/search'
    return(self.invoke(cmd))

  def getJiraList(self):
    fields='["id","key","summary","components","creator","created","updated","status","customfield_30941","customfield_10370","customfield_11730","assignee","reporter"]'
    request='\'{"jql":"project =' + Config.JIRAPROJECTLIST +'","startAt":0,"maxResults":1000,"fields":' + fields + '}\''
    cmd=self.jiraPost(request,'/rest/api/2/search')
    return(self.invoke(cmd))
  
  def getIssueKey(self,num):
    return(Config.guessProjectNameFromNum(num) + '-' + str(num))

  def getIssue(self,num):
    cmd=Config.CURL + ' ' +  Config.JIRAURL +'/rest/api/latest/issue/' + self.getIssueKey(num)
    return(self.invoke(cmd))

  def getComments(self,num):
    cmd=Config.CURL + ' ' +  Config.JIRAURL + self.getJiraRestUri(num,'/comment')
    return(self.invoke(cmd))

  def addComment(self,num,comment):
    request='\'{"body": "' + 'From ' + Config.JIRANAME + ' : ' + comment[0] + '"}\''
    url='/rest/api/latest/issue/' + Config.JIRAPROJECT + '-' + str(num) + '/comment'
    cmd=self.jiraPost(request,url)
    return(self.invoke(cmd))

  def getTransitions(self,num):
    cmd=Config.CURL + ' ' +  Config.JIRAURL + self.getJiraRestUri(num,'/transitions')
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

