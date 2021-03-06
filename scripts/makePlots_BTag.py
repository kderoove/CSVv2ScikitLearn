import sys
sys.argv.append( '-b-' )
import os
import ROOT
from ROOT import *
from array import array
import time
import multiprocessing
import thread
import subprocess
import math



Jet_flavourCutsDict = {}
Jet_flavourCutsDict["B"] = "Jet_flavour == 5"
Jet_flavourCutsDict["C"] = "Jet_flavour == 4"
Jet_flavourCutsDict["light"] = "Jet_flavour !=4 && Jet_flavour !=5"
Jet_flavourCutsDict["non-C"] = "Jet_flavour !=4"
Jet_flavourCutsDict["non-B"] = "Jet_flavour !=5"

# also add TagVarCSV_vertexCategory
categoryCutsDict = {}
categoryCutsDict["NoVertex"] = "TagVarCSV_vertexCategory == 2"
categoryCutsDict["PseudoVertex"] = "TagVarCSV_vertexCategory == 1"
categoryCutsDict["RecoVertex"] = "TagVarCSV_vertexCategory == 0"

categories = []
categories.append("NoVertex")
categories.append("PseudoVertex")
categories.append("RecoVertex")
categories.append("Inclusive")

Jet_flavours = []
Jet_flavours.append("B")
Jet_flavours.append("C")
Jet_flavours.append("light")
Jet_flavours.append("non-C")
Jet_flavours.append("non-B")

PtBins = []
PtBins = []
PtBins.append
PtBins.append("Jet_pt > 15")
PtBins.append("15 < Jet_pt and Jet_pt <= 40")
PtBins.append("40 < Jet_pt and Jet_pt <= 60")
PtBins.append("60 < Jet_pt and Jet_pt <= 90")
PtBins.append("90 < Jet_pt and Jet_pt <= 150")
PtBins.append("150 < Jet_pt and Jet_pt <=400")
PtBins.append("Jet_pt > 400")
PtBins.append("Jet_pt > 30")
PtBins.append("Jet_pt > 150")


etaPtBins = []
etaPtBins.append
etaPtBins.append("15 < Jet_pt and Jet_pt <= 40 and abs(Jet_eta) <= 1.2")
etaPtBins.append("15 < Jet_pt and Jet_pt <= 40 and 1.2 < abs(Jet_eta) and abs(Jet_eta) <= 2.1")
etaPtBins.append("15 < Jet_pt and Jet_pt <= 40 and abs(Jet_eta) > 2.1")
etaPtBins.append("40 < Jet_pt and Jet_pt <= 60 and abs(Jet_eta) <= 1.2")
etaPtBins.append("40 < Jet_pt and Jet_pt <= 60 and 1.2 < abs(Jet_eta) and abs(Jet_eta) <= 2.1")
etaPtBins.append("40 < Jet_pt and Jet_pt <= 60 and abs(Jet_eta) > 2.1")
etaPtBins.append("60 < Jet_pt and Jet_pt <= 90 and abs(Jet_eta) <= 1.2")
etaPtBins.append("60 < Jet_pt and Jet_pt <= 90 and 1.2 < abs(Jet_eta) and abs(Jet_eta) <= 2.1")
etaPtBins.append("60 < Jet_pt and Jet_pt <= 90 and abs(Jet_eta) > 2.1")
etaPtBins.append("90 < Jet_pt and Jet_pt <= 150 and abs(Jet_eta) <= 1.2")
etaPtBins.append("90 < Jet_pt and Jet_pt <= 150 and 1.2 < abs(Jet_eta) and abs(Jet_eta) <= 2.1")
etaPtBins.append("90 < Jet_pt and Jet_pt <= 150 and abs(Jet_eta) > 2.1")
etaPtBins.append("150 < Jet_pt and Jet_pt <= 400 and abs(Jet_eta) <= 1.2")
etaPtBins.append("150 < Jet_pt and Jet_pt <= 400 and 1.2 < abs(Jet_eta) and abs(Jet_eta) <= 2.1")
etaPtBins.append("150 < Jet_pt and Jet_pt <= 400 and abs(Jet_eta) > 2.1")
etaPtBins.append("400 < Jet_pt and Jet_pt <= 600 and abs(Jet_eta)<= 1.2")
etaPtBins.append("400 < Jet_pt and Jet_pt <= 600 and abs(Jet_eta) > 1.2")
etaPtBins.append("Jet_pt > 600 and abs(Jet_eta) <= 1.2")
etaPtBins.append("Jet_pt > 600 and abs(Jet_eta) > 1.2")
  


