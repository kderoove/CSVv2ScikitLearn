import ROOT
import os
import multiprocessing
import array



# LR training variables
training_vars_float = [
  'Jet_pt',
  'Jet_eta',
  'TagVarCSV_jetNTracks',
  'TagVarCSV_trackSip3dSig_0',
  'TagVarCSV_trackSip3dSig_1',
  'TagVarCSV_trackSip3dSig_2',
  'TagVarCSV_trackSip3dSig_3',
  'TagVarCSV_trackSip3dSigAboveCharm',
	'TagVarCSV_trackPtRel_0',
	'TagVarCSV_trackPtRel_1',
	'TagVarCSV_trackPtRel_2',
	'TagVarCSV_trackPtRel_3',
	'TagVarCSV_trackEtaRel_0',
	'TagVarCSV_trackEtaRel_1',
	'TagVarCSV_trackEtaRel_2',
	'TagVarCSV_trackEtaRel_3',
	'TagVarCSV_trackDeltaR_0',
	'TagVarCSV_trackDeltaR_1',
	'TagVarCSV_trackDeltaR_2',
	'TagVarCSV_trackDeltaR_3',
	'TagVarCSV_trackPtRatio_0',
	'TagVarCSV_trackPtRatio_1',
	'TagVarCSV_trackPtRatio_2',
	'TagVarCSV_trackPtRatio_3',
	'TagVarCSV_trackJetDist_0',
	'TagVarCSV_trackJetDist_1',
	'TagVarCSV_trackJetDist_2',
	'TagVarCSV_trackJetDist_3',
	'TagVarCSV_trackDecayLenVal_0',
	'TagVarCSV_trackDecayLenVal_1',
	'TagVarCSV_trackDecayLenVal_2',
  'TagVarCSV_trackDecayLenVal_3',
  'TagVarCSV_trackSumJetEtRatio',
  'TagVarCSV_trackSumJetDeltaR',
  'TagVarCSV_vertexMass',
  'TagVarCSV_vertexNTracks',
  'TagVarCSV_vertexEnergyRatio',
  'TagVarCSV_vertexJetDeltaR',
  'TagVarCSV_flightDistance2dSig',
  'TagVarCSV_jetNSecondaryVertices',
]


