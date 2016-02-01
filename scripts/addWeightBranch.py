#! /bin/env python

import sys
import os

from array import array
from ROOT import *
import time
import shutil
import math
import multiprocessing
import rootpy.io as io
from rootpy.tree import Tree
import prettyjson
from argparse import ArgumentParser
import rootpy
from pdb import set_trace
import re
log = rootpy.log["/createNewTree"]
log.setLevel(rootpy.log.INFO)

def processNtuple(infile_name, outfile_name, sample, 
                  flav_weight=False, pteta_weight=False, cat_weight=False,
                  tag=''):  
  log.debug("processing %s --> %s" % (infile_name, outfile_name))
  
  fname_regex = re.compile('[a-zA-Z_0-9\/]*\/?[a-zA-Z_0-9]+_(?P<category>[a-zA-Z]+)_(?P<flavor>[A-Z]+)\.root')
  match = fname_regex.match(infile_name)

  if not match:
    raise ValueError("Could not match the regex to the file %s" % infile_name)
  flavor = match.group('flavor')
  full_category = match.group('category')
  weight_tfile = None
  flav_dir = None
  tfile_category = ''
  if pteta_weight or flav_weight or cat_weight:
    weight_tfile = io.root_open('../data_trees/%s_weights.root' % sample)
    flav_dir = weight_tfile.Get(flavor)
    categories = [i.name for i in flav_dir.keys()]
    #match existing categories to this one, which might be a subset of general category stored in the root file
    tfile_category = [i for i in categories if i in full_category][0] 

  weights = None
  if pteta_weight:    
    weights = flav_dir.Get('%s/kin' % tfile_category)
  flavor_weight = 1.
  if flav_weight:
    flavor_weight = prettyjson.loads(
      weight_tfile.flavour_weights.String().Data()
      )[flavor]
  #put bias weights
  category_weights = None
  if cat_weight:
    category_weights = flav_dir.Get('%s/bias' % tfile_category)
  
  print "Starting to process %s" %infile_name
  
  # make copy of input ntuple to be safe and work with that
  print "copying %s to %s" %(infile_name, outfile_name)
  shutil.copy2("%s" %(infile_name), "%s"%(outfile_name))
  
  # retrieve the ntuple of interest
  inFile = TFile.Open( "%s" %(outfile_name), "update" ) # this now uses the copied file in outDirName
  inTreeName = "ttree"
  myTree = inFile.Get( inTreeName )
  
  #create new branches
  weight_etaPt = array( "f", [ 0. ] )
  weight_category = array( "f", [ 0. ] )
  weight_flavour = array( "f", [ 0. ] )
  weight = array( "f", [ 0. ] )

  b_weight_etaPt = myTree.Branch( "weight_etaPt", weight_etaPt, 'weight_etaPt/F' )
  b_weight_category = myTree.Branch( "weight_category", weight_category, 'weight_category/F' )
  b_weight_flavour = myTree.Branch( "weight_flavour", weight_flavour, 'weight_flavour/F' )
  b_weight = myTree.Branch( "weight", weight, 'weight/F' )
  # connect branches needed for weight calculation
  Jet_pt = array( "f", [ 0. ] )
  Jet_eta = array( "f", [ 0. ] )
  myTree.SetBranchAddress( 'Jet_pt', Jet_pt )
  myTree.SetBranchAddress( 'Jet_eta', Jet_eta )

  ### actual loop ###
  entries = myTree.GetEntriesFast()
  print "%s: Starting event loop" %(multiprocessing.current_process().name)
  startTime = time.time()
  for ientry in xrange(entries):
    # get the next tree in the chain and verify
    myTree.GetEntry(ientry)
  
    # timing
    reportEveryNevents = 50000
    if (ientry%reportEveryNevents==0):
      if (ientry != 0):
        print "%s: Progress: %3.1f%%" %(multiprocessing.current_process().name, float(ientry)/(entries)*100)
        endTime = time.time()
        deltaTime = endTime - startTime
        rate = float(reportEveryNevents)/deltaTime
        print "%s: current rate: %5.2f Hz" %(multiprocessing.current_process().name, rate)
        startTime = time.time()
    
    # obtain the different weights
    weight[0] = 1.
    if pteta_weight:
      bin_idx = weights.FindFixBin(Jet_pt[0], abs(Jet_eta[0]))
      weight_etaPt[0] = weights[bin_idx].value
      weight[0] *= weights[bin_idx].value
    if flav_weight:
      weight_flavour[0] = flavor_weight
      weight[0] *= flavor_weight
    if cat_weight:
      bin_idx = category_weights.FindFixBin(Jet_pt[0], abs(Jet_eta[0]))          
      weight_category[0] = category_weights[bin_idx].value
      weight[0] *= category_weights[bin_idx].value
    # and fill the branches
    b_weight_etaPt.Fill()
    b_weight_category.Fill()
    b_weight_flavour.Fill()
    b_weight.Fill()
    
  inFile.Write()
  inFile.Close()
  print "%s: Total time: %5.2f s" %(multiprocessing.current_process().name, time.clock())



def main(args):
  parallelProcesses = multiprocessing.cpu_count()
  
  outDirName = '../data_trees/flat_trees/'
  outDirName = os.path.join(outDirName, args.sample)
  if not os.path.exists(outDirName):
    print "Creating new output directory: ", outDirName
    os.makedirs(outDirName)
  
  input_files = [i.strip() for i in open('../data_trees/inputs/%s.list' % args.sample)]
                
  # create Pool
  pool = multiprocessing.Pool(parallelProcesses)
  print "Using %i parallel processes" % parallelProcesses
  
  # run jobs
  nfiles = len(input_files)
  for idx, infile in enumerate(input_files): 
    base_input = os.path.basename(infile)
    outfile = os.path.join(outDirName, 'flat_%s' % base_input)
    proc_args = (
      infile, outfile, args.sample,
      args.flav_weight, args.kin_weight, args.cat_weight
      )
    if args.debug:
      processNtuple(*proc_args)
    else:
      pool.apply_async(
        processNtuple, 
        args = (
          infile, outfile, args.sample, 
          args.flav_weight, args.kin_weight, args.cat_weight,
          '%i/%i' % (idx, nfiles)
          )
        )
  pool.close()
  pool.join()
  


if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument('sample', help='sample to run on qcd or ttjets')
  parser.add_argument('--apply-pteta-weight',  dest='kin_weight', action='store_true', help='applies pt-eta weight')
  parser.add_argument('--apply-category-weight',  dest='cat_weight', action='store_true', help='applies category weight (from both qcd and ttjets)')
  parser.add_argument('--apply-flavor-weight', dest='flav_weight', action='store_true', help='applies flavour weight')
  parser.add_argument('--debug', action='store_true', help='does not run in parallel')
  args = parser.parse_args()
  if args.debug:
    log.setLevel(rootpy.log.DEBUG)
  import ROOT
  ROOT.gROOT.SetBatch(True)
  main(args)

#  LocalWords:  inFileList

