import warnings
import pandas as pd
import numpy as np

warnings.filterwarnings('ignore')


def make_assess_table(species, kea, indicator, poor_upper, fair_upper, good_upper, api_call):
  """ builds the pandas table for connectivity status assessment
  :species:     target species
  :kea:         KEA eg. Accessible Spawning Habitat
  :indicator:   indicator for assessment eg. % of total spawning habitat
  :poor_upper:  upper bound for poor range
  :fair_upper:  upper bound for fair range
  :good_upper:  upper bound for good range
  :api_call:    one of api.connect, api.connect_spawn, api.connect_rear
  
  Note that very good will be inferred from good_upper
  
  """
  df = pd.DataFrame({"Focal Species":[str(species)," "],
                   "KEA":[str(kea)," "],
                   "Indicator":[str(indicator),"Current Status:"],
                   "Poor":["<"+str(poor_upper)+"%"," "],
                   "Fair":[str(poor_upper+1)+"-"+str(fair_upper)+"%"," "],
                   "Good":[str(fair_upper+1)+"-"+str(good_upper)+"%", " "],
                   "Very Good":[">"+str(good_upper)+"%"," "] 
                   })
                   
  if api_call < poor_upper:
    df["Poor"][1] = str(api_call)
  elif api_call < fair_upper:
    df["Fair"][1] = str(api_call)
  elif api_call < good_upper:
    df["Good"][1] = str(api_call)
  else:
    df["Very Good"][1] = str(api_call)
    
  def colour_table(val):
    red = '#ff0000;'
    yellow = '#ffff00;'
    lgreen = '#92d050;'
    dgreen = '#03853e;'

    if val=="<"+str(poor_upper)+"%" : color = red
    elif val.isdigit() and int(val) < poor_upper : color = red
    elif val==str(poor_upper+1)+"-"+str(fair_upper)+"%": color = yellow
    elif val.isdigit() and (int(val) > poor_upper and int(val) < fair_upper) : color = yellow 
    elif val==str(fair_upper+1)+"-"+str(good_upper)+"%"  : color = lgreen
    elif val.isdigit() and (int(val) > fair_upper and int(val) < good_upper) : color = lgreen 
    elif val ==">"+str(good_upper)+"%": color = dgreen
    elif val.isdigit() and int(val) > good_upper : color = dgreen 
    elif val == "Current Status:" : return "font-weight: bold"
    else: color = 'white'
    return 'background-color: %s' % color
  
  return df.style.applymap(colour_table).set_table_styles(
   [{
       'selector': 'th',
       'props': [('background-color', '#008270'),('text-align', 'left')]
   }]).hide()
