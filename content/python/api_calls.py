import pandas as pd
import numpy as np
import warnings
import requests
import json
import pandas

def barrier_extent(barrier_type):

    request = 'https://cabd-pro.cwf-fcf.org/bcfishpass/functions/postgisftw.wcrp_barrier_extent/items.json?watershed_group_code=ELKR&barrier_type=' + barrier_type

    response_api = requests.get(request)
    parse = response_api.text
    result = json.loads(parse)

    blocked_km = result[0]['all_habitat_blocked_km']
    blocked_pct = result[0]['extent_pct']

    return blocked_km, blocked_pct

def barrier_count(barrier_type):
    request = 'https://cabd-pro.cwf-fcf.org/bcfishpass/functions/postgisftw.wcrp_barrier_count/items.json?watershed_group_codeELKR&barrier_type=' + barrier_type

    response_api = requests.get(request)
    parse = response_api.text
    result = json.loads(parse)

    n_passable = result[0]['n_passable']
    n_barrier = result[0]['n_barrier']
    n_potential = result[0]['n_potential']
    n_unknown = result[0]['n_unknown']

    sum_bar = (n_passable, n_barrier, n_potential, n_unknown)

    return n_passable, n_barrier, n_potential, n_unknown, sum(sum_bar)

def barrier_severity(barrier_type):

    request = 'https://cabd-pro.cwf-fcf.org/bcfishpass/functions/postgisftw.wcrp_barrier_severity/items.json?watershed_group_code=ELKR&barrier_type=' + barrier_type

    response_api = requests.get(request)
    parse = response_api.text
    result = json.loads(parse)

    n_assessed_barrier = result[0]['n_assessed_barrier']
    n_assess_total = result[0]['n_assess_total']
    pct_assessed_barrier = result[0]['pct_assessed_barrier']

    return n_assessed_barrier, n_assess_total, pct_assessed_barrier

def watershed_connectivity(habitat_type):

    request = 'https://cabd-pro.cwf-fcf.org/bcfishpass/functions/postgisftw.wcrp_habitat_connectivity_status/items.json?watershed_group_code=ELKR&habitat_type=' + habitat_type

    response_api = requests.get(request)
    parse = response_api.text
    result = json.loads(parse)

    connect_stat = result[0]['connectivity_status']
    all_habitat = result[0]['all_habitat']
    all_habitat_acc = result[0]['all_habitat_accessible']

    return round(connect_stat), all_habitat, all_habitat_acc

warnings.filterwarnings('ignore')

connect = watershed_connectivity("ALL")[0]
total = watershed_connectivity("ALL")[1] #total km in ELKR
access = watershed_connectivity("ALL")[2]
gain = round((total*0.96)-access,2)                   # Change the multiplier to the goal percentage

connect_spawn = watershed_connectivity("SPAWNING")[0]
total_spawn = watershed_connectivity("SPAWNING")[1]
access_spawn = watershed_connectivity("SPAWNING")[2]
gain_spawn = round((total_spawn*0.96)-access_spawn,2)

connect_rear = watershed_connectivity("REARING")[0]
total_rear = watershed_connectivity("REARING")[1] 
access_rear = watershed_connectivity("REARING")[2]
gain_rear = round((total_rear*0.8)-access_rear,2)

connect_up = watershed_connectivity("UPSTREAM_ELKO")[0]
total_up = round(watershed_connectivity("UPSTREAM_ELKO")[1],2)
access_up = watershed_connectivity("UPSTREAM_ELKO")[2]
gain_up_31 = round((total_up*0.83)-access_up,2)  # goal for 2031
gain_up_41 = round((total_up*0.86)-access_up,2)  # goal for 2041

connect_down = watershed_connectivity("DOWNSTREAM_ELKO")[0]
total_down = round(watershed_connectivity("DOWNSTREAM_ELKO")[1], 2)
access_down = watershed_connectivity("DOWNSTREAM_ELKO")[2]
gain_down = round((total_down*0.99)-access_down,2)

num_dam = barrier_severity('DAM')[1]
km_dam = barrier_extent('DAM')[0]
pct_dam = barrier_extent('DAM')[1]
resource_km = barrier_extent('ROAD, RESOURCE/OTHER')[0]
resource_pct = round(barrier_extent('ROAD, RESOURCE/OTHER')[1])
demo_km = barrier_extent('ROAD, DEMOGRAPHIC')[0]
demo_pct = round(barrier_extent('ROAD, DEMOGRAPHIC')[1])
resource_sev = round(barrier_severity('ROAD, RESOURCE/OTHER')[2])
demo_sev = round(barrier_severity('ROAD, DEMOGRAPHIC')[2])
sum_road = barrier_severity('ROAD, RESOURCE/OTHER')[1] + barrier_severity('ROAD, DEMOGRAPHIC')[1]
sum_rail = barrier_severity('RAIL')[1]
rail_km = barrier_extent('RAIL')[0]
rail_pct = round(barrier_extent('RAIL')[1])
rail_sev = round(barrier_severity('RAIL')[2])
