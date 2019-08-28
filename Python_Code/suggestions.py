import numpy as np
from AADI_RoverDomain.parameters import Parameters as p

def low_high_split(rover_dist, rover_id, poi_id, poi_values, n_counters):
    npartners = n_counters

    partners = np.zeros(npartners)

    if rover_id < p.num_rovers/2:
        if poi_values[poi_id] > 5.0:
            for partner_id in range(npartners):
                partners[partner_id] = rover_dist
        else:
            for partner_id in range(npartners):
                partners[partner_id] = 100.0
    else:
        if poi_values[poi_id] <= 5.0:
            for partner_id in range(npartners):
                partners[partner_id] = rover_dist
        else:
            for partner_id in range(npartners):
                partners[partner_id] = 100.0

    return partners, npartners

def satisfy_coupling_high_value_incentive(rover_dist, poi_id, poi_values, n_counters):
    npartners = n_counters

    partners = np.zeros(npartners)
    if poi_values[poi_id] > 5.0:
        for partner_id in range(npartners):
            partners[partner_id] = p.min_distance
    else:
        for partner_id in range(npartners):
            partners[partner_id] = rover_dist

    return partners, npartners

def high_value_only(rover_dist, poi_id, poi_values, n_counters):
    npartners = n_counters

    partners = np.zeros(npartners)
    if poi_values[poi_id] > 5.0:
        for partner_id in range(npartners):
            partners[partner_id] = rover_dist
    else:
        for partner_id in range(npartners):
            partners[partner_id] = 100.0

    return partners, npartners

def low_value_pois(rover_dist, poi_id, poi_values, n_counters):
    npartners = n_counters

    partners = np.zeros(npartners)
    if poi_values[poi_id] <= 5.0:
        for partner_id in range(npartners):
            partners[partner_id] = rover_dist
    else:
        for partner_id in range(npartners):
            partners[partner_id] = 100.0

    return partners, npartners

def position_based(nobservers, rover_dist, rx, ry, poi_id, poi_values, n_counters):
    npartners = n_counters

    partners = np.zeros(npartners)

    if ry > 15 and poi_values[poi_id] <= 5.0:
        for partner_id in range(npartners):
            partners[partner_id] = p.min_distance
    else:
        for partner_id in range(npartners):
            partners[partner_id] = rover_dist

    return partners, npartners

def negative_distances(rover_dist, poi_id, poi_values, n_counters):
    npartners = n_counters

    partners = np.zeros(npartners)

    if poi_values[poi_id] > 5:
        for partner_id in range(npartners):
            partners[partner_id] = rover_dist
    elif rover_dist < p.min_observation_dist:
        for partner_id in range(npartners):
            partners[partner_id] = -10.0
    else:
        for partner_id in range(npartners):
            partners[partner_id] = 100.00

    return partners, npartners
