import json
import os
import sys
import re
import argparse
from Utils.Config import *
from Utils.Jira import *

reload(sys)
sys.setdefaultencoding('utf-8')
from pprint import pprint

status = {'Open':         'Activ',
          'In Progress' : 'Activ',
          'Solved'      : 'Activ',
          'Closed' :      'Inact'
}

#----------------------------------------------------------------
def fInspect(args=None) :
  jira=Jira()
  datas=jira.getInspect()
  pprint(datas)


#----------------------------------------------------------------
def fList(args=None) :
  jira=Jira()
  datas=jira.getJiraList()
  for d in datas["issues"] :
    #pprint(d)
    #exit()
    f=d["fields"]
    if status[f["status"]["name"]][0:1] not in args.status :
      continue
    if f["components"][0]["name"][0:1] not in args.comp :
      continue
    if args.summary and re.search(args.summary[0],f["summary"].encode('ascii','replace')) is None :
      continue
    if args.assignee and re.search(args.assignee[0],f["assignee"]["emailAddress"]) is None :
      continue
    print('{:13.13};{};{:5.5};{};{};{:3.3};{:3.3};{:3.3};{:50.50};{:40.40};{:30.30}'.format(
      d["key"],
      status[f["status"]["name"]],
      f["components"][0]["name"],
      f["created"][0:10],
      f["updated"][0:10],
      f["creator"]["emailAddress"][0:20],
      f["assignee"]["emailAddress"][0:20],
      f["reporter"]["emailAddress"][0:20],
      f["summary"].encode('ascii','replace'),
      f["customfield_10370"]["value"],
      f["customfield_11730"]
     ))
  return
#----------------------------------------------------------------
def fCache(args=None) :
  return

#----------------------------------------------------------------
def fScan(args=None) :
  jira=Jira()
  datas=jira.getComments(args.jirano)
  #pprint(datas)
  mark='-'*100
  for d in datas["comments"] :
    print("\n{}\n;Comment;{:10.10};Author;{:50.50}\n{}\n{}".format(
     mark,
     d["created"],
     d["author"]["emailAddress"],
     mark,
     d["body"]
    ))
  datas=jira.getTransitions(args.jirano)
  print("\n")
  print(mark)
  for d in datas["transitions"] :
    print("Next allowed status;{:5.5};{:10.10};{:100.100}".format(
     d["id"],
     d["name"],
     d["to"]["description"]
    ))
  #pprint(datas)
  return

#----------------------------------------------------------------
def fComment(args=None) :
  jira=Jira()
  datas=jira.addComment(args.jirano,args.body)
  return


#----------------------------------------------------------------
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='sub-command help')

parserList = subparsers.add_parser('list', help='a help')
parserList.set_defaults(func=fList)
parserList.add_argument('--summary','-f',nargs=1,help="filter for list")
parserList.add_argument('--assignee','-a',nargs=1,help="assignee")
parserList.add_argument('--comp','-c',nargs=1,help="component Bench, Support, Project ",default='BSP')
parserList.add_argument('--status','-s',nargs=1,help="status Activ,Inact ",default='A')

parserInspect = subparsers.add_parser('inspect', help='a help')
parserInspect.set_defaults(func=fInspect)

parserCache = subparsers.add_parser('cache', help='a help')
parserCache.set_defaults(func=fCache)
parserCache.add_argument('num',nargs='?',help="num of file to cache")

parserScan = subparsers.add_parser('scan', help='a help')
parserScan.set_defaults(func=fScan)
parserScan.add_argument('jirano',nargs='?',help="item to scan (given by list)")
parserScan.add_argument('--show','-s',nargs=1,help="Comments, Transitions",default='CT')

parserComment = subparsers.add_parser('comment', help='a help')
parserComment.set_defaults(func=fComment)
parserComment.add_argument('jirano',nargs='?',help="item to comment (given by list)")
parserComment.add_argument('--body','-s',nargs=1,help="Comment",default='Seen')

args=parser.parse_args()
args.func(args)