def train(bdtoptions):
  
  TMVA_tools = ROOT.TMVA.Tools.Instance()

  tree = ROOT.TChain('tree')

 
  files = [
"/user/kderoove/bTagging/MoveCSVv2ToMVApackage/ScikitLearn/data_trees/flat_trees/qcd/flat_skimmed_20k_eachptetabin_CombinedSVRecoVertex_B.root",
"/user/kderoove/bTagging/MoveCSVv2ToMVApackage/ScikitLearn/data_trees/flat_trees/qcd/flat_skimmed_20k_eachptetabin_CombinedSVPseudoVertex_B.root",
"/user/kderoove/bTagging/MoveCSVv2ToMVApackage/ScikitLearn/data_trees/flat_trees/qcd/flat_skimmed_20k_eachptetabin_CombinedSVNoVertex_B.root",
"/user/kderoove/bTagging/MoveCSVv2ToMVApackage/ScikitLearn/data_trees/flat_trees/qcd/flat_skimmed_20k_eachptetabin_CombinedSVRecoVertex_C.root",
"/user/kderoove/bTagging/MoveCSVv2ToMVApackage/ScikitLearn/data_trees/flat_trees/qcd/flat_skimmed_20k_eachptetabin_CombinedSVPseudoVertex_C.root",
"/user/kderoove/bTagging/MoveCSVv2ToMVApackage/ScikitLearn/data_trees/flat_trees/qcd/flat_skimmed_20k_eachptetabin_CombinedSVNoVertex_C.root",
"/user/kderoove/bTagging/MoveCSVv2ToMVApackage/ScikitLearn/data_trees/flat_trees/qcd/flat_skimmed_20k_eachptetabin_CombinedSVRecoVertex_DUSG.root",
"/user/kderoove/bTagging/MoveCSVv2ToMVApackage/ScikitLearn/data_trees/flat_trees/qcd/flat_skimmed_20k_eachptetabin_CombinedSVPseudoVertex_DUSG.root",
"/user/kderoove/bTagging/MoveCSVv2ToMVApackage/ScikitLearn/data_trees/flat_trees/qcd/flat_skimmed_20k_eachptetabin_CombinedSVNoVertex_DUSG.root"
    ]
  
  for f in files:
      print 'Opening file %s' %f
      tree.Add('%s' %f)
  
  signal_selection = 'Jet_flavour==5' # c
  background_selection = 'Jet_flavour!=5' # no c and no b --> DUSG

  num_pass = tree.GetEntries(signal_selection)
  num_fail = tree.GetEntries(background_selection)

  print 'N events signal', num_pass
  print 'N events background', num_fail
  outFile = ROOT.TFile('TMVA_classification.root', 'RECREATE')

  factory = ROOT.TMVA.Factory(
                               "TMVAClassification", 
                               outFile, 
                               "!V:!Silent:Color:DrawProgressBar:Transformations=I"
                             ) 

  for var in training_vars_float:
    factory.AddVariable(var, 'F') # add float variable
  for var in training_vars_int:
    factory.AddVariable(var, 'I') # add integer variable

  factory.SetWeightExpression('weight')

  factory.AddSignalTree(tree, 1.)
  factory.AddBackgroundTree(tree, 1.)

  # import pdb; pdb.set_trace()

  factory.PrepareTrainingAndTestTree( ROOT.TCut(signal_selection), ROOT.TCut(background_selection),
                                      "nTrain_Signal=0:nTest_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )

  
  factory.BookMethod( ROOT.TMVA.Types.kBDT,
                      "BDTG",
                      # "!H:!V:NTrees=1000:BoostType=Grad:Shrinkage=0.05:UseBaggedGrad:GradBaggingFraction=0.9:SeparationType=GiniIndex:nCuts=500:NNodesMax=5"
                      ":".join(bdtoptions)
                    )

  factory.TrainAllMethods()

  # factory.OptimizeAllMethods()

  factory.TestAllMethods()

  factory.EvaluateAllMethods()

  outFile.Close()

##   ROOT.gROOT.LoadMacro('$ROOTSYS/tmva/test/TMVAGui.C')
##   ROOT.TMVAGui('TMVA_classification.root')
##   raw_input("Press Enter to continue...")


def trainMultiClass():

  classes = [
    ('Jet_flavour==5', 'B'),
    ('Jet_flavour==4', 'C'),
    ('Jet_flavour!=5 && Jet_flavour!=4', 'DUSG')
  ]

  for cl in classes:
    print 'N events', cl[1], tree.GetEntries(cl[0])

  outFile = ROOT.TFile('TMVA_multiclass.root', 'RECREATE')

  factory = ROOT.TMVA.Factory(
        "TMVAClassification", 
        outFile, 
        "!V:!Silent:Color:DrawProgressBar:Transformations=I:AnalysisType=Multiclass" ) 

  for var in training_vars_float:
    factory.AddVariable(var, 'F') # add float variable
  for var in training_vars_int:
    factory.AddVariable(var, 'I') # add integer variable

  # factory.SetWeightExpression('')

  for cl in classes:
    factory.AddTree(tree, cl[1], 1., ROOT.TCut(cl[0]))
  # factory.AddSignalTree(tree, 1.)
  # factory.AddBackgroundTree(tree, 1.)

  # import pdb; pdb.set_trace()

  factory.PrepareTrainingAndTestTree( ROOT.TCut(''), ROOT.TCut(''),  "SplitMode=Random:NormMode=NumEvents:!V")

  factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDTG","!H:!V:NTrees=1000:BoostType=Grad:Shrinkage=0.05:UseBaggedGrad:GradBaggingFraction=0.9:SeparationType=GiniIndex:nCuts=500:NNodesMax=5" )

  # factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT_ADA", "!H:!V:NTrees=400:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=50:AdaBoostBeta=0.2:MaxDepth=2:MinNodeSize=6")

  factory.TrainAllMethods()

  # factory.OptimizeAllMethods()

  factory.TestAllMethods()

  factory.EvaluateAllMethods()

  outFile.Close()

 #ROOT.gROOT.LoadMacro('$ROOTSYS/tmva/test/TMVAMultiClassGui.C')
 #ROOT.TMVAMultiClassGui('TMVA_multiclass.root')
 #raw_input("Press Enter to continue...")



def read(inDirName, inFileName):
  
  print "Reading", inFileName
  
  TMVA_tools = ROOT.TMVA.Tools.Instance()

  tree = ROOT.TChain('ttree')

  tree.Add('%s/%s' %(inDirName, inFileName))

  reader = ROOT.TMVA.Reader('TMVAClassification_BDTG')

  varDict = {}
  for var in training_vars_float:
    varDict[var] = array.array('f',[0])
    reader.AddVariable(var, varDict[var])


  reader.BookMVA("BDTG","TMVAClassification_BDTG.weights.xml")

  bdtOuts = []
  flavours = []
  categories = []
  jetPts = []
  jetEtas = []

  for jentry in xrange(tree.GetEntries()):
    if ((jentry%50) != 0): #skip every 200 events
    	continue
    ientry = tree.LoadTree(jentry)
    nb = tree.GetEntry(jentry)

    for var in varDict:
      varDict[var][0] = getattr(tree, var)

    bdtOutput = reader.EvaluateMVA("BDTG")
    Jet_flavour = tree.Jet_flavour
    bdtOuts.append(bdtOutput)
    flavours.append(Jet_flavour)
    categories.append(tree.TagVarCSV_vertexCategory)
    jetPts.append(tree.Jet_pt)
    jetEtas.append(tree.Jet_eta)

    if jentry%10000 == 0:
      print jentry, bdtOutput, Jet_flavour

  writeSmallTree = True

  if writeSmallTree:
    print "Writing small tree"

    BDTG = array.array('f',[0])
    flav = array.array('f',[0])
    cat = array.array('f',[0])
    Jet_pt = array.array('f',[0])
    Jet_eta = array.array('f',[0])
    Jet_CSVIVF = array.array('f',[0])

    fout = ROOT.TFile('trainPlusBDTG_%s.root'%(inFileName.replace(".root","")), 'RECREATE')
    outTree = ROOT.TTree( 'ttree', 'b-tagging training tree' )
    outTree.Branch('BDTG', BDTG, 'BDTG/F')
    outTree.Branch('Jet_flavour', flav, 'Jet_flavour/F')
    outTree.Branch('TagVarCSV_vertexCategory', cat, 'TagVarCSV_vertexCategory/F')
    outTree.Branch('Jet_pt', Jet_pt, 'Jet_pt/F')
    outTree.Branch('Jet_eta', Jet_eta, 'Jet_eta/F')
    outTree.Branch('Jet_CSVIVF', Jet_CSVIVF, 'Jet_CSVIVF/F')


    for i in range(len((bdtOuts))):
      BDTG[0] = bdtOuts[i]
      flav[0] = flavours[i]
      cat[0] = categories[i]
      Jet_pt[0] = jetPts[i]
      Jet_eta[0] = jetEtas[i]
      if i%10000==0:
        print i, bdtOuts[i], flavours[i]
      outTree.Fill()
      # treeout.Write()
    fout.Write()
    fout.Close()
  print "done", inFileName

def readParallel():

  print "start readParallel()"
  ROOT.gROOT.SetBatch(True)
  parallelProcesses = multiprocessing.cpu_count()
  
  inDirName="/user/kderoove/bTagging/MoveCSVv2ToMVApackage/ScikitLearn/FlatTrees_tt/"
  files = [
    "skimmed_20k_eachptetabin_CombinedSVNoVertex_B.root",
    "skimmed_20k_eachptetabin_CombinedSVNoVertex_C.root",
    "skimmed_20k_eachptetabin_CombinedSVNoVertex_DUSG.root",
    "skimmed_20k_eachptetabin_CombinedSVPseudoVertex_B.root",
    "skimmed_20k_eachptetabin_CombinedSVPseudoVertex_C.root",
    "skimmed_20k_eachptetabin_CombinedSVPseudoVertex_DUSG.root",
    "skimmed_20k_eachptetabin_CombinedSVRecoVertex_B.root",
    "skimmed_20k_eachptetabin_CombinedSVRecoVertex_C.root",
    "skimmed_20k_eachptetabin_CombinedSVRecoVertex_DUSG.root"
    ]
  #files ["CombinedSVNoVertex_B.root"]

  #for inFileName in os.listdir(inDirName):
  #  if inFileName.endswith(".root") and not (inFileName.find("Eta") >= 0):
  #    files.append(inFileName)

  # create Pool
  p = multiprocessing.Pool(parallelProcesses)
  print "Using %i parallel processes" %parallelProcesses

  for f in files:
    # debug
     read(inDirName, f)
    # break
    # run jobs
    #p.apply_async(read, args = (inDirName, f,))

  p.close()
  p.join()
    


if __name__ == '__main__':
    bdtoptions = [ "!H",
                                 "!V",
                                 "NTrees=2000",
                                 "MinNodeSize=5%",
                                 "BoostType=Grad",
                                 "Shrinkage=0.50",
                                 "UseBaggedGrad",
                                 "GradBaggingFraction=0.3",
                                 "nCuts=50",
                                 "MaxDepth=8",
                               ]
    #train(bdtoptions)
    # trainMultiClass()
    readParallel()

