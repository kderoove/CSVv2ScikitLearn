#include <string>         // std::string
#include <vector>

void Filter_qcd() {
//void Filter(string filename="", string Treename="") {
// Example of Root macro based on $ROOTSYS/tutorials/tree/copytree3.C
   
  gSystem->Load("$ROOTSYS/test/libEvent");

    string inputname = "/user/kderoove/bTagging/MoveCSVv2ToMVApackage/CMSSW_7_4_14/src/RecoBTag/TagVarExtractor/test/JetTaggingVariables_QCD_76X.root";
    string treename  = "tagVars/ttree";
//    string inputname = filename;
//    string treename  = Treename;
    bool debug = false;

	Int_t max_nb_ofjets	=20000;
	Float_t ptbins[] = {15,40,60,90,150,400,600,10000};
	Float_t etabins[] = {0,1.2,2.1,2.4};

  
	//Get old file, old tree and set top branch address
  	TString name = inputname.c_str();
    TFile *oldfile = new TFile(name);
  	TTree *oldtree = (TTree*)oldfile->Get(treename.c_str()); //CombinedSVV2NoVertex, CombinedSVV2RecoVertex, CombinedSVV2PseudoVertex
  	Int_t nentries = (Int_t)oldtree->GetEntries();

    cout << "There are " << nentries << " jets in the file " << inputname << " will select maximally " << max_nb_ofjets << " in each pt/eta bin per flavour and vtx category" << endl;
   
  	Float_t flavour_f, vtxCat_f, jetNTracks;
  	Float_t trackPtRel_0;
  	Float_t jetpt, jeteta, jetgenpt;
  	flavour_f = -1;
  	vtxCat_f = -1;
  	jetNTracks = -1;
  	trackPtRel_0 = -1;
  	jetpt = -1;
  	jeteta = -1;
  	jetgenpt = -1;
  	oldtree->SetBranchAddress("Jet_flavour",&flavour_f);
  	oldtree->SetBranchAddress("Jet_pt",&jetpt);
  	oldtree->SetBranchAddress("Jet_genpt",&jetgenpt);
  	oldtree->SetBranchAddress("Jet_eta",&jeteta);
  	oldtree->SetBranchAddress("TagVarCSV_vertexCategory",&vtxCat_f);
  	oldtree->SetBranchAddress("TagVarCSV_jetNTracks",&jetNTracks);
  	oldtree->SetBranchAddress("TagVarCSV_trackPtRel_0",&trackPtRel_0);

  	//Create a new file + a clone of old tree in new file
	vector<TTree*> newtree_B;
	vector<TTree*> newtree_C;
	vector<TTree*> newtree_DUSG;
    Int_t nbOfjets_B[3][19], nbOfjets_C[3][19], nbOfjetsKept_B[3][19], nbOfjetsKept_C[3][19];
    Int_t nbOfjets_DUS[3][19],nbOfjetsKept_DUS[3][19];
    Int_t nbOfjets_G[3][19],nbOfjetsKept_G[3][19];

    for(unsigned int i=0; i<3; i++)//Define for different VtxCategories
    {
	    for(int j = 0 ; j<19 ; j++){
		    nbOfjets_B[i][j]=0;
		    nbOfjetsKept_B[i][j]=0;
		    nbOfjets_C[i][j]=0;
		    nbOfjetsKept_C[i][j]=0;
		    nbOfjets_DUS[i][j]=0;
		    nbOfjetsKept_DUS[i][j]=0;
		    nbOfjets_G[i][j]=0;
		    nbOfjetsKept_G[i][j]=0;
	    }
	}

	TFile *newfile_VertexCatMinusOne = new TFile("../SkimmedTrees/VertexCatMinusOne.root","RECREATE");
  	TTree *newtree_VertexCatMinusOne = oldtree->CloneTree(0);
	TFile *newfile_PU = new TFile("../SkimmedTrees/PU.root","RECREATE");
  	TTree *newtree_PU = oldtree->CloneTree(0);

	
	TFile *newfile_RecoVertex_B = new TFile("../SkimmedTrees/skimmed_20k_eachptetabin_CombinedSVRecoVertex_B.root","RECREATE");
  	TTree *newtree_RecoVertex_B = oldtree->CloneTree(0);
  	newtree_B.push_back(newtree_RecoVertex_B);
	TFile *newfile_RecoVertex_C = new TFile("../SkimmedTrees/skimmed_20k_eachptetabin_CombinedSVRecoVertex_C.root","RECREATE");
  	TTree *newtree_RecoVertex_C = oldtree->CloneTree(0);
  	newtree_C.push_back(newtree_RecoVertex_C);
	TFile *newfile_RecoVertex_DUSG = new TFile("../SkimmedTrees/skimmed_20k_eachptetabin_CombinedSVRecoVertex_DUSG.root","RECREATE");
  	TTree *newtree_RecoVertex_DUSG = oldtree->CloneTree(0);
  	newtree_DUSG.push_back(newtree_RecoVertex_DUSG);
	TFile *newfile_PseudoVertex_B = new TFile("../SkimmedTrees/skimmed_20k_eachptetabin_CombinedSVPseudoVertex_B.root","RECREATE");
  	TTree *newtree_PseudoVertex_B = oldtree->CloneTree(0);
  	newtree_B.push_back(newtree_PseudoVertex_B);
	TFile *newfile_PseudoVertex_C = new TFile("../SkimmedTrees/skimmed_20k_eachptetabin_CombinedSVPseudoVertex_C.root","RECREATE");
  	TTree *newtree_PseudoVertex_C = oldtree->CloneTree(0);
  	newtree_C.push_back(newtree_PseudoVertex_C);
	TFile *newfile_PseudoVertex_DUSG = new TFile("../SkimmedTrees/skimmed_20k_eachptetabin_CombinedSVPseudoVertex_DUSG.root","RECREATE");
  	TTree *newtree_PseudoVertex_DUSG = oldtree->CloneTree(0);
  	newtree_DUSG.push_back(newtree_PseudoVertex_DUSG);
	TFile *newfile_NoVertex_B = new TFile("../SkimmedTrees/skimmed_20k_eachptetabin_CombinedSVNoVertex_B.root","RECREATE");
  	TTree *newtree_NoVertex_B = oldtree->CloneTree(0);
  	newtree_B.push_back(newtree_NoVertex_B);
	TFile *newfile_NoVertex_C = new TFile("../SkimmedTrees/skimmed_20k_eachptetabin_CombinedSVNoVertex_C.root","RECREATE");
  	TTree *newtree_NoVertex_C = oldtree->CloneTree(0);
  	newtree_C.push_back(newtree_NoVertex_C);
	TFile *newfile_NoVertex_DUSG = new TFile("../SkimmedTrees/skimmed_20k_eachptetabin_CombinedSVNoVertex_DUSG.root","RECREATE");
  	TTree *newtree_NoVertex_DUSG = oldtree->CloneTree(0);
  	newtree_DUSG.push_back(newtree_NoVertex_DUSG);


	for (Int_t i=0;i<nentries; i++)
	{
	    oldtree->GetEntry(i);
	    int flavour = int(flavour_f);
	    int vtxCat = int(vtxCat_f);
        if(debug)
        {
    	    cout << "JetPt: " << jetpt << endl;
    	    cout << "Jet_genPt: " << jetgenpt << endl;
    	    cout << "JetEtat: " << jeteta << endl;
    	    cout << "JetFlavour: " << flavour << endl;
    	    cout << "VtxCat: " << vtxCat << endl;
        }
        if(jetNTracks<2) continue;			
        if(trackPtRel_0 != trackPtRel_0) continue;

        if(vtxCat == -1) //For now skip events with vtxCat=-1 for further understanding
        {
            newtree_VertexCatMinusOne->Fill();
            continue;
        }
        else if(abs(flavour)<=0 && jetgenpt<8.)//This should rule out any PU jets
        {
            newtree_PU->Fill();
            continue;
        }
        else if((abs(flavour)>3 && flavour!=21) && jetgenpt<8.)//This should rule out any PU jets
        {
            newtree_PU->Fill();
            continue;
        }

		if(flavour < 21 && fabs(flavour) != 5 && fabs(flavour) != 4) //DUS jets
		{  
	        if((jetpt>=ptbins[0] && jetpt<ptbins[1]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_DUS[vtxCat][0]++;
				if(nbOfjets_DUS[vtxCat][0]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][0]++;}
			}
			else if((jetpt>=ptbins[0] && jetpt<ptbins[1]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
				nbOfjets_DUS[vtxCat][1]++;
				if(nbOfjets_DUS[vtxCat][1]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][1]++;}
			}
			else if((jetpt>=ptbins[0] && jetpt<ptbins[1]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_DUS[vtxCat][2]++;
				if(nbOfjets_DUS[vtxCat][2]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][2]++;}
	  		}
	  		else if((jetpt>=ptbins[1] && jetpt<ptbins[2]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
	  		{
				nbOfjets_DUS[vtxCat][3]++;
				if(nbOfjets_DUS[vtxCat][3]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][3]++;}
			}
			else if((jetpt>=ptbins[1] && jetpt<ptbins[2]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
				nbOfjets_DUS[vtxCat][4]++;
				if(nbOfjets_DUS[vtxCat][4]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][4]++;}
			}
			else if((jetpt>=ptbins[1] && jetpt<ptbins[2]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_DUS[vtxCat][5]++;
				if(nbOfjets_DUS[vtxCat][5]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][5]++;}
		  	}
		  	else if((jetpt>=ptbins[2] && jetpt<ptbins[3]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
		  	{
				nbOfjets_DUS[vtxCat][6]++;
				if(nbOfjets_DUS[vtxCat][6]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][6]++;}
			}
			else if((jetpt>=ptbins[2] && jetpt<ptbins[3]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
				nbOfjets_DUS[vtxCat][7]++;
				if(nbOfjets_DUS[vtxCat][7]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][7]++;}
			}
			else if((jetpt>=ptbins[2] && jetpt<ptbins[3]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_DUS[vtxCat][8]++;
				if(nbOfjets_DUS[vtxCat][8]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][8]++;}
			}
			else if((jetpt>=ptbins[3] && jetpt<ptbins[4]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_DUS[vtxCat][9]++;
				if(nbOfjets_DUS[vtxCat][9]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][9]++;}
			}
			else if((jetpt>=ptbins[3] && jetpt<ptbins[4]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
			    nbOfjets_DUS[vtxCat][10]++;
				if(nbOfjets_DUS[vtxCat][10]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][10]++;}
			}
			else if((jetpt>=ptbins[3] && jetpt<ptbins[4]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_DUS[vtxCat][11]++;
				if(nbOfjets_DUS[vtxCat][11]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][11]++;}
			}
			else if((jetpt>=ptbins[4] && jetpt<ptbins[5]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_DUS[vtxCat][12]++;
				if(nbOfjets_DUS[vtxCat][12]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][12]++;}
			}
			else if((jetpt>=ptbins[4] && jetpt<ptbins[5]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
				nbOfjets_DUS[vtxCat][13]++;
				if(nbOfjets_DUS[vtxCat][13]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][13]++;}
			}
			else if((jetpt>=ptbins[4] && jetpt<ptbins[5]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_DUS[vtxCat][14]++;
				if(nbOfjets_DUS[vtxCat][14]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][14]++;}
			}
			else if((jetpt>=ptbins[5] && jetpt<ptbins[6]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_DUS[vtxCat][15]++;
				if(nbOfjets_DUS[vtxCat][15]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][15]++;}
			}
			else if((jetpt>=ptbins[5] && jetpt<ptbins[6]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_DUS[vtxCat][16]++;
				if(nbOfjets_DUS[vtxCat][16]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][16]++;}
			}
			else if((jetpt>=ptbins[6] && jetpt<ptbins[7]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_DUS[vtxCat][17]++;
				if(nbOfjets_DUS[vtxCat][17]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][17]++;}
			}
			else if((jetpt>=ptbins[6] && jetpt<ptbins[7]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_DUS[vtxCat][18]++;
				if(nbOfjets_DUS[vtxCat][18]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_DUS[vtxCat][18]++;}
			}				
	        if(debug) cout << "Passed DUS flavour" << endl;
		}

		else if(flavour >= 21)// g-jets
		{
	        if((jetpt>=ptbins[0] && jetpt<ptbins[1]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_G[vtxCat][0]++;
				if(nbOfjets_G[vtxCat][0]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][0]++;}
			}
			else if((jetpt>=ptbins[0] && jetpt<ptbins[1]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
				nbOfjets_G[vtxCat][1]++;
				if(nbOfjets_G[vtxCat][1]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][1]++;}
			}
			else if((jetpt>=ptbins[0] && jetpt<ptbins[1]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_G[vtxCat][2]++;
				if(nbOfjets_G[vtxCat][2]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][2]++;}
	  		}
	  		else if((jetpt>=ptbins[1] && jetpt<ptbins[2]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
	  		{
				nbOfjets_G[vtxCat][3]++;
				if(nbOfjets_G[vtxCat][3]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][3]++;}
			}
			else if((jetpt>=ptbins[1] && jetpt<ptbins[2]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
				nbOfjets_G[vtxCat][4]++;
				if(nbOfjets_G[vtxCat][4]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][4]++;}
			}
			else if((jetpt>=ptbins[1] && jetpt<ptbins[2]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_G[vtxCat][5]++;
				if(nbOfjets_G[vtxCat][5]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][5]++;}
		  	}
		  	else if((jetpt>=ptbins[2] && jetpt<ptbins[3]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
		  	{
				nbOfjets_G[vtxCat][6]++;
				if(nbOfjets_G[vtxCat][6]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][6]++;}
			}
			else if((jetpt>=ptbins[2] && jetpt<ptbins[3]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
				nbOfjets_G[vtxCat][7]++;
				if(nbOfjets_G[vtxCat][7]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][7]++;}
			}
			else if((jetpt>=ptbins[2] && jetpt<ptbins[3]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_G[vtxCat][8]++;
				if(nbOfjets_G[vtxCat][8]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][8]++;}
			}
			else if((jetpt>=ptbins[3] && jetpt<ptbins[4]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_G[vtxCat][9]++;
				if(nbOfjets_G[vtxCat][9]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][9]++;}
			}
			else if((jetpt>=ptbins[3] && jetpt<ptbins[4]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
			    nbOfjets_G[vtxCat][10]++;
				if(nbOfjets_G[vtxCat][10]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][10]++;}
			}
			else if((jetpt>=ptbins[3] && jetpt<ptbins[4]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_G[vtxCat][11]++;
				if(nbOfjets_G[vtxCat][11]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][11]++;}
			}
			else if((jetpt>=ptbins[4] && jetpt<ptbins[5]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_G[vtxCat][12]++;
				if(nbOfjets_G[vtxCat][12]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][12]++;}
			}
			else if((jetpt>=ptbins[4] && jetpt<ptbins[5]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
				nbOfjets_G[vtxCat][13]++;
				if(nbOfjets_G[vtxCat][13]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][13]++;}
			}
			else if((jetpt>=ptbins[4] && jetpt<ptbins[5]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_G[vtxCat][14]++;
				if(nbOfjets_G[vtxCat][14]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][14]++;}
			}
			else if((jetpt>=ptbins[5] && jetpt<ptbins[6]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_G[vtxCat][15]++;
				if(nbOfjets_G[vtxCat][15]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][15]++;}
			}
			else if((jetpt>=ptbins[5] && jetpt<ptbins[6]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_G[vtxCat][16]++;
				if(nbOfjets_G[vtxCat][16]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][16]++;}
			}
			else if((jetpt>=ptbins[6] && jetpt<ptbins[7]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_G[vtxCat][17]++;
				if(nbOfjets_G[vtxCat][17]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][17]++;}
			}
			else if((jetpt>=ptbins[6] && jetpt<ptbins[7]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_G[vtxCat][18]++;
				if(nbOfjets_G[vtxCat][18]<max_nb_ofjets){ newtree_DUSG[vtxCat]->Fill(); nbOfjetsKept_G[vtxCat][18]++;}
			}				
    	    if(debug) cout << "Passed G flavour" << endl;
		}
		
		else if(fabs(flavour) == 4)//C-jets
		{
	        if((jetpt>=ptbins[0] && jetpt<ptbins[1]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_C[vtxCat][0]++;
				if(nbOfjets_C[vtxCat][0]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][0]++;}
			}
			else if((jetpt>=ptbins[0] && jetpt<ptbins[1]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
				nbOfjets_C[vtxCat][1]++;
				if(nbOfjets_C[vtxCat][1]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][1]++;}
			}
			else if((jetpt>=ptbins[0] && jetpt<ptbins[1]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_C[vtxCat][2]++;
				if(nbOfjets_C[vtxCat][2]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][2]++;}
	  		}
	  		else if((jetpt>=ptbins[1] && jetpt<ptbins[2]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
	  		{
				nbOfjets_C[vtxCat][3]++;
				if(nbOfjets_C[vtxCat][3]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][3]++;}
			}
			else if((jetpt>=ptbins[1] && jetpt<ptbins[2]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
				nbOfjets_C[vtxCat][4]++;
				if(nbOfjets_C[vtxCat][4]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][4]++;}
			}
			else if((jetpt>=ptbins[1] && jetpt<ptbins[2]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_C[vtxCat][5]++;
				if(nbOfjets_C[vtxCat][5]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][5]++;}
		  	}
		  	else if((jetpt>=ptbins[2] && jetpt<ptbins[3]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
		  	{
				nbOfjets_C[vtxCat][6]++;
				if(nbOfjets_C[vtxCat][6]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][6]++;}
			}
			else if((jetpt>=ptbins[2] && jetpt<ptbins[3]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
				nbOfjets_C[vtxCat][7]++;
				if(nbOfjets_C[vtxCat][7]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][7]++;}
			}
			else if((jetpt>=ptbins[2] && jetpt<ptbins[3]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_C[vtxCat][8]++;
				if(nbOfjets_C[vtxCat][8]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][8]++;}
			}
			else if((jetpt>=ptbins[3] && jetpt<ptbins[4]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_C[vtxCat][9]++;
				if(nbOfjets_C[vtxCat][9]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][9]++;}
			}
			else if((jetpt>=ptbins[3] && jetpt<ptbins[4]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
			    nbOfjets_C[vtxCat][10]++;
				if(nbOfjets_C[vtxCat][10]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][10]++;}
			}
			else if((jetpt>=ptbins[3] && jetpt<ptbins[4]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_C[vtxCat][11]++;
				if(nbOfjets_C[vtxCat][11]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][11]++;}
			}
			else if((jetpt>=ptbins[4] && jetpt<ptbins[5]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_C[vtxCat][12]++;
				if(nbOfjets_C[vtxCat][12]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][12]++;}
			}
			else if((jetpt>=ptbins[4] && jetpt<ptbins[5]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
				nbOfjets_C[vtxCat][13]++;
				if(nbOfjets_C[vtxCat][13]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][13]++;}
			}
			else if((jetpt>=ptbins[4] && jetpt<ptbins[5]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_C[vtxCat][14]++;
				if(nbOfjets_C[vtxCat][14]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][14]++;}
			}
			else if((jetpt>=ptbins[5] && jetpt<ptbins[6]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_C[vtxCat][15]++;
				if(nbOfjets_C[vtxCat][15]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][15]++;}
			}
			else if((jetpt>=ptbins[5] && jetpt<ptbins[6]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_C[vtxCat][16]++;
				if(nbOfjets_C[vtxCat][16]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][16]++;}
			}
			else if((jetpt>=ptbins[6] && jetpt<ptbins[7]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_C[vtxCat][17]++;
				if(nbOfjets_C[vtxCat][17]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][17]++;}
			}
			else if((jetpt>=ptbins[6] && jetpt<ptbins[7]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_C[vtxCat][18]++;
				if(nbOfjets_C[vtxCat][18]<max_nb_ofjets){ newtree_C[vtxCat]->Fill(); nbOfjetsKept_C[vtxCat][18]++;}
			}				
    	    if(debug) cout << "Passed C flavour" << endl;
		}

		else if(fabs(flavour) == 5)//B-jets
		{
	        if((jetpt>=ptbins[0] && jetpt<ptbins[1]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_B[vtxCat][0]++;
				if(nbOfjets_B[vtxCat][0]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][0]++;}
			}
			else if((jetpt>=ptbins[0] && jetpt<ptbins[1]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
				nbOfjets_B[vtxCat][1]++;
				if(nbOfjets_B[vtxCat][1]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][1]++;}
			}
			else if((jetpt>=ptbins[0] && jetpt<ptbins[1]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_B[vtxCat][2]++;
				if(nbOfjets_B[vtxCat][2]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][2]++;}
	  		}
	  		else if((jetpt>=ptbins[1] && jetpt<ptbins[2]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
	  		{
				nbOfjets_B[vtxCat][3]++;
				if(nbOfjets_B[vtxCat][3]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][3]++;}
			}
			else if((jetpt>=ptbins[1] && jetpt<ptbins[2]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
				nbOfjets_B[vtxCat][4]++;
				if(nbOfjets_B[vtxCat][4]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][4]++;}
			}
			else if((jetpt>=ptbins[1] && jetpt<ptbins[2]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_B[vtxCat][5]++;
				if(nbOfjets_B[vtxCat][5]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][5]++;}
		  	}
		  	else if((jetpt>=ptbins[2] && jetpt<ptbins[3]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
		  	{
				nbOfjets_B[vtxCat][6]++;
				if(nbOfjets_B[vtxCat][6]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][6]++;}
			}
			else if((jetpt>=ptbins[2] && jetpt<ptbins[3]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
				nbOfjets_B[vtxCat][7]++;
				if(nbOfjets_B[vtxCat][7]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][7]++;}
			}
			else if((jetpt>=ptbins[2] && jetpt<ptbins[3]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_B[vtxCat][8]++;
				if(nbOfjets_B[vtxCat][8]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][8]++;}
			}
			else if((jetpt>=ptbins[3] && jetpt<ptbins[4]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_B[vtxCat][9]++;
				if(nbOfjets_B[vtxCat][9]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][9]++;}
			}
			else if((jetpt>=ptbins[3] && jetpt<ptbins[4]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
			    nbOfjets_B[vtxCat][10]++;
				if(nbOfjets_B[vtxCat][10]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][10]++;}
			}
			else if((jetpt>=ptbins[3] && jetpt<ptbins[4]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_B[vtxCat][11]++;
				if(nbOfjets_B[vtxCat][11]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][11]++;}
			}
			else if((jetpt>=ptbins[4] && jetpt<ptbins[5]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_B[vtxCat][12]++;
				if(nbOfjets_B[vtxCat][12]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][12]++;}
			}
			else if((jetpt>=ptbins[4] && jetpt<ptbins[5]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[2]))
			{
				nbOfjets_B[vtxCat][13]++;
				if(nbOfjets_B[vtxCat][13]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][13]++;}
			}
			else if((jetpt>=ptbins[4] && jetpt<ptbins[5]) && (fabs(jeteta)>=etabins[2] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_B[vtxCat][14]++;
				if(nbOfjets_B[vtxCat][14]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][14]++;}
			}
			else if((jetpt>=ptbins[5] && jetpt<ptbins[6]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_B[vtxCat][15]++;
				if(nbOfjets_B[vtxCat][15]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][15]++;}
			}
			else if((jetpt>=ptbins[5] && jetpt<ptbins[6]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_B[vtxCat][16]++;
				if(nbOfjets_B[vtxCat][16]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][16]++;}
			}
			else if((jetpt>=ptbins[6] && jetpt<ptbins[7]) && (fabs(jeteta)>=etabins[0] && fabs(jeteta)<etabins[1]))
			{
				nbOfjets_B[vtxCat][17]++;
				if(nbOfjets_B[vtxCat][17]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][17]++;}
			}
			else if((jetpt>=ptbins[6] && jetpt<ptbins[7]) && (fabs(jeteta)>=etabins[1] && fabs(jeteta)<etabins[3]))
			{
				nbOfjets_B[vtxCat][18]++;
				if(nbOfjets_B[vtxCat][18]<max_nb_ofjets){ newtree_B[vtxCat]->Fill(); nbOfjetsKept_B[vtxCat][18]++;}
			}				
    	    if(debug) cout << "Passed B flavour" << endl;
		}
		
	}
	
	for(unsigned int i=0; i<3; i++)
	{
	    int Total_B = 0;
	    int Total_C = 0;
	    int Total_DUS = 0;
	    int Total_G = 0;

		for(int j = 0 ; j<19 ; j++)
		{
		    Total_B = Total_B+nbOfjets_B[i][j];
		    Total_C = Total_C+nbOfjets_C[i][j];
		    Total_DUS = Total_DUS+nbOfjets_DUS[i][j];
		    Total_G = Total_G+nbOfjets_G[i][j];
			cout << "Jetflavour B in VertexCategory " << i << " has " << nbOfjets_B[i][j] << " in pt/eta-bin " << j << " and we keep " << nbOfjetsKept_B[i][j] << endl;
			cout << "Jetflavour C in VertexCategory " << i << " has " << nbOfjets_C[i][j] << " in pt/eta-bin " << j << " and we keep " << nbOfjetsKept_C[i][j] << endl;
			cout << "Jetflavour DUS in VertexCategory " << i << " has " << nbOfjets_DUS[i][j] << " in pt/eta-bin " << j << " and we keep " << nbOfjetsKept_DUS[i][j] << endl;
			cout << "Jetflavour G in VertexCategory " << i << " has " << nbOfjets_G[i][j] << " in pt/eta-bin " << j << " and we keep " << nbOfjetsKept_G[i][j] << endl;
		}

        cout << "--------------------------------------------------------------------------------" << endl;
        cout << " Total for jetFlavour B in VertexCategory " << i << ": " << Total_B << endl;
        cout << " Total for jetFlavour C in VertexCategory " << i << ": " << Total_C << endl;
        cout << " Total for jetFlavour DUS in VertexCategory " << i << ": " << Total_DUS << endl;
        cout << " Total for jetFlavour G in VertexCategory " << i << ": " << Total_G << endl;
        cout << "--------------------------------------------------------------------------------" << endl;

		if(debug)newtree_B[i]->Print();
	  	newtree_B[i]->AutoSave();
		if(debug)newtree_C[i]->Print();
	  	newtree_C[i]->AutoSave();
		if(debug)newtree_DUSG[i]->Print();
	  	newtree_DUSG[i]->AutoSave();
	}
	if(debug)newtree_VertexCatMinusOne->Print();
  	newtree_VertexCatMinusOne->AutoSave();

	  	delete oldfile;
  		delete newfile_NoVertex_B;
  		delete newfile_NoVertex_C;
  		delete newfile_NoVertex_DUSG;
  		delete newfile_PseudoVertex_B;
  		delete newfile_PseudoVertex_C;
  		delete newfile_PseudoVertex_DUSG;
  		delete newfile_RecoVertex_B;
  		delete newfile_RecoVertex_C;
  		delete newfile_RecoVertex_DUSG;
  		delete newtree_VertexCatMinusOne;
}
