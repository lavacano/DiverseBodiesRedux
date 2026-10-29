"""The pool's archetypes: per sex and tier, slider ranges in percent (lo, hi). Each archetype names how many
bodies it gives. A slider not named is 0. Ranges were set from the measured effects (effects.json) and the
calibration run: CBBE's zeroed body is already a fantasy hourglass (waist/hip 0.60), so ordinary women need
a much thicker waist than the base, and the ugly shapes need strong values to read as what they are.

No woman's bust goes below a small but real one (owner poll, 2026-09-24, from a render and a photo of a
concave chest the physics folded): Breasts at least 0, BreastsSmall at most 30 -- tests/test_pool.py holds it."""

FEMALE = {
    'beautiful': {
        'Hourglass': (1, {'Breasts': (35, 55), '7B Upper': (15, 30), 'BreastPerkiness': (15, 35), 'PushUp': (5, 25),
                          'Hips': (15, 30), 'Butt': (20, 35), 'RoundAss': (25, 55), 'ChubbyWaist': (5, 15), 'Thighs': (10, 20)}),
        'Athletic': (1, {'MuscularArms': (25, 45), 'MuscularLegs': (30, 50), 'MuscularButt': (40, 70), 'BreastsSmall': (0, 10),
                         'Breasts': (20, 35), 'ChestWidth': (5, 20), 'ChubbyWaist': (10, 20), 'Butt': (15, 30),
                         'BreastPerkiness': (20, 40), 'RoundAss': (20, 40)}),
        'Slender': (1, {'LegsThin': (5, 20), 'Arms': (5, 15), 'BreastsSmall': (0, 10), 'Breasts': (25, 35),
                        'BreastPerkiness': (20, 40), 'ChubbyWaist': (5, 15), 'Hips': (10, 20), 'Butt': (10, 20), 'SlimThighs': (0, 15)}),
        'Voluptuous': (1, {'7B Upper': (25, 45), 'Breasts': (45, 65), 'BreastGravity2': (5, 15), 'Hips': (25, 40),
                           'BigButt': (25, 45), 'Thighs': (25, 40), 'ChubbyWaist': (10, 20), 'ChubbyArms': (5, 15), 'AppleCheeks': (10, 30)}),
        'Petite': (1, {'BreastsSmall': (0, 15), 'Breasts': (20, 35), 'BreastPerkiness': (20, 40), 'SlimThighs': (5, 20),
                       'Arms': (5, 15), 'LegsThin': (5, 15), 'RoundAss': (20, 40), 'ChubbyWaist': (0, 10), 'Hips': (5, 15)}),
        'Pear': (1, {'BreastsSmall': (0, 10), 'Breasts': (20, 35), 'Hips': (30, 45), 'Thighs': (30, 45), 'AppleCheeks': (30, 50), 'Butt': (25, 40),
                     'ChubbyWaist': (5, 15), 'ChubbyButt': (15, 30)}),
    },
    'middle': {
        'Average': (3, {'ChubbyWaist': (30, 60), 'WideWaistLine': (15, 35), 'HipUpperWidth': (10, 25), 'Belly': (10, 25),
                        'Breasts': (28, 45), 'BreastGravity2': (15, 30), 'Hips': (8, 22), 'Butt': (10, 25), 'Thighs': (5, 20),
                        'BreastsSmall': (0, 10)}),
        'Soft': (3, {'ChubbyWaist': (40, 70), 'Belly': (20, 40), 'BigBelly': (10, 25), 'WideWaistLine': (15, 30), 'ChubbyArms': (15, 30),
                     'ChubbyLegs': (10, 25), 'Breasts': (30, 50), 'BreastGravity2': (20, 40), 'ChubbyButt': (15, 30), 'Hips': (10, 25), 'Butt': (15, 30)}),
        'Lean': (3, {'LegsThin': (5, 20), 'Arms': (5, 15), 'BreastsSmall': (0, 10), 'Breasts': (20, 35), 'ButtSmall': (0, 15), 'ChubbyWaist': (25, 50),
                     'WideWaistLine': (20, 40), 'HipUpperWidth': (10, 25), 'BreastGravity2': (10, 20), 'Hips': (5, 18), 'Butt': (10, 20)}),
        'Sturdy': (3, {'BigTorso': (10, 25), 'Back': (15, 30), 'ChestWidth': (10, 25), 'ChubbyWaist': (30, 55), 'WideWaistLine': (15, 30),
                       'MuscularLegs': (15, 35), 'MuscularArms': (10, 25), 'Thighs': (10, 25), 'Hips': (8, 22), 'Butt': (10, 25),
                       'Breasts': (25, 40)}),
        'Busty': (3, {'Breasts': (40, 60), '7B Upper': (15, 30), 'BreastGravity2': (20, 40), 'ChubbyWaist': (30, 55), 'Belly': (10, 25),
                      'WideWaistLine': (10, 25), 'Hips': (10, 25), 'Butt': (15, 30)}),
        'WideHips': (3, {'Hips': (25, 45), 'Thighs': (25, 40), 'ChubbyLegs': (10, 25), 'ChubbyButt': (20, 35), 'ChubbyWaist': (30, 55),
                         'HipUpperWidth': (15, 30), 'Belly': (10, 25), 'Breasts': (25, 40), 'BreastGravity2': (10, 25)}),
    },
    'ugly': {
        'Obese': (3, {'ChubbyWaist': (80, 110), 'BigBelly': (25, 45), 'Belly': (60, 90), 'HipUpperWidth': (40, 70),
                      'WideWaistLine': (40, 70), 'ChubbyLegs': (50, 80), 'ChubbyButt': (40, 70),
                      'BigTorso': (30, 50), 'Back': (30, 50), 'Breasts': (45, 65), 'BreastGravity2': (40, 60),
                      'Thighs': (30, 50), 'CalfSize': (25, 45)}),
        'Flat': (3, {'Breasts': (18, 28), 'BreastsSmall': (0, 10),
                     'ButtSmall': (0, 15), 'Hips': (0, 12), 'SlimThighs': (10, 25), 'ChubbyWaist': (35, 60),
                     'WideWaistLine': (25, 45), 'HipUpperWidth': (15, 30), 'Butt': (8, 18)}),
        'Frail': (2, {'LegsThin': (30, 60), 'Arms': (20, 40), 'SlimThighs': (20, 40), 'ButtSmall': (0, 15),
                      'Breasts': (18, 28), 'BreastsSmall': (0, 10), 'BreastGravity2': (15, 30), 'Hips': (0, 12), 'CalfSmooth': (20, 40), 'WideWaistLine': (10, 25)}),
        'Apple': (3, {'BigBelly': (20, 40), 'Belly': (50, 80), 'ChubbyWaist': (70, 100), 'WideWaistLine': (25, 50),
                      'HipUpperWidth': (25, 45), 'Back': (25, 45),
                      'LegsThin': (15, 30), 'ButtSmall': (0, 15), 'SlimThighs': (5, 20), 'Breasts': (25, 45), 'BreastGravity2': (30, 50)}),
        'Saggy': (2, {'BreastGravity2': (50, 75), 'Breasts': (30, 50), 'Belly': (25, 45), 'BigBelly': (10, 25),
                      'ChubbyWaist': (45, 65), 'ButtSmall': (0, 15), 'WideWaistLine': (15, 35), 'Hips': (8, 22), 'Butt': (10, 25)}),
        'BottomHeavy': (2, {'ChubbyLegs': (50, 80), 'Thighs': (40, 65), 'Hips': (35, 55), 'BigButt': (30, 50), 'ChubbyButt': (35, 55),
                            'Breasts': (20, 35), 'BreastsSmall': (0, 10), 'ChubbyWaist': (30, 50)}),
        'Boxy': (2, {'BigTorso': (25, 45), 'ChestWidth': (30, 50), 'Back': (25, 45), 'ChubbyWaist': (45, 70), 'WideWaistLine': (35, 55),
                     'HipUpperWidth': (20, 35), 'Hips': (0, 12), 'ButtSmall': (0, 15), 'Breasts': (20, 35)}),
    },
}

