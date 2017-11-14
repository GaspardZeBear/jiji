import json
import os
import sys
import re
import argparse
import logging
from Utils.Config import *
from Utils.Jira import *

reload(sys)
sys.setdefaultencoding('utf-8')
from pprint import pprint,pformat

status = {'Open':         'Activ',
          'In Progress' : 'Activ',
          'Solved'      : 'Activ',
          'Closed' :      'Inact',
          'Expertised' :      'Activ',
          'Information needed' : 'Activ'
}

#----------------------------------------------------------------
def fSample(args=None) :
  jira=Jira()
  datas=jira.getSample()
  pprint(datas)


#----------------------------------------------------------------
def translateStatus(stat) :
  if stat in status :
    return(status[stat])
  return(stat)

#----------------------------------------------------------------
def getComponents(fields,sep='') :
  if len(fields["components"]) > 0 :
    #return(fields["components"][0]["name"])
    cs=''
    for c in fields["components"] :
      if "name" in c :
        cs = cs + c["name"][0:3] + sep
    return(cs.rstrip(sep))
  return("None")


#----------------------------------------------------------------
def isComponentSelected(fields) :
  cs=set(getComponents(fields))
  a=set(args.components[0])
  if len(a & cs) > 0 :
    return True
  return False

#----------------------------------------------------------------
def displayIssue(datas) :
  f=datas["fields"]
  print('{:13.13};{:6.6};{:6.6};{:6.6};{:12.12};{};{};{:3.3};{:3.3};{:50.50};{:40.40};{:30.30}'.format(
      datas["key"],
      f["issuetype"]["name"],
      f["status"]["name"],
      translateStatus(f["status"]["name"]),
      getComponents(f,','),
      f["created"][0:10],
      f["updated"][0:10],
      f["creator"]["emailAddress"][0:20],
      f["assignee"]["emailAddress"][0:20],
      f["summary"].encode('ascii','replace'),
      f["customfield_10370"]["value"],
      f["customfield_11730"]
  ))
#      f["reporter"]["emailAddress"][0:20],
#      status[f["status"]["name"]],


#----------------------------------------------------------------
def fList(args=None) :
  logging.debug(pformat(args) )
  jira=Jirak()
  datas=jira.getIssues()
  for d in datas["issues"] :
    try :
      f=d["fields"]
      if f["status"]["name"] in status :
        if status[f["status"]["name"]][0:1] not in args.status[0] :
          continue
      #if f["components"][0]["name"][0:1] not in args.components[0] :
      if not isComponentSelected(f) :
        continue
      if args.summary and re.search(args.summary[0],f["summary"].encode('ascii','replace')) is None :
        continue
      if args.assignee and re.search(args.assignee[0],f["assignee"]["emailAddress"]) is None :
        continue
      displayIssue(d)
    except NameError :
      print(d["keys"] + " raised NameError")
    except :
      print(" raised Error")
  return

#----------------------------------------------------------------
def fCache(args=None) :
  return

#----------------------------------------------------------------
def printMark(section) :
  mark='='*100
  print("\n"+mark)
  print(section)
  print(mark)

#----------------------------------------------------------------
def showTransitions(datas) :
  printMark('Transitions')
  for d in datas["transitions"] :
    print("Next allowed status;{:5.5};{:10.10};{:100.100}".format(
     d["id"],
     d["name"],
     d["to"]["description"]
    ))
  #pprint(datas)


#----------------------------------------------------------------
def showComments(datas) :
  printMark('Comments')
  comments=datas["fields"]["comment"]["comments"]
  print("---------------------> Total " + str(len(comments)) + " comments")
  if args.back and len(comments) > int(args.back[0]) :
    start=-int(args.back[0])
    comments=comments[start:]
  for d in comments :
    body="".join([s for s in d["body"].splitlines(True) if s.strip()])
    print("\n{}\n;Comment;{:10.10};Author;{:50.50}\n".format(
     '-'*100,
     d["created"],
     d["author"]["emailAddress"]
    ))
    print("{}".format(
     body
    ))
  return

#"".join([s for s in mystr.splitlines(True) if s.strip()])
#----------------------------------------------------------------
def showHeader(datas) :
  printMark('Headers')
  f=datas["fields"]
  displayIssue(datas)

