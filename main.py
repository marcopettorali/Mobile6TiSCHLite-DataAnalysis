from scenario import *
from itertools import product
# scp ubuntu@172.16.4.120:~/omnetpp-5.6.2/samples/MobileTSCH/MobileTSCH/simulations/sysmtsch/results/debug-* ~/PycharmProjects/MobileTSCHDataAnalysis/samples

name = f"/home/ubuntu/git/Mobile6TiSCH-Lite/Mobile6TiSCH-Lite/simulations/mobile6tischlite/results"

parse_scenario(name + f"/speed_reqres_dddu_p75-100,0.5mps")
parse_scenario(name + f"/speed_reqres_dddu_p75-100,2mps")
parse_scenario(name + f"/speed_reqres_dddu_p75-100,5mps")
exit()

for s, p, mn, m in product(["convergecast_sddu4", "reqres_dddu"], [25,50,75], list(range(10,110,10)), [0,1,2]) :
    parse_scenario(name + f"/mobility_{s}_p{p}-{mn},{m}")

for s, p, mn, sp in product(["convergecast_sddu4", "reqres_dddu"], [25,50,75], list(range(10,110,10)), [0.5,2,5]) :
    parse_scenario(name + f"/speed_{s}_p{p}-{mn},{sp}mps")
