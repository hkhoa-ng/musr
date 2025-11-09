import numpy as np

def nominal_delta(a, b):
    """Nominal distance: 0 if equal, 1 if different."""
    if a is None or b is None:
        return 0  # Skip missing pairs
    return 0 if a == b else 1

def safe_masi_distance(label1, label2):
    """Safe MASI distance metric that handles empty sets."""
    if label1 is None or label2 is None:
        return 0  # Skip missing pairs
    set_a = set(label1) if not isinstance(label1, (set, frozenset)) else label1
    set_b = set(label2) if not isinstance(label2, (set, frozenset)) else label2
    
    if len(set_a) == 0 and len(set_b) == 0:
        return 0.0
    elif len(set_a) == 0 or len(set_b) == 0:
        return 1.0
    
    len_intersection = len(set_a.intersection(set_b))
    len_union = len(set_a.union(set_b))
    len_label1 = len(set_a)
    len_label2 = len(set_b)
    
    if len_label1 == len_label2 and len_label1 == len_intersection:
        m = 1
    elif len_intersection == min(len_label1, len_label2):
        m = 0.67
    elif len_intersection > 0:
        m = 0.33
    else:
        m = 0
    
    return 1 - (len_intersection / len_union) * m

def compute_alpha(data, delta_func):
    """Compute Krippendorff's alpha, handling varying numbers of raters."""
    data = [list(unit) for unit in data]
    N = len(data)  # Number of units (stories)
    
    # Compute D_o: average distance over within-unit pairs
    total_within_pairs = 0
    D_o = 0
    for unit in data:
        m = sum(1 for x in unit if x is not None)  # Count non-missing raters
        if m < 2:
            continue  # Skip units with fewer than 2 raters
        pairs = m * (m - 1) / 2
        total_within_pairs += pairs
        for i in range(len(unit)):
            for j in range(i + 1, len(unit)):
                if unit[i] is not None and unit[j] is not None:
                    D_o += delta_func(unit[i], unit[j])
    D_o = D_o / total_within_pairs if total_within_pairs > 0 else 0
    
    # Compute D_e: average distance over all possible pairs
    all_values = [r for unit in data for r in unit if r is not None]
    n = len(all_values)
    total_all_pairs = n * (n - 1) / 2
    D_e = 0
    for i in range(n):
        for j in range(i + 1, n):
            D_e += delta_func(all_values[i], all_values[j])
    D_e = D_e / total_all_pairs if total_all_pairs > 0 else 0
    
    # Alpha
    if D_e == 0:
        return 1.0
    else:
        return 1 - D_o / D_e

# Grouping datasets: DS1 (US1–US10, 4 raters), DS2 (US11–US20, 4 raters), DS3 (US21–US30, 3 raters)
grouping_data = [
    [1, 1, 1, 1],  # US1
    [2, 2, 2, 2],  # US2
    [2, 2, 2, 3],  # US3
    [3, 3, 3, 3],  # US4
    [4, 4, 4, 4],  # US5
    [5, 7, 4, 5],  # US6
    [4, 4, 4, 4],  # US7
    [6, 6, 6, 6],  # US8
    [7, 7, 4, 7],  # US9
    [8, 8, 8, 8],  # US10
    [9, 9, 9, 9],  # US11
    [9, 9, 9, 9],  # US12
    [10, 10, 10, 10],  # US13
    [11, 11, 11, 11],  # US14
    [11, 11, 11, 11],  # US15
    [9, 9, 9, 9],  # US16
    [9, 9, 9, 9],  # US17
    [9, 9, 9, 9],  # US18
    [11, 11, 11, 11],  # US19
    [12, 12, 12, 12],  # US20
    [3, 3, 3, None],  # US21
    [1, 6, 1, None],  # US22
    [1, 7, 1, None],  # US23
    [2, 8, 2, None],  # US24
    [2, 7, 2, None],  # US25
    [5, 9, 2, None],  # US26
    [1, 6, 1, None],  # US27
    [4, 10, 4, None],  # US28
    [5, 11, 4, None],  # US29
    [3, 10, 3, None],  # US30
]

