from stats_util import *


import time
import os
import os.path

def read_vectors(repetition):
    names = {}
    vectors = {}
    with open(repetition + ".vec", "r") as vec_file:
        for line in vec_file:
            if "vector" in line:
                array = line.split(" ")
                names[array[1]] = array[2] + " " + array[3].split(":")[0]
            else:
                array = line.split("\t")
                if array[0].isdigit():
                    name = names[array[0]]
                    if not name in vectors:
                        vectors[name] = []
                    vectors[name].append(line)

    return vectors


def read_scalars(repetition):
    scalars = {}
    with open(repetition + ".sca", "r") as sca_file:
        for line in sca_file:
            if "scalar" in line:
                array = line.split(" ")
                try:
                    scalars[array[1] + " " +
                        array[2].split(":")[0]] = array[3].strip()
                except:
                    return scalars
    return scalars

def parse_repetition(repetition):

    print("########################")
    print(f"Repetition {repetition}")

    # load scalars
    scalars_str = read_scalars(repetition)

    # load vectors
    vectors = read_vectors(repetition)

    # PDR
    pdr = {}
    up_s = 0
    up_r = 0
    down_s = 0
    down_r = 0
    for scalar in scalars_str:
        if "stats_upstreamPacketSent" in scalar:
            up_s += int(scalars_str[scalar])
        elif "stats_upstreamPacketReceived" in scalar:
            up_r += int(scalars_str[scalar])
        elif "stats_downstreamPacketSent" in scalar:
            down_s += int(scalars_str[scalar])
        elif "stats_downstreamPacketReceived" in scalar:
            down_r += int(scalars_str[scalar])
    
    pdr["Upstream PDR"] = 0 if up_s == 0 else up_r / up_s
    pdr["Downstream PDR"] = 0 if down_s == 0 else down_r / down_s
    pdr["TicToc PDR"] = 0 if up_s == 0 else down_r/up_s 

 
    # OUTCOMES
    outcomes_temp = {'0':0, '1':0,'2':0,'3':0, '4':0, '5':0}
    total = 0
    for scalar in scalars_str:
        if "outcome" in scalar:
            val = int(scalar.split("outcome")[1])
            outcomes_temp[str(val)] += int(scalars_str[scalar])
            total += int(scalars_str[scalar])
        elif "packetsDropped" in scalar:
            outcomes_temp['5'] += int(scalars_str[scalar])
            total += int(scalars_str[scalar])
    for o in outcomes_temp:
        outcomes_temp[o] = 0 if total == 0 else outcomes_temp[o]/total

    outcomes = {
        "Packets delivered": outcomes_temp['0'],
        "Packets lost due to noise": outcomes_temp['1'],
        "Packets collided": outcomes_temp['2'],
        "Destinatary out of range": outcomes_temp['3'],
        "Packets dropped":outcomes_temp['5'],
        "Other causes of loss": outcomes_temp['4']
    }

    # QUEUE SIZE
    queue = {}

    mn = []
    br = []

    for scalar in scalars_str:
        if "stats_queueSize" in scalar and "mn" in scalar:
            mn.append(float(scalars_str[scalar]))
        elif "stats_queueSize" in scalar and "br" in scalar:
            br.append(float(scalars_str[scalar]))

    queue["Queue MN Avg"] = s_mean_value(mn)
    queue["Queue MN Var"] = 0 if len(mn) <= 1 else s_variance(mn) 
    queue["Queue BR Avg"] = s_mean_value(br)
    queue["Queue BR Var"] = 0 if len(br) <= 1 else s_variance(br)


    # DELAY
    delay = {}

    down_avgs = []
    down_95per = []
    down_vars = []

    up_avgs = []
    up_95per = []
    up_vars = []

    rtt_avgs = []
    rtt_95per = []
    rtt_vars = []

    for vector in vectors:
        if "stats_downstreamPacketDelay" in vector:
            samples = [float(x.split("\t")[3]) for x in vectors[vector]]
            down_avgs.append(s_mean_value(samples))
            down_95per.append(s_percentile(samples, 0.95))
            down_vars.append(0 if len(samples) <= 1 else s_variance(samples)) 
        elif "stats_upstreamPacketDelay" in vector:
            samples = [float(x.split("\t")[3]) for x in vectors[vector]]
            up_avgs.append(s_mean_value(samples))
            up_95per.append(s_percentile(samples, 0.95))
            up_vars.append(0 if len(samples) <= 1 else s_variance(samples))
        elif "stats_rtt" in vector:
            samples = [float(x.split("\t")[3]) for x in vectors[vector]]
            rtt_avgs.append(s_mean_value(samples))
            rtt_95per.append(s_percentile(samples, 0.95))
            rtt_vars.append(0 if len(samples) <= 1 else s_variance(samples) )
    
    delay["Upstream Delay Avg"] = s_mean_value(up_avgs)
    delay["Upstream Delay 95th Perc"] = s_mean_value(up_95per)
    delay["Upstream Delay Var"] = s_mean_value(up_vars)
    delay["Downstream Delay Avg"] = s_mean_value(down_avgs)
    delay["Downstream Delay 95th Perc"] = s_mean_value(down_95per)
    delay["Downstream Delay Var"] = s_mean_value(down_vars)
    delay["RTT Avg"] = s_mean_value(rtt_avgs)
    delay["RTT 95th Perc"] = s_mean_value(rtt_95per)
    delay["RTT Var"] = s_mean_value(rtt_vars)

    ################

    ret = {}
    ret.update(pdr)
    ret.update(outcomes)
    ret.update(queue)
    ret.update(delay)

    print(ret)
    return ret