def processNtuple(inFileName, inDirName, outDirName,):
  
  print "Starting to process %s" %inFileName
  # retrieve the ntuple of interest
  inFile = TFile( "%s/%s" %(inDirName, inFileName) )
  inTreeName = "ttree"
  mychain = gDirectory.Get( inTreeName )
  
  # output
  outFileName = "%s/%s_Histograms.root" %(outDirName, inFileName.rsplit(".",1)[0])
  print "Writing to %s" %outFileName
  outFile = TFile( outFileName, 'recreate' )

  discriminantHistos = []
  nBins = 100
  
  for flav in Jet_flavourCutsDict.keys():
    discriminantHisto = TH1D("histBDTG_%s"%flav, "BDTG output for %s;BDTG value"%flav, nBins, 0, 1)
    mychain.Draw("BDTG >> +histBDTG_%s"%flav, Jet_flavourCutsDict[flav], "")
    discriminantHisto.Write()
    discriminantHistos.append(discriminantHisto)
    for i in range(len(etaPtBins)):
      discriminantHisto = TH1D("histBDTG_%s_EtaPt%i"%(flav, i), "BDTG output for %s and %s;BDTG value"%(flav, etaPtBins[i]), nBins, 0, 1)
      mychain.Draw("BDTG >> +histBDTG_%s_EtaPt%i"%(flav, i), "(%s) && (%s)" %(Jet_flavourCutsDict[flav], etaPtBins[i].replace("and","&&")), "")
      discriminantHisto.Write()
      discriminantHistos.append(discriminantHisto)
    for cat in categoryCutsDict.keys():
      discriminantHisto = TH1D("histBDTG_%s_%s"%(flav, cat), "BDTG output for %s and %s;BDTG value"%(flav, cat), nBins, 0, 1)
      mychain.Draw("BDTG >> +histBDTG_%s_%s"%(flav, cat), "%s && %s"%(Jet_flavourCutsDict[flav], categoryCutsDict[cat]), "")
      discriminantHisto.Write()
      discriminantHistos.append(discriminantHisto)
    for j in range(len(PtBins)):
      discriminantHisto = TH1D("histBDTG_%s_Pt%i"%(flav, j), "BDTG output for %s and %s;BDTG value"%(flav, PtBins[j]), nBins, 0, 1)
      mychain.Draw("BDTG >> +histBDTG_%s_Pt%i"%(flav, j), "(%s) && (%s)" %(Jet_flavourCutsDict[flav], PtBins[j].replace("and","&&")), "")
      discriminantHisto.Write()
      discriminantHistos.append(discriminantHisto)

#  outFile.Close()
#
#  outFileName_ = "%s/%s_Histograms_CSVIVF.root" %(outDirName, inFileName.rsplit(".",1)[0])
#  print "Writing to %s" %outFileName_
#  outFile_ = TFile( outFileName_, 'recreate' )

  for flav in Jet_flavourCutsDict.keys():
    discriminantHisto = TH1D("histJet_CSVIVF_%s"%flav, "Jet_CSVIVF output for %s;Jet_CSVIVF value"%flav, nBins, 0, 1)
    mychain.Draw("Jet_CSVIVF >> +histJet_CSVIVF_%s"%flav, Jet_flavourCutsDict[flav], "")
    discriminantHisto.Write()
    discriminantHistos.append(discriminantHisto)
    for i in range(len(etaPtBins)):
      discriminantHisto = TH1D("histJet_CSVIVF_%s_EtaPt%i"%(flav, i), "Jet_CSVIVF output for %s and %s;Jet_CSVIVF value"%(flav, etaPtBins[i]), nBins, 0, 1)
      mychain.Draw("Jet_CSVIVF >> +histJet_CSVIVF_%s_EtaPt%i"%(flav, i), "(%s) && (%s)" %(Jet_flavourCutsDict[flav], etaPtBins[i].replace("and","&&")), "")
      discriminantHisto.Write()
      discriminantHistos.append(discriminantHisto)
    for cat in categoryCutsDict.keys():
      discriminantHisto = TH1D("histJet_CSVIVF_%s_%s"%(flav, cat), "Jet_CSVIVF output for %s and %s;Jet_CSVIVF value"%(flav, cat), nBins, 0, 1)
      mychain.Draw("Jet_CSVIVF >> +histJet_CSVIVF_%s_%s"%(flav, cat), "%s && %s"%(Jet_flavourCutsDict[flav], categoryCutsDict[cat]), "")
      discriminantHisto.Write()
      discriminantHistos.append(discriminantHisto)
    for j in range(len(PtBins)):
      discriminantHisto = TH1D("histJet_CSVIVF_%s_Pt%i"%(flav, j), "Jet_CSVIVF output for %s and %s;Jet_CSVIVF value"%(flav, PtBins[j]), nBins, 0, 1)
      mychain.Draw("Jet_CSVIVF >> +histJet_CSVIVF_%s_Pt%i"%(flav, j), "(%s) && (%s)" %(Jet_flavourCutsDict[flav], PtBins[j].replace("and","&&")), "")
      discriminantHisto.Write()
      discriminantHistos.append(discriminantHisto)

  outFile.Close()  
