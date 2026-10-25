"""The pool's archetypes: per sex and tier, slider ranges in percent (lo, hi). Each archetype names how many
bodies it gives. A slider not named is 0. Ranges were set from the measured effects (effects.json) and the
calibration run: CBBE's zeroed body is already a fantasy hourglass (waist/hip 0.60), so ordinary women need
a much thicker waist than the base, and the ugly shapes need strong values to read as what they are.

No woman's bust goes below a small but real one (owner poll, 2026-09-24, from a render and a photo of a
concave chest the physics folded): Breasts at least 0, BreastsSmall at most 30 -- tests/test_pool.py holds it."""

FEMALE = {
    'beautiful': {
        'Hourglass': (1, {'Breasts': (20, 40), '7B Upper': (10, 25), 'BreastPerkiness': (10, 30), 'PushUp': (0, 20),
                          'Hips': (10, 25), 'Butt': (15, 30), 'RoundAss': (20, 50), 'ChubbyWaist': (5, 15), 'Thighs': (5, 15)}),
        'Athletic': (1, {'MuscularArms': (25, 45), 'MuscularLegs': (30, 50), 'MuscularButt': (40, 70), 'BreastsSmall': (10, 30),
                         'Breasts': (0, 15), 'ChestWidth': (5, 20), 'ChubbyWaist': (10, 20), 'Butt': (10, 25),
                         'BreastPerkiness': (20, 40), 'RoundAss': (20, 40)}),
        'Slender': (1, {'LegsThin': (10, 25), 'Arms': (5, 15), 'BreastsSmall': (0, 20), 'Breasts': (10, 20),
                        'BreastPerkiness': (20, 40), 'ChubbyWaist': (5, 15), 'Hips': (5, 15), 'Butt': (5, 15), 'SlimThighs': (0, 15)}),
        'Voluptuous': (1, {'7B Upper': (25, 45), 'Breasts': (30, 50), 'BreastGravity2': (5, 15), 'Hips': (20, 35),
                           'BigButt': (20, 40), 'Thighs': (20, 35), 'ChubbyWaist': (10, 20), 'ChubbyArms': (5, 15), 'AppleCheeks': (10, 30)}),
        'Petite': (1, {'BreastsSmall': (20, 30), 'Breasts': (0, 15), 'BreastPerkiness': (20, 40), 'SlimThighs': (10, 25),
                       'Arms': (10, 20), 'LegsThin': (5, 15), 'RoundAss': (20, 40), 'ChubbyWaist': (0, 10), 'Hips': (0, 10)}),
        'Pear': (1, {'BreastsSmall': (10, 25), 'Hips': (25, 40), 'Thighs': (30, 45), 'AppleCheeks': (30, 50), 'Butt': (20, 35),
                     'ChubbyWaist': (5, 15), 'ChubbyButt': (10, 25)}),
    },
    'middle': {
        'Average': (3, {'ChubbyWaist': (60, 90), 'WideWaistLine': (30, 60), 'HipUpperWidth': (20, 40), 'Belly': (20, 45),
                        'Breasts': (0, 20), 'BreastGravity2': (20, 40), 'Hips': (-10, 10), 'Butt': (-10, 10), 'Thighs': (0, 15),
                        'ChubbyArms': (5, 25), 'BreastsSmall': (0, 25)}),
        'Soft': (3, {'ChubbyWaist': (70, 100), 'Belly': (40, 60), 'BigBelly': (15, 35), 'WideWaistLine': (20, 40), 'ChubbyArms': (25, 45),
                     'ChubbyLegs': (15, 35), 'Breasts': (10, 30), 'BreastGravity2': (30, 50), 'ChubbyButt': (10, 25), 'Back': (15, 30)}),
        'Lean': (3, {'LegsThin': (10, 30), 'Arms': (10, 25), 'BreastsSmall': (15, 30), 'ButtSmall': (15, 35), 'ChubbyWaist': (55, 80),
                     'WideWaistLine': (40, 70), 'HipUpperWidth': (20, 40), 'BreastGravity2': (10, 25), 'Hips': (-20, 0)}),
        'Sturdy': (3, {'BigTorso': (20, 35), 'Back': (25, 45), 'ChestWidth': (15, 35), 'ChubbyWaist': (55, 80), 'WideWaistLine': (20, 40),
                       'MuscularLegs': (10, 30), 'MuscularArms': (10, 30), 'Thighs': (10, 25), 'Hips': (-10, 5), 'ButtSmall': (0, 20),
                       'Breasts': (0, 20)}),
        'Busty': (3, {'Breasts': (25, 45), '7B Upper': (10, 25), 'BreastGravity2': (35, 55), 'ChubbyWaist': (55, 85), 'Belly': (20, 40),
                      'WideWaistLine': (20, 40), 'Hips': (-5, 10), 'ChubbyArms': (10, 25)}),
        'WideHips': (3, {'Hips': (15, 30), 'Thighs': (20, 35), 'ChubbyLegs': (10, 25), 'ChubbyButt': (15, 30), 'ChubbyWaist': (60, 85),
                         'HipUpperWidth': (20, 40), 'Belly': (15, 30), 'BreastsSmall': (10, 30), 'BreastGravity2': (15, 35)}),
    },
    'ugly': {
        'Obese': (3, {'ChubbyWaist': (110, 140), 'BigBelly': (25, 50), 'Belly': (90, 120), 'HipUpperWidth': (60, 90),
                      'WideWaistLine': (60, 100), 'ChubbyLegs': (80, 110), 'ChubbyArms': (90, 120), 'ChubbyButt': (60, 90),
                      'BigTorso': (40, 70), 'Back': (50, 80), 'Breasts': (40, 60), 'BreastGravity2': (70, 90),
                      'BreastFlatness2': (20, 40), 'Thighs': (40, 60), 'CalfSize': (40, 70)}),
        'Flat': (3, {'Breasts': (0, 5), 'BreastsSmall': (20, 30), 'BreastsSmall2': (40, 70), 'BreastFlatness2': (50, 80),
                     'ButtSmall': (60, 90), 'Hips': (-50, -35), 'SlimThighs': (20, 40), 'ChubbyWaist': (70, 100),
                     'WideWaistLine': (50, 80), 'HipUpperWidth': (30, 50)}),
        'Frail': (2, {'LegsThin': (70, 100), 'Arms': (60, 90), 'SlimThighs': (50, 70), 'ButtSmall': (60, 80), 'BreastsSmall': (20, 30),
                      'Breasts': (0, 5), 'BreastGravity2': (40, 60), 'Hips': (-40, -25), 'CalfSmooth': (40, 70), 'WideWaistLine': (20, 40)}),
        'Apple': (3, {'BigBelly': (30, 55), 'Belly': (90, 120), 'ChubbyWaist': (110, 140), 'WideWaistLine': (40, 70),
                      'HipUpperWidth': (40, 70), 'Back': (40, 60),
                      'LegsThin': (30, 50), 'ButtSmall': (40, 60), 'SlimThighs': (10, 30), 'Breasts': (10, 30), 'BreastGravity2': (60, 90),
                      'ChubbyArms': (40, 60)}),
        'Saggy': (2, {'BreastGravity2': (90, 120), 'BreastFlatness2': (60, 90), 'Breasts': (20, 45), 'Belly': (40, 60), 'BigBelly': (20, 40),
                      'ChubbyWaist': (70, 90), 'ButtSmall': (30, 50), 'WideWaistLine': (30, 50)}),
        'BottomHeavy': (2, {'ChubbyLegs': (90, 120), 'Thighs': (60, 90), 'Hips': (50, 70), 'BigButt': (40, 70), 'ChubbyButt': (50, 80),
                            'BreastsSmall': (20, 30), 'Breasts': (0, 5), 'Arms': (15, 30), 'ChubbyWaist': (50, 70)}),
        'Boxy': (2, {'BigTorso': (50, 80), 'ChestWidth': (60, 90), 'Back': (50, 80), 'ChubbyWaist': (80, 110), 'WideWaistLine': (70, 100),
                     'HipUpperWidth': (40, 60), 'Hips': (-55, -40), 'ButtSmall': (50, 70), 'BreastsSmall': (20, 30), 'MuscularArms': (20, 40)}),
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
