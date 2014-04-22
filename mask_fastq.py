#!/usr/bin/env python

import re

def masked_fasta(file):
  def f(l,s):
    if s[0] == ">":
      l.append([s[1:].strip(),""])
      return l
    else:
      l[-1][1] += s.strip()
      return l
  return dict(reduce(f,file,[]))

def original_fastq(file):
  def f(l,s):
    if re.match(r"^@HWI-",s):
      l.append([s[1:].strip(), [""]])
      return l
    elif re.match(r"^\+$",s):
      l[-1][1].append("")
      return l
    else:
      l[-1][1][-1] += s.strip()
      return l
  return dict(reduce(f,file,[]))

def replace_seq(fastq, fasta):
  d = {}
  for key in fasta.keys():
    d[key] = [fasta[key], fastq[key][1]]
  return d  

def print_fastq(d,file):
  for key in d.keys():
    print >> file, "@%s\n%s\n+\n%s" % (key,d[key][0],d[key][1])

import argparse
import sys
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('masked_fasta',
                      type=argparse.FileType('r'))
  parser.add_argument('original_fastq',
                      type=argparse.FileType('r'))
  parser.add_argument('out_fastq',
                      nargs='?',
                      type=argparse.FileType('w'),
                      default=sys.stdout)
  args = parser.parse_args()
  print_fastq(replace_seq(original_fastq(args.original_fastq),
                          masked_fasta(args.masked_fasta))
              ,args.out_fastq)
