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
          'Closed' :      'Inact'
}

#----------------------------------------------------------------
def fSample(args=None) :
  jira=Jira()
  datas=jira.getSample()
  pprint(datas)


#----------------------------------------------------------------
def displayIssue(datas) :
  f=datas["fields"]
  print('{:13.13};{};{:5.5};{};{};{:3.3};{:3.3};{:50.50};{:40.40};{:30.30}'.format(
      datas["key"],
      status[f["status"]["name"]],
      f["components"][0]["name"],
      f["created"][0:10],
      f["updated"][0:10],
      f["creator"]["emailAddress"][0:20],
      f["assignee"]["emailAddress"][0:20],
      f["summary"].encode('ascii','replace'),
      f["customfield_10370"]["value"],
      f["customfield_11730"]
  ))
#      f["reporter"]["emailAddress"][0:20],


#----------------------------------------------------------------
def fList(args=None) :
  logging.debug(pformat(args) )
  jira=Jira()
  datas=jira.getJiraList()
  for d in datas["issues"] :
    f=d["fields"]
    if status[f["status"]["name"]][0:1] not in args.status[0] :
      continue
    if f["components"][0]["name"][0:1] not in args.components[0] :
      continue
    if args.summary and re.search(args.summary[0],f["summary"].encode('ascii','replace')) is None :
      continue
    if args.assignee and re.search(args.assignee[0],f["assignee"]["emailAddress"]) is None :
      continue
    displayIssue(d)
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
  for d in datas["fields"]["comment"]["comments"] :
    print("\n{}\n;Comment;{:10.10};Author;{:50.50}\n{}\n{}".format(
     '-'*100,
     d["created"],
     d["author"]["emailAddress"],
     '-'*100,
     d["body"]
    ))
  return

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
parserList.add_argument('--components','-c',nargs=1,help="component Bench, Support, Project ",default=['BDISP'])
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

parserComment = subparsers.add_parser('comment', help='a help')
parserComment.set_defaults(func=fComment)
parserComment.add_argument('jirano',nargs='?',help="item to comment (given by list)")
parserComment.add_argument('--body','-s',nargs=1,help="Comment",default='Seen')

parserTransition = subparsers.add_parser('transition', help='a help')
parserTransition.set_defaults(func=fTransition)
parserTransition.add_argument('jirano',nargs='?',help="item to transition (given by list)")
parserTransition.add_argument('--status','-s',nargs=1,help="Transition")

args=parser.parse_args()
logging.basicConfig(format="%(asctime)s %(funcName)s %(levelname)s %(message)s", level=args.loglevel) 


args.func(args)

