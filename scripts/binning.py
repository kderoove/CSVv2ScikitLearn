from pdb import set_trace

pt_bins = [15, 40, 60, 90, 150, 400, 600]
eta_bins = [1.2, 2.1]
flavors = ['B', 'C', 'DUSG']
sv_categories = ["RecoVertex", "PseudoVertex", "NoVertex"]

def get_cut(ptmin, ptmax, etamin, etamax):
   if ptmin is not None and ptmax is not None:
      pt_cut = '%.0f <= Jet_pt && Jet_pt < %.0f' % (ptmin, ptmax)
   elif ptmin is None: #x underflow
      pt_cut = 'Jet_pt < %.0f' % (ptmax)
   else:
      pt_cut = '%.0f <= Jet_pt' % (ptmin)

   if etamin is not None and etamax is not None:
      eta_cut = '%.4f <= TMath::Abs(Jet_eta) && TMath::Abs(Jet_eta) < %.4f' % (etamin, etamax)
   elif etamin is None: #y underflow
      eta_cut = 'TMath::Abs(Jet_eta) <= %.4f' % (etamax)
   else:
      eta_cut = '%.4f <= TMath::Abs(Jet_eta)' % (etamin)
   return '%s && %s' % (pt_cut, eta_cut)

def cut_from_bin(proxy):
   pt_i, eta_i, _ = proxy.xyz
   ptmin = proxy.x.low  if pt_i != 0 else None
   ptmax = proxy.x.high if pt_i < len(pt_bins) else None

   etamin = proxy.y.low  if eta_i != 0 else None
   etamax = proxy.y.high if eta_i < len(eta_bins) else None
   
   return get_cut(ptmin, ptmax, etamin, etamax)

def itercuts():
   ptmin = None
   for ptmax in pt_bins:
      etamin = None
      for etamax in eta_bins:
         yield get_cut(ptmin, ptmax, etamin, etamax)
         etamin = etamax
      yield get_cut(ptmin, ptmax, etamin, None)
      ptmin = ptmax

   etamin = None
   for etamax in eta_bins:
      yield get_cut(ptmin, None, etamin, etamax)
      etamin = etamax
   yield get_cut(ptmin, None, etamin, None)
