import os
import re
import rootpy.io as io
import rootpy
import rootpy.tree as tr
from ROOT import TH1D
import numpy as np
np.set_printoptions(precision=5)
import root_numpy as rootnp
from sklearn.externals import joblib
log = rootpy.log["/toy_diagnostics"]
log.setLevel(rootpy.log.INFO)



#################################
#				#
# 	Training		#
#				#
#################################

variables = [
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


input_files = [i.strip() for i in open('../data_trees/inputs/qcd_flat.list')] #Make sure there are no empty lines in .list
flavors = ['B', 'C', 'DUSG']
sv_categories = ["RecoVertex", "PseudoVertex", "NoVertex"]
fname_regex = re.compile('[a-zA-Z_0-9\/]*\/?[a-zA-Z_0-9]+_(?P<category>[a-zA-Z]+)_(?P<flavor>[A-Z]+)\.root')

print 'Merging and converting the samples'
X = np.ndarray((0,len(variables)),float) # container to hold the combined trees in numpy array structure
y = np.ones(0) # container to hold the truth signal(1) or background(0) information
weights_flavour = np.ones(0) # container to hold the truth signal(1) or background(0) information
weights_JetPtEta = np.ones(0) # container holding the weights for each of the jets
weights_cat = np.ones(0) # container holding the weights for each of the jets
weights = np.ones(0) # container holding the weights for each of the jets
for fname in input_files:
   log.info('processing file %s for training' % fname)
   with io.root_open(fname) as tfile:
      match = fname_regex.match(fname)
      if not match:
         raise ValueError("Could not match the regex to the file %s" % fname)
      flavor = match.group('flavor')
      full_category = match.group('category')
      category = [i for i in sv_categories if i in full_category][0]
#      if flavor == 'C':
#      	log.info('Jet_flavour %s is not considered signal or background in this training and is omitted' % flavor) 
#	continue

      nfiles_per_sample = None
      skip_n_events = 2 # put this to 1 to include all the events
      tree = rootnp.root2array(fname,'ttree',variables,None,0,nfiles_per_sample,skip_n_events,False,'weight')
      tree = rootnp.rec2array(tree)
      X = np.concatenate((X, tree),0)
      if flavor == "B":
      	y = np.concatenate((y,np.ones(tree.shape[0])))
        weight_B = np.empty(tree.shape[0])
        weight_B.fill(2)
        weights_flavour = np.concatenate((weights_flavour,weight_B))
      elif flavor == "C":
      	y = np.concatenate((y,np.zeros(tree.shape[0])))
        weight_C = np.empty(tree.shape[0])
        weight_C.fill(1)
        weights_flavour = np.concatenate((weights_flavour,weight_C))
      else:
      	y = np.concatenate((y,np.zeros(tree.shape[0])))
        weight_DUSG = np.empty(tree.shape[0])
        weight_DUSG.fill(3)
        weights_flavour = np.concatenate((weights_flavour,weight_DUSG))
   
      # Getting the weights out
      weights_tree_JetPtEta = rootnp.root2array(fname,'ttree','weight_etaPt',None,0,nfiles_per_sample,skip_n_events,False,'weight')
      weights_JetPtEta = np.concatenate((weights_JetPtEta,weights_tree_JetPtEta),0)#Weights according to the JetPtEta
      
      weights_tree_cat = rootnp.root2array(fname,'ttree','weight_category',None,0,nfiles_per_sample,skip_n_events,False,'weight')
      weights_cat = np.concatenate((weights_cat,weights_tree_cat),0)#Weights according to the category

      weights = np.multiply(weights_JetPtEta,weights_cat,weights_flavour)


print 'Starting training'
import time	
#from sklearn.ensemble import RandomForestClassifier 
min_frac_samples_split = 0.006
#clf = RandomForestClassifier(n_estimators=1000,min_samples_split = int(min_frac_samples_split*y.shape[0]), n_jobs = 5, verbose = 3)
from sklearn.ensemble import GradientBoostingClassifier
#clf = GradientBoostingClassifier(n_estimators=500, max_depth=15, min_samples_split=0.006*len(X), learning_rate=0.05)
clf = GradientBoostingClassifier(n_estimators=500,min_samples_split = int(min_frac_samples_split*y.shape[0]), learning_rate = 0.05, max_depth=15, verbose = 3)
start = time.time()
clf.fit(X, y,weights)
end = time.time()
print 'training completed --> Elapsed time: ' , (end-start)/60 ,  'minutes'

#training_file = './trainingFiles/MVATraining.pkl'
#print 'Dumping training file in: ' + training_file
#joblib.dump(clf, training_file,protocol = HIGHEST_PROTOCOL) 


#######################################
## Converting to TMVA readable xml file
#######################################

import sklearn_to_tmva as convert
trainingWeights_TMVA = 'TMVAClassification_BDTG.weights.xml'
log.info('Dumping training file in: ' + trainingWeights_TMVA)
# *** Sklearn(python)-type training file (.pkl) ***
#joblib.dump(clf, trainingWeights_TMVA, compress=True)
# *** TMVA-style training file (.xml) ***
out_ext = (trainingWeights_TMVA).split('.')[-1]
convert.gbr_to_tmva(clf,X,trainingWeights_TMVA,mva_name = "BDTG",coef = 10, var_names = variables)

#################################
#				#
# 	Validation		#
#				#
#################################

#input_files = [i.strip() for i in open('data_trees/inputs/ttjets.list')]
input_files = [i.strip() for i in open('../data_trees/inputs/ttjets.list')] #Make sure there are no empty lines in .list
pt_bins = [15, 40, 60, 90, 150, 400, 600]
eta_bins = [1.2, 2.1]
#flavors = ['C', 'B', 'DUSG']
#sv_categories = ["NoVertex", "PseudoVertex", "RecoVertex"]
fname_regex = re.compile('[a-zA-Z_0-9\/]*\/?[a-zA-Z_0-9]+_(?P<category>[a-zA-Z]+)_(?P<flavor>[A-Z]+)\.root')

# you can reload the training if needed (or if you only want to do a validation on an existing training)
# but it is much faster to use the still existing classifier from the training

'''
#training_file = './training_file/MVATraining.pkl'
print 'Loading training file from: ' + training_file
clf_val = joblib.load(training_file)
'''
clf_val = clf

for fname in input_files:
   log.info('processing file %s' % fname)
   with io.root_open(fname) as tfile:
      match = fname_regex.match(fname)
      if not match:
         raise ValueError("Could not match the regex to the file %s" % fname)
      flavor = match.group('flavor')
      full_category = match.group('category')
      category = [i for i in sv_categories if i in full_category][0]
      
      nfiles_per_sample = None
      skip_n_events = 50 # put this to 1 to include all the events
      X_val = rootnp.root2array(fname,'ttree',variables,None,0,nfiles_per_sample,skip_n_events,False,'weight')
      X_val = rootnp.rec2array(X_val)
      BDTG =  clf_val.predict_proba(X_val)[:,1]
      
      Output_variables = ['Jet_flavour','TagVarCSV_vertexCategory','Jet_pt','Jet_eta','Jet_CSVIVF']
      Output_tree = rootnp.root2array(fname,'ttree',Output_variables,None,0,nfiles_per_sample,skip_n_events,False,'weight')
      Output_tree = rootnp.rec2array(Output_tree)

      Output_tree_final = np.ndarray((Output_tree.shape[0],),dtype=[('Jet_flavour', float), ('TagVarCSV_vertexCategory', float), ('Jet_pt', float), ('Jet_eta', float),('Jet_CSVIVF', float), ('BDTG', float)])#, buffer = np.array([1,2,3,4,5]))
      for idx,val in enumerate(BDTG):
       Output_tree_final[idx][0] = Output_tree[idx][0]
       Output_tree_final[idx][1] = Output_tree[idx][1]
       Output_tree_final[idx][2] = Output_tree[idx][2]
       Output_tree_final[idx][3] = Output_tree[idx][3]
       Output_tree_final[idx][4] = Output_tree[idx][4]
       Output_tree_final[idx][5] = BDTG[idx]
       
      Output_tree_final = Output_tree_final.view(np.recarray)
      tree = rootnp.array2root(Output_tree_final, 'trainPlusBDTG_CombinedSV'+category+'_'+flavor+'.root', 'ttree','recreate') 
      log.info('Output file dumped in trainPlusBDTG_CombinedSV'+category+'_'+flavor+'.root')   
      
log.info('done')