#  outFile_.Close()
  inFile.Close()


def makeROCCurves(outDirName):
  
  nBins = 100
  xBins = array("d")
  xBinsPlot = array("d")
  yBinsPlot = array("d")
  for i in range(0,nBins+2):
    xBins.append(float(i)/nBins)
  outFileName = "%s/AllHistograms.root" %(outDirName)
  print "Updating %s" %outFileName
  outFile = TFile.Open(outFileName, "update")
  histDictFlav = [[0 for x in range(len(PtBins))] for y in range(len(Jet_flavours))]
  histDictFlavEffs = [[0 for x in range(len(PtBins))] for y in range(len(Jet_flavours))]
  histDictFlavEffsError = [[0 for x in range(len(PtBins))] for y in range(len(Jet_flavours))]
  histDictFlavCat = [[0 for x in range(len(categories))] for y in range(len(Jet_flavours))]
  histDictFlavCatEffs = [[0 for x in range(len(categories))] for y in range(len(Jet_flavours))]
  histDictFlavCatEffsError = [[0 for x in range(len(categories))] for y in range(len(Jet_flavours))]
  for flav in range(len(Jet_flavours)):
    for j in range(len(PtBins)):
      histDictFlav[flav][j] = outFile.Get("histBDTG_%s_Pt%i"%(Jet_flavours[flav],j))
      histDictFlavEffs[flav][j] = array("d")
      histDictFlavEffsError[flav][j] = array("d")
      integral = histDictFlav[flav][j].Integral(0, histDictFlav[flav][j].GetNbinsX()+1)
      for xbin in range(0, histDictFlav[flav][j].GetNbinsX()+2):
        histDictFlavEffs[flav][j].append(histDictFlav[flav][j].Integral(xbin, histDictFlav[flav][j].GetNbinsX()+1)/integral) # Eff = Sum(binx --> end) / Sum(begin --> end)
	histDictFlavEffsError[flav][j].append(math.sqrt(histDictFlav[flav][j].Integral(xbin, histDictFlav[flav][j].GetNbinsX()+1))/integral)
    for c in range(len(categories)):
      if c < (len(categories)-1):
        histDictFlavCat[flav][c] = outFile.Get("histBDTG_%s_%s"%(Jet_flavours[flav],categories[c]))
      else:
        histDictFlavCat[flav][c] = outFile.Get("histBDTG_%s"%(Jet_flavours[flav]))
      histDictFlavCatEffs[flav][c] = array("d")
      histDictFlavCatEffsError[flav][c] = array("d")
      integral = histDictFlavCat[flav][c].Integral(0, histDictFlavCat[flav][c].GetNbinsX()+1)
      #print "histBDTG_%s_%s"%(Jet_flavours[flav],categories[c])
      #print integral
      for xbin in range(0, histDictFlavCat[flav][c].GetNbinsX()+2):
        histDictFlavCatEffs[flav][c].append(histDictFlavCat[flav][c].Integral(xbin, histDictFlavCat[flav][c].GetNbinsX()+1)/integral)
	histDictFlavCatEffsError[flav][c].append(math.sqrt(histDictFlavCat[flav][c].Integral(xbin, histDictFlavCat[flav][c].GetNbinsX()+1))/integral)


  # Create Efficiency v. Discriminator bin plots
  canvas1 = TCanvas("c0","Eff",800,800)
  XbinEff = array("d")
  YbinEff = array("d")
  XbinEffError = array("d") # dummy
  YbinEffError = array("d")
  for flav in range(len(Jet_flavours)):
    for cat in range(len(categories)):
      del XbinEff[:]
      del YbinEff[:]
      del XbinEffError[:] # dummy
      del YbinEffError[:]
      for Xbin in range(0,histDictFlavCat[flav][cat].GetNbinsX()+1):
        YbinEff.append(histDictFlavCatEffs[flav][cat][Xbin])
	YbinEffError.append(histDictFlavCatEffsError[flav][cat][Xbin])
        XbinEff.append(histDictFlavCat[flav][cat].GetBinCenter(Xbin))
	XbinEffError.append(0) # dummy
        #XbinEff.append(histDictFlavCat[flav][cat].Integral(Xbin,histDictFlavCat[flav][cat].GetNbinsX()+1))
        #XbinEff.append(Xbin)
      EffCurve = TGraphErrors(len(XbinEff),XbinEff,YbinEff,XbinEffError,YbinEffError)
      EffCurve.GetXaxis().SetTitle("%s Discriminant"%(Jet_flavours[flav]))
      EffCurve.GetYaxis().SetTitle("%s efficiency"%(Jet_flavours[flav]))
      EffCurve.SetTitle("%s efficiency, %s"%(Jet_flavours[flav],categories[cat]))
      EffCurve.SetName("Efficiency_%s_discrim_%s"%(Jet_flavours[flav],categories[cat]))
      EffCurve.Draw("al")
      gPad.SetGridx(1)
      gPad.SetGridy(1)
      #canvas1.SaveAs("%s/%s.png" %(outDirName, EffCurve.GetName()))
      EffCurve.Write()

  # Create ROC curves for vertex categories
  canvas2 = TCanvas("c2","ROC",800,800);
  for flav1 in range(len(Jet_flavours)):
    for flav2 in range(len(Jet_flavours)):
      for cat in range(len(categories)):
        del xBinsPlot[:]
        del yBinsPlot[:]
        yBins = array("d")
        for i in range(0,nBins+2):
          yBins.append(0.)
        integral1 = histDictFlavCat[flav1][cat].Integral(0, histDictFlavCat[flav1][cat].GetNbinsX()+1)
        discrimBin = histDictFlavCat[flav1][cat].GetNbinsX()+1 
        for currentBin in range(0,nBins+2):
          currentEff = histDictFlavCatEffs[flav1][cat][discrimBin]
          yBins[currentBin] = histDictFlavCatEffs[flav2][cat][discrimBin]
          while currentEff < xBins[currentBin] and discrimBin > 0:
            discrimBin -= 1
            currentEff = histDictFlavCatEffs[flav1][cat][discrimBin]
            yBins[currentBin] = histDictFlavCatEffs[flav2][cat][discrimBin]
          if (currentBin < (nBins+1) and currentEff < xBins[currentBin+1]):
            xBinsPlot.append(xBins[currentBin])
            yBinsPlot.append(yBins[currentBin])

        rocCurve = TGraph(len(xBinsPlot),xBinsPlot,yBinsPlot)
        rocCurve.GetXaxis().SetTitle("%s efficiency"%Jet_flavours[flav1])
        rocCurve.GetYaxis().SetTitle("%s efficiency"%Jet_flavours[flav2])
        rocCurve.SetTitle("%s vs. %s, %s"%(Jet_flavours[flav1], Jet_flavours[flav2], categories[cat]))
        rocCurve.SetName("ROC_%s_%s_%s"%(Jet_flavours[flav1], Jet_flavours[flav2],categories[cat]))
        rocCurve.GetYaxis().SetRangeUser(0.0001,1.0);
        rocCurve.GetXaxis().SetLimits(0.,1.0);
        rocCurve.Draw("al")
        gPad.SetGridx(1)
        gPad.SetGridy(1)
        gPad.SetLogy()
        #canvas2.SaveAs("%s/%s.png" %(outDirName, rocCurve.GetName()))
        rocCurve.Write()
        
  # Create ROC curves
  canvas = TCanvas("c1","ROC",800,800);
  for flav1 in range(len(Jet_flavours)):
    for flav2 in range(len(Jet_flavours)):
      for n in range(len(PtBins)):
        del xBinsPlot[:]
        del yBinsPlot[:]
        yBins = array("d")
        for i in range(0,nBins+2):
          yBins.append(0.)
        integral1 = histDictFlav[flav1][n].Integral(0, histDictFlav[flav1][n].GetNbinsX()+1)
        #del xBinsPlot[:]
        #del yBinsPlot[:]
        #print "ROC curve for flavor %s %s" %(flav1,flav2)
        # loop over efficiency values starting at 0 (i.e. highest bin)
        discrimBin = histDictFlav[flav1][n].GetNbinsX()+1
        for currentBin in range(0,nBins+2):
          # get discriminant bin for signal
          currentEff = histDictFlavEffs[flav1][n][discrimBin]
          yBins[currentBin] = histDictFlavEffs[flav2][n][discrimBin]
        #print "%i - %i: %f - %f - %f" %(currentBin, discrimBin, xBins[currentBin], currentEff, yBins[currentBin])
          while currentEff < xBins[currentBin] and discrimBin > 0:
            discrimBin -= 1
            currentEff = histDictFlavEffs[flav1][n][discrimBin]
            yBins[currentBin] = histDictFlavEffs[flav2][n][discrimBin]
            #print "while %i - %i: %f - %f - %f" %(currentBin, discrimBin, xBins[currentBin], currentEff, yBins[currentBin])
          #print "--------------"
          if (currentBin < (nBins+1) and currentEff < xBins[currentBin+1]):
            xBinsPlot.append(xBins[currentBin])
            yBinsPlot.append(yBins[currentBin])

        
        #print yBins
        #print len(yBins)

        #print "eff vs eff"
        #for i in range (0, len(xBinsPlot)):
        #  print "%f %f" %(xBinsPlot[i], yBinsPlot[i])

        #rocCurve = TGraph(len(xBins),xBins,yBins)
        rocCurve = TGraph(len(xBinsPlot),xBinsPlot,yBinsPlot)
        rocCurve.GetXaxis().SetTitle("%s efficiency"%Jet_flavours[flav1])
        rocCurve.GetYaxis().SetTitle("%s efficiency"%Jet_flavours[flav2])
        rocCurve.SetTitle("%s vs. %s, %s"%(Jet_flavours[flav1], Jet_flavours[flav2], PtBins[n]))
        rocCurve.SetName("ROC_%s_%s_%i"%(Jet_flavours[flav1], Jet_flavours[flav2],n))
        rocCurve.GetYaxis().SetRangeUser(0.0001,1.0);
        rocCurve.GetXaxis().SetLimits(0.,1.0);
        #TH1D("ROC_%s_%s"%(flav1, flav2), "ROC curve for %s vs. %s;%s efficiency;%s efficiency"%(flav1, flav2, flav1, flav2), 100, -1, 1)
        rocCurve.Draw("al")
        gPad.SetGridx(1)
        gPad.SetGridy(1)
        gPad.SetLogy()
        #canvas.SaveAs("%s/%s.png" %(outDirName, rocCurve.GetName()))
        rocCurve.Write()
      #break
  outFile.Close()        
  