#----------------------------------------------------------------
def fInspect(args=None) :
  logging.debug(pformat(args) )
  jira=Jira()
  datas=jira.getIssue(args.jirano)
  #pprint(datas)
  if 'H' in args.show[0] :
    showHeader(datas)
    print(datas["fields"]["description"])
  if 'C' in args.show[0] :
    showComments(datas)
  if 'T' in args.show[0] :
    datasT=jira.getTransitions(args.jirano)
    showTransitions(datasT)
  return

#----------------------------------------------------------------
def NfInspect(args=None) :
  logging.debug(pformat(args) )
  jira=Jirak()
  datas=jira.getIssue(args.jirano)
  if 'H' in args.show[0] :
    showHeader(datas)
    print(datas["fields"]["description"])
  if 'C' in args.show[0] :
    showComments(datas)
  if 'T' in args.show[0] :
    datasT=jira.getTransitions(args.jirano)
    showTransitions(datasT)
  return



#----------------------------------------------------------------
def fComment(args=None) :
  logging.debug(pformat(args) )
  jira=Jira()
  datas=jira.addComment(args.jirano,args.body)
  return

#----------------------------------------------------------------
def fKanby(args=None) :
  logging.debug(pformat(args) )
  jira=Jira()
  return


#----------------------------------------------------------------
def fTransition(args=None) :
  logging.debug(pformat(args) )
  jira=Jira()
  jira.transition(args.jirano,args.status)
  datas=jira.getIssue(args.jirano)
  showHeader(datas)
  datasT=jira.getTransitions(args.jirano)
  showTransitions(datasT)
  return


#----------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument(
    '-d', '--debug',
    help="Print lots of debugging statements",
    action="store_const", dest="loglevel", const=logging.DEBUG,
    default=logging.WARNING,
)
parser.add_argument(
    '-v', '--verbose',
    help="Be verbose",
    action="store_const", dest="loglevel", const=logging.INFO,
)

subparsers = parser.add_subparsers(help='sub-command help')

parserList = subparsers.add_parser('list', help='a help')
parserList.set_defaults(func=fList)
parserList.add_argument('--summary','-f',nargs=1,help="filter for list")
parserList.add_argument('--assignee','-a',nargs=1,help="assignee")
parserList.add_argument('--components','-c',nargs=1,help="component Bench, Dip, Internal, Support, Project, OZI ",default=['BDISPO'])
parserList.add_argument('--status','-s',nargs=1,help="status Activ,Inact ",default=['A'])

parserSample = subparsers.add_parser('sample', help='a help')
parserSample.set_defaults(func=fSample)

parserCache = subparsers.add_parser('cache', help='a help')
parserCache.set_defaults(func=fCache)
parserCache.add_argument('num',nargs='?',help="num of file to cache")

parserInspect = subparsers.add_parser('inspect', help='a help')
parserInspect.set_defaults(func=fInspect)
parserInspect.add_argument('jirano',nargs='?',help="item to inspect (given by list)")
parserInspect.add_argument('--show','-s',nargs=1,help="Comments, Transitions",default=['CHT'])
parserInspect.add_argument('--back','-b',nargs=1,help="from end, count")
parserInspect.add_argument('--for','-f',nargs=1,help="from beginning, count")
parserInspect.add_argument('--exc','-x',nargs=1,help="no text")

parserComment = subparsers.add_parser('comment', help='a help')
parserComment.set_defaults(func=fComment)
parserComment.add_argument('jirano',nargs='?',help="item to comment (given by list)")
parserComment.add_argument('--body','-s',nargs=1,help="Comment",default='Seen')

parserTransition = subparsers.add_parser('transition', help='a help')
parserTransition.set_defaults(func=fTransition)
parserTransition.add_argument('jirano',nargs='?',help="item to transition (given by list)")
parserTransition.add_argument('--status','-s',nargs=1,help="Transition")

parserKanby = subparsers.add_parser('kanby', help='a help')
parserKanby.set_defaults(func=fKanby)


args=parser.parse_args()
logging.basicConfig(format="%(asctime)s %(funcName)s %(levelname)s %(message)s", level=args.loglevel) 


args.func(args)