MALE = {
    'beautiful': {
        'Athlete': (1, {'TigerSanBBMale': (20, 35), 'BTAbDefinition': (50, 80), 'BTPectorals': (30, 50), 'BTShoulders': (30, 50),
                        'BTWaist-In': (30, 50), 'BT2AdonisBelt': (30, 60)}),
        'Swimmer': (1, {'BTAbDefinition': (30, 50), 'BTBiceps': (30, 50), 'BTButt': (40, 60), 'BTCalves': (50, 75), 'BTShoulders': (10, 20),
                        'BTStomach': (30, 45), 'BTTraps': (10, 25), 'BTWaist-In': (20, 35), 'BTThinArm': (20, 40), 'ThinThigh': (30, 60)}),
        'Muscular': (1, {'BTAryaydaMoreMuscular': (30, 50), 'BTARYAYDA': (30, 50), 'BTAbDefinition': (40, 70), 'BTTraps': (40, 60),
                         'BTPectorals': (20, 40), 'BTWaist-In': (10, 30)}),
        'Lean': (1, {'BTAbDefinition': (50, 80), 'BTNegStomach': (20, 40), 'BTWaist-In': (30, 50), 'BTPectorals': (10, 25),
                     'BTBiceps': (20, 40), 'BTShoulders': (10, 25)}),
        'Broad': (1, {'TigerSanBBMale': (40, 60), 'BTShoulders': (40, 60), 'BTTraps': (40, 60), 'BTBack': (30, 50), 'BTAbDefinition': (20, 40)}),
        'Classic': (1, {'BTPectorals': (20, 35), 'BTShoulders': (20, 35), 'BTAbDefinition': (30, 50), 'BTBiceps': (20, 35),
                        'BTWaist-In': (20, 30), 'BTButt': (20, 40)}),
    },
    'middle': {
        'Average': (3, {'BTStomachFat': (20, 50), 'BTChubbyArm': (20, 50), 'BTChubbyLeg': (10, 40), 'BTPectorals': (0, 15),
                        'BTChestSmoothing': (20, 40), 'Hips': (10, 30)}),
        'Dad': (3, {'BTStomachFat': (50, 80), 'BTLowerStomachSize': (20, 50), 'BTChestSmoothing': (30, 50), 'BTChubbyArm': (30, 60),
                    'BTBodyFatv2': (5, 15), 'Hips': (20, 40)}),
        'Lean': (3, {'BTThinArm': (20, 50), 'ThinThigh': (20, 50), 'BTTHinCalf': (20, 50), 'BTStomachFat': (0, 20), 'BTAbDefinition': (0, 20)}),
        'Stocky': (3, {'BTBodyFatv2': (10, 25), 'BTStomachFat': (30, 50), 'BTShoulders': (20, 40), 'BTTraps': (20, 40), 'BTThigh': (20, 40),
                       'BTChubbyLeg': (20, 40)}),
        'Wiry': (3, {'BTAbDefinition': (10, 30), 'BTThinArm': (30, 50), 'BTBiceps': (10, 20), 'BTStomach': (10, 25), 'ThinThigh': (30, 50)}),
        'Soft': (3, {'BTStomachFat': (40, 60), 'BTChestSmoothing': (40, 70), 'BTChubbyArm': (40, 70), 'BTChubbyLeg': (30, 50), 'Hips': (30, 50)}),
    },
    'ugly': {
        'Obese': (3, {'BTBodyFatv2': (70, 100), 'BTStomachFat': (100, 130), 'BTLowerStomachSize': (50, 80), 'BTChubbyArm': (80, 100),
                      'BTChubbyLeg': (60, 90), 'BTChestSmoothing': (60, 90), 'Hips': (60, 100)}),
        'BeerBelly': (3, {'BTStomachFat': (110, 130), 'BTLowerStomachSize': (60, 90), 'BTCenterStomachSize': (50, 80), 'BTThinArm': (40, 70),
                          'ThinThigh': (40, 70), 'BTTHinCalf': (30, 60), 'BTNegPecMuscle': (30, 50)}),
        'Frail': (3, {'BTThinArm': (80, 100), 'ThinThigh': (80, 100), 'BTTHinCalf': (80, 100), 'BTNegBicepMuscle': (60, 90),
                      'BTNegPecMuscle': (60, 90), 'BTNegChestWidth': (50, 80), 'BTNegShoulder': (50, 80), 'BTNegScapularMuscle': (40, 70)}),
        'Pear': (3, {'BTThighWidth': (60, 90), 'BTOuterUpperThighSize': (60, 90), 'BTButt': (60, 90), 'Hips': (70, 100), 'BTNegShoulder': (40, 70),
                     'BTNegChestWidth': (30, 60), 'BTStomachFat': (50, 80), 'BTChestSmoothing': (40, 60)}),
        'Moobs': (3, {'BTChestSmoothing': (80, 100), 'BTStomachFat': (70, 100), 'BTBodyFatv2': (20, 40), 'BTChubbyArm': (60, 90),
                      'BTNegPecMuscle': (30, 60), 'Hips': (40, 70)}),
        'SkinnyFat': (2, {'BTStomachFat': (60, 90), 'BTThinArm': (50, 80), 'ThinThigh': (40, 70), 'BTNegShoulder': (40, 70),
                          'BTNegChestWidth': (40, 70), 'BTChestSmoothing': (40, 70)}),
    },
}

ARCHETYPES = {'female': FEMALE, 'male': MALE}