def makeROCCurves_CSVIVF(outDirName):
  
  nBins = 100
  xBins = array("d")
  xBinsPlot = array("d")
  yBinsPlot = array("d")
  for i in range(0,nBins+2):
    xBins.append(float(i)/nBins)
  outFileName = "%s/AllHistograms_CSVIVF.root" %(outDirName)
  print "Updating %s" %outFileName
  outFile = TFile.Open(outFileName, "update")
  histDictFlav = [[0 for x in range(len(PtBins))] for y in range(len(Jet_flavours))]
  histDictFlavEffs = [[0 for x in range(len(PtBins))] for y in range(len(Jet_flavours))]
  histDictFlavEffsError = [[0 for x in range(len(PtBins))] for y in range(len(Jet_flavours))]
  histDictFlavCat = [[0 for x in range(len(categories))] for y in range(len(Jet_flavours))]
  histDictFlavCatEffs = [[0 for x in range(len(categories))] for y in range(len(Jet_flavours))]
  histDictFlavCatEffsError = [[0 for x in range(len(categories))] for y in range(len(Jet_flavours))]
  for flav in range(len(Jet_flavours)):
    for j in range(len(PtBins)):
      histDictFlav[flav][j] = outFile.Get("histJet_CSVIVF_%s_Pt%i"%(Jet_flavours[flav],j))
      histDictFlavEffs[flav][j] = array("d")
      histDictFlavEffsError[flav][j] = array("d")
      integral = histDictFlav[flav][j].Integral(0, histDictFlav[flav][j].GetNbinsX()+1)
      for xbin in range(0, histDictFlav[flav][j].GetNbinsX()+2):
        histDictFlavEffs[flav][j].append(histDictFlav[flav][j].Integral(xbin, histDictFlav[flav][j].GetNbinsX()+1)/integral) # Eff = Sum(binx --> end) / Sum(begin --> end)
	histDictFlavEffsError[flav][j].append(math.sqrt(histDictFlav[flav][j].Integral(xbin, histDictFlav[flav][j].GetNbinsX()+1))/integral)
    for c in range(len(categories)):
      if c < (len(categories)-1):
        histDictFlavCat[flav][c] = outFile.Get("histJet_CSVIVF_%s_%s"%(Jet_flavours[flav],categories[c]))
      else:
        histDictFlavCat[flav][c] = outFile.Get("histJet_CSVIVF_%s"%(Jet_flavours[flav]))
      histDictFlavCatEffs[flav][c] = array("d")
      histDictFlavCatEffsError[flav][c] = array("d")
      integral = histDictFlavCat[flav][c].Integral(0, histDictFlavCat[flav][c].GetNbinsX()+1)
      for xbin in range(0, histDictFlavCat[flav][c].GetNbinsX()+2):
        histDictFlavCatEffs[flav][c].append(histDictFlavCat[flav][c].Integral(xbin, histDictFlavCat[flav][c].GetNbinsX()+1)/integral)
	histDictFlavCatEffsError[flav][c].append(math.sqrt(histDictFlavCat[flav][c].Integral(xbin, histDictFlavCat[flav][c].GetNbinsX()+1))/integral)


  # Create Efficiency v. Discriminator bin plots
  canvas1 = TCanvas("c0","Eff",800,800)
  XbinEff = array("d")
  YbinEff = array("d")
  XbinEffError = array("d") # dummy
  YbinEffError = array("d")
  for flav in range(len(Jet_flavours)):
    for cat in range(len(categories)):
      del XbinEff[:]
      del YbinEff[:]
      del XbinEffError[:] # dummy
      del YbinEffError[:]
      for Xbin in range(0,histDictFlavCat[flav][cat].GetNbinsX()+1):
        YbinEff.append(histDictFlavCatEffs[flav][cat][Xbin])
	YbinEffError.append(histDictFlavCatEffsError[flav][cat][Xbin])
        XbinEff.append(histDictFlavCat[flav][cat].GetBinCenter(Xbin))
	XbinEffError.append(0) # dummy
        #XbinEff.append(histDictFlavCat[flav][cat].Integral(Xbin,histDictFlavCat[flav][cat].GetNbinsX()+1))
        #XbinEff.append(Xbin)
      EffCurve = TGraphErrors(len(XbinEff),XbinEff,YbinEff,XbinEffError,YbinEffError)
      EffCurve.GetXaxis().SetTitle("%s Discriminant"%(Jet_flavours[flav]))
      EffCurve.GetYaxis().SetTitle("%s efficiency"%(Jet_flavours[flav]))
      EffCurve.SetTitle("%s efficiency, %s"%(Jet_flavours[flav],categories[cat]))
      EffCurve.SetName("Efficiency_%s_discrim_%s"%(Jet_flavours[flav],categories[cat]))
      EffCurve.Draw("al")
      gPad.SetGridx(1)
      gPad.SetGridy(1)
      #canvas1.SaveAs("%s/%s.png" %(outDirName, EffCurve.GetName()))
      EffCurve.Write()

  # Create ROC curves for vertex categories
  canvas2 = TCanvas("c2","ROC",800,800);
  for flav1 in range(len(Jet_flavours)):
    for flav2 in range(len(Jet_flavours)):
      for cat in range(len(categories)):
        del xBinsPlot[:]
        del yBinsPlot[:]
        yBins = array("d")
        for i in range(0,nBins+2):
          yBins.append(0.)
        integral1 = histDictFlavCat[flav1][cat].Integral(0, histDictFlavCat[flav1][cat].GetNbinsX()+1)
        discrimBin = histDictFlavCat[flav1][cat].GetNbinsX()+1 
        for currentBin in range(0,nBins+2):
          currentEff = histDictFlavCatEffs[flav1][cat][discrimBin]
          yBins[currentBin] = histDictFlavCatEffs[flav2][cat][discrimBin]
          while currentEff < xBins[currentBin] and discrimBin > 0:
            discrimBin -= 1
            currentEff = histDictFlavCatEffs[flav1][cat][discrimBin]
            yBins[currentBin] = histDictFlavCatEffs[flav2][cat][discrimBin]
          if (currentBin < (nBins+1) and currentEff < xBins[currentBin+1]):
            xBinsPlot.append(xBins[currentBin])
            yBinsPlot.append(yBins[currentBin])

        rocCurve = TGraph(len(xBinsPlot),xBinsPlot,yBinsPlot)
        rocCurve.GetXaxis().SetTitle("%s efficiency"%Jet_flavours[flav1])
        rocCurve.GetYaxis().SetTitle("%s efficiency"%Jet_flavours[flav2])
        rocCurve.SetTitle("%s vs. %s, %s"%(Jet_flavours[flav1], Jet_flavours[flav2], categories[cat]))
        rocCurve.SetName("ROC_%s_%s_%s"%(Jet_flavours[flav1], Jet_flavours[flav2],categories[cat]))
        rocCurve.GetYaxis().SetRangeUser(0.0001,1.0);
        rocCurve.GetXaxis().SetLimits(0.,1.0);
        rocCurve.Draw("al")
        gPad.SetGridx(1)
        gPad.SetGridy(1)
        gPad.SetLogy()
        #canvas2.SaveAs("%s/%s.png" %(outDirName, rocCurve.GetName()))
        rocCurve.Write()
        
  # Create ROC curves
  canvas = TCanvas("c1","ROC",800,800);
  for flav1 in range(len(Jet_flavours)):
    for flav2 in range(len(Jet_flavours)):
      for n in range(len(PtBins)):
        del xBinsPlot[:]
        del yBinsPlot[:]
        yBins = array("d")
        for i in range(0,nBins+2):
          yBins.append(0.)
        integral1 = histDictFlav[flav1][n].Integral(0, histDictFlav[flav1][n].GetNbinsX()+1)
        #del xBinsPlot[:]
        #del yBinsPlot[:]
        #print "ROC curve for flavor %s %s" %(flav1,flav2)
        # loop over efficiency values starting at 0 (i.e. highest bin)
        discrimBin = histDictFlav[flav1][n].GetNbinsX()+1
        for currentBin in range(0,nBins+2):
          # get discriminant bin for signal
          currentEff = histDictFlavEffs[flav1][n][discrimBin]
          yBins[currentBin] = histDictFlavEffs[flav2][n][discrimBin]
        #print "%i - %i: %f - %f - %f" %(currentBin, discrimBin, xBins[currentBin], currentEff, yBins[currentBin])
          while currentEff < xBins[currentBin] and discrimBin > 0:
            discrimBin -= 1
            currentEff = histDictFlavEffs[flav1][n][discrimBin]
            yBins[currentBin] = histDictFlavEffs[flav2][n][discrimBin]
            #print "while %i - %i: %f - %f - %f" %(currentBin, discrimBin, xBins[currentBin], currentEff, yBins[currentBin])
          #print "--------------"
          if (currentBin < (nBins+1) and currentEff < xBins[currentBin+1]):
            xBinsPlot.append(xBins[currentBin])
            yBinsPlot.append(yBins[currentBin])

        
        #print yBins
        #print len(yBins)

        #print "eff vs eff"
        #for i in range (0, len(xBinsPlot)):
        #  print "%f %f" %(xBinsPlot[i], yBinsPlot[i])

        #rocCurve = TGraph(len(xBins),xBins,yBins)
        rocCurve = TGraph(len(xBinsPlot),xBinsPlot,yBinsPlot)
        rocCurve.GetXaxis().SetTitle("%s efficiency"%Jet_flavours[flav1])
        rocCurve.GetYaxis().SetTitle("%s efficiency"%Jet_flavours[flav2])
        rocCurve.SetTitle("%s vs. %s, %s"%(Jet_flavours[flav1], Jet_flavours[flav2], PtBins[n]))
        rocCurve.SetName("ROC_%s_%s_%i"%(Jet_flavours[flav1], Jet_flavours[flav2],n))
        rocCurve.GetYaxis().SetRangeUser(0.0001,1.0);
        rocCurve.GetXaxis().SetLimits(0.,1.0);
        #TH1D("ROC_%s_%s"%(flav1, flav2), "ROC curve for %s vs. %s;%s efficiency;%s efficiency"%(flav1, flav2, flav1, flav2), 100, -1, 1)
        rocCurve.Draw("al")
        gPad.SetGridx(1)
        gPad.SetGridy(1)
        gPad.SetLogy()
        #canvas.SaveAs("%s/%s.png" %(outDirName, rocCurve.GetName()))
        rocCurve.Write()
      #break
  outFile.Close()        
  