# Ticket-linking datasets: DS1 (US1–US10, 4 raters), DS2 (US11–US20, 4 raters), DS3 (US21–US30, 3 raters)
ticket_data = [
    [frozenset([502]), frozenset([502]), frozenset([502]), frozenset([502])],  # US1
    [frozenset([101]), frozenset([101]), frozenset([101]), frozenset([101])],  # US2
    [frozenset(), frozenset(), frozenset(), frozenset([501])],  # US3
    [frozenset([501]), frozenset([501]), frozenset([501]), frozenset([501])],  # US4
    [frozenset(), frozenset(), frozenset(), frozenset([302])],  # US5
    [frozenset([102, 303]), frozenset([102, 303]), frozenset([102, 303]), frozenset([303])],  # US6
    [frozenset([302]), frozenset([302]), frozenset([302]), frozenset([302])],  # US7
    [frozenset([202]), frozenset([202]), frozenset([201, 202, 203, 204]), frozenset([202])],  # US8
    [frozenset([301, 304]), frozenset([301, 304]), frozenset([301, 304]), frozenset([301])],  # US9
    [frozenset([503]), frozenset(), frozenset([503]), frozenset()],  # US10
    [frozenset([22, 23]), frozenset([21, 23]), frozenset([22, 23]), frozenset([22, 23])],  # US11
    [frozenset([9, 15, 16, 41]), frozenset([5, 16]), frozenset([15, 16]), frozenset([15, 23])],  # US12
    [frozenset([14]), frozenset(), frozenset([14]), frozenset()],  # US13
    [frozenset([12, 17, 21, 37, 38, 48]), frozenset([17, 20, 86]), frozenset([12, 17, 20, 37, 38, 39, 40, 41, 48]), frozenset([12])],  # US14
    [frozenset([13, 19]), frozenset([19]), frozenset([13, 19]), frozenset([13])],  # US15
    [frozenset([11, 39, 40]), frozenset(), frozenset([11, 21]), frozenset([11])],  # US16
    [frozenset([5, 6, 8, 10]), frozenset([80]), frozenset([6, 8, 9, 10]), frozenset([10])],  # US17
    [frozenset([86]), frozenset(), frozenset([86]), frozenset()],  # US18
    [frozenset([18, 47]), frozenset([18, 47]), frozenset([18, 47]), frozenset([18])],  # US19
    [frozenset([79, 80, 95, 102]), frozenset([95, 102]), frozenset([79, 80, 95, 102]), frozenset()],  # US20
    [frozenset(), frozenset(), frozenset(), None],  # US21
    [frozenset([634, 565]), frozenset([657, 652, 669, 650, 656, 602, 601, 576, 566, 674, 565]), frozenset([672, 572]), None],  # US22
    [frozenset([681, 628, 613, 646]), frozenset([629, 613, 646, 666, 655, 612, 615, 608, 599, 598, 595, 596, 592, 588, 590, 591, 593, 584, 586, 583, 580]), frozenset([628, 681]), None],  # US23
    [frozenset(), frozenset(), frozenset(), None],  # US24
    [frozenset(), frozenset(), frozenset(), None],  # US25
    [frozenset([672, 610, 572]), frozenset([672, 681, 678, 572]), frozenset([572, 672]), None],  # US26
    [frozenset([653]), frozenset([620, 653, 677, 679, 660, 659, 671, 628, 661, 649, 627, 619, 625, 621]), frozenset([620, 653]), None],  # US27
    [frozenset(), frozenset(), frozenset(), None],  # US28
    [frozenset([568, 569]), frozenset([569, 568]), frozenset([568]), None],  # US29
    [frozenset(), frozenset(), frozenset(), None],  # US30
]

# Compute for Grouping Datasets
# DS1 (US1–US10, 4 raters)
human_grouping_ds1 = [row[:3] for row in grouping_data[:10]]  # First 3 raters
human_alpha_ds1 = compute_alpha(human_grouping_ds1, nominal_delta)
print(f"Grouping DS1 Human raters' Krippendorff's alpha: {human_alpha_ds1 :.3f}")
alpha_ds1 = compute_alpha(grouping_data[:10], nominal_delta)
print(f"Grouping DS1 MAS against human raters' Krippendorff's alpha: {alpha_ds1 :.3f}")
print(f"Grouping DS1 Delta: {(alpha_ds1 - human_alpha_ds1) :.3f}")

# DS2 (US11–US20, 4 raters)
human_grouping_ds2 = [row[:3] for row in grouping_data[10:20]]  # First 3 raters
human_alpha_ds2 = compute_alpha(human_grouping_ds2, nominal_delta)
print(f"Grouping DS2 Human raters' Krippendorff's alpha: {human_alpha_ds2 :.3f}")
alpha_ds2 = compute_alpha(grouping_data[10:20], nominal_delta)
print(f"Grouping DS2 MAS against human raters' Krippendorff's alpha: {alpha_ds2 :.3f}")
print(f"Grouping DS2 Delta: {(alpha_ds2 - human_alpha_ds2) :.3f}")