def main():

  ROOT.gROOT.SetBatch(True)
  parallelProcesses = multiprocessing.cpu_count()
  
  # create Pool
  p = multiprocessing.Pool(parallelProcesses)
  print "Using %i parallel processes" %parallelProcesses
    
  #outDirName = './histos_witherror'
  outDirName = './Validation'
  inDirName = "./"
  fileList = []
  
  if not os.path.exists(outDirName):
    print "Creating new output directory: ", outDirName
    os.makedirs(outDirName)

  for inFileName in os.listdir(inDirName):
    if inFileName.endswith(".root") and inFileName.startswith("trainPlusBDTG_"):
      category = inFileName.replace("trainPlusBDTG_", "").split("_",1)[0]
      Jet_flavour = inFileName.replace("trainPlusBDTG_", "").split("_",2)[1]
      key = "%s_%s" %(category, Jet_flavour)
      print key
      fileList.append(inFileName.replace(".root", "_Histograms.root"))
      # processNtuple(inFileName, inDirName, outDirName)
      # break
      p.apply_async(processNtuple, args = (inFileName, inDirName, outDirName,))

  p.close()
  p.join()


  # loop over all output files of one category and Jet_flavour and hadd them
  outDirName = os.path.join(os.path.abspath(sys.path[0]), outDirName) # absolute path to be safe
  print "hadding key files"
  haddList = ""
  for fileName in fileList:
    haddList += "%s " %fileName
  haddCommand = "pwd && hadd -f AllHistograms.root %s" %(haddList)
  # print haddCommand
  lock=thread.allocate_lock()
  lock.acquire()
  haddProcess=subprocess.Popen(haddCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=outDirName)
  haddProcess.wait()
  lock.release()
  errors = haddProcess.stderr.read()
  if ( len(errors) > 0):
    print "WARNING, there has been an error!"
    print errors
  print haddProcess.stdout.read()
  # delete split files
  # for fileName in fileList:
  #   print "deleting %s/%s"%(outDirName, fileName)
  #   os.remove("%s/%s"%(outDirName, fileName))
  haddCommand_ = "pwd && hadd -f AllHistograms_CSVIVF.root %s" %(haddList)
  lock_=thread.allocate_lock()
  lock_.acquire()
  haddProcess_=subprocess.Popen(haddCommand_, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=outDirName)
  haddProcess_.wait()
  lock_.release()
  errors_ = haddProcess_.stderr.read()
  if ( len(errors_) > 0):
    print "WARNING, there has been an error!"
    print errors_
  print haddProcess_.stdout.read()
  
  makeROCCurves(outDirName)
  makeROCCurves_CSVIVF(outDirName)
  

if __name__ == "__main__":
  main()