# DS3 (US21–US30, 3 raters)
human_grouping_ds3 = [row[:2] for row in grouping_data[20:]]  # First 2 raters
human_alpha_ds3 = compute_alpha(human_grouping_ds3, nominal_delta)
print(f"Grouping DS3 Human raters' Krippendorff's alpha: {human_alpha_ds3 :.3f}")
alpha_ds3 = compute_alpha(grouping_data[20:], nominal_delta)
print(f"Grouping DS3 MAS against human raters' Krippendorff's alpha: {alpha_ds3 :.3f}")
print(f"Grouping DS3 Delta: {(alpha_ds3 - human_alpha_ds3) :.3f}")

# Compute for Ticket-Linking Datasets
# DS1 (US1–US10, 4 raters)
human_ticket_ds1 = [row[:3] for row in ticket_data[:10]]  # First 3 raters
human_masi_alpha_ds1 = compute_alpha(human_ticket_ds1, safe_masi_distance)
print(f"Ticket DS1 Human raters' K-alpha with MASI distance: {human_masi_alpha_ds1 :.3f}")
masi_alpha_ds1 = compute_alpha(ticket_data[:10], safe_masi_distance)
print(f"Ticket DS1 MAS against human raters' K-alpha with MASI distance: {masi_alpha_ds1 :.3f}")
print(f"Ticket DS1 Delta: {(masi_alpha_ds1 - human_masi_alpha_ds1) :.3f}")

# DS2 (US11–US20, 4 raters)
human_ticket_ds2 = [row[:3] for row in ticket_data[10:20]]  # First 3 raters
human_masi_alpha_ds2 = compute_alpha(human_ticket_ds2, safe_masi_distance)
print(f"Ticket DS2 Human raters' K-alpha with MASI distance: {human_masi_alpha_ds2 :.3f}")
masi_alpha_ds2 = compute_alpha(ticket_data[10:20], safe_masi_distance)
print(f"Ticket DS2 MAS against human raters' K-alpha with MASI distance: {masi_alpha_ds2 :.3f}")
print(f"Ticket DS2 Delta: {(masi_alpha_ds2 - human_masi_alpha_ds2) :.3f}")

# DS3 (US21–US30, 3 raters)
human_ticket_ds3 = [row[:2] for row in ticket_data[20:]]  # First 2 raters
human_masi_alpha_ds3 = compute_alpha(human_ticket_ds3, safe_masi_distance)
print(f"Ticket DS3 Human raters' K-alpha with MASI distance: {human_masi_alpha_ds3 :.3f}")
masi_alpha_ds3 = compute_alpha([row[:3] for row in ticket_data[20:]], safe_masi_distance)
print(f"Ticket DS3 MAS against human raters' K-alpha with MASI distance: {masi_alpha_ds3 :.3f}")
print(f"Ticket DS3 Delta: {(masi_alpha_ds3 - human_masi_alpha_ds3) :.3f}")

# Combined Grouping (DS1+DS2+DS3)
human_grouping_all = [row[:3] if len(row) > 3 else row[:2] for row in grouping_data]
human_alpha_all = compute_alpha(human_grouping_all, nominal_delta)
print(f"Combined Grouping DS1+DS2+DS3 Human raters' Krippendorff's alpha: {human_alpha_all :.3f}")
alpha_all = compute_alpha(grouping_data, nominal_delta)
print(f"Combined Grouping DS1+DS2+DS3 MAS against human raters' Krippendorff's alpha: {alpha_all :.3f}")
print(f"Combined Grouping DS1+DS2+DS3 Delta: {(alpha_all - human_alpha_all) :.3f}")

# Combined Ticket Linking (DS1+DS2+DS3)
human_ticket_all = [row[:3] if len(row) > 3 else row[:2] for row in ticket_data]
human_masi_alpha_all = compute_alpha(human_ticket_all, safe_masi_distance)
print(f"Combined Ticket DS1+DS2+DS3 Human raters' K-alpha with MASI distance: {human_masi_alpha_all :.3f}")
masi_alpha_all = compute_alpha([row[:4] if len(row) > 3 else row[:3] for row in ticket_data], safe_masi_distance)
print(f"Combined Ticket DS1+DS2+DS3 MAS against human raters' K-alpha with MASI distance: {masi_alpha_all :.3f}")
print(f"Combined Ticket DS1+DS2+DS3 Delta: {(masi_alpha_all - human_masi_alpha_all) :.3f}")
