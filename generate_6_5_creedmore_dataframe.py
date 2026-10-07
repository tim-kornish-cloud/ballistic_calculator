import logging
from matplotlib import pyplot as plt
from py_ballisticcalc import PreferredUnits
from py_ballisticcalc import TableG7, TableG1
from py_ballisticcalc import (DragModel, Ammo, Weapon, Shot, Atmo, Vacuum, Wind,
                              Calculator, HitResult, TrajFlag, logger, BaseEngineConfigDict)
from py_ballisticcalc.unit import *
PreferredUnits.adjustment = Angular.MOA
PreferredUnits.drop_angle = Angular.MOA
PreferredUnits.windage_angle = Angular.MOA
logger.setLevel(logging.WARNING)

print("Default units:\n"+str(PreferredUnits))  # Print default units

# Establish 100-yard zero for a standard .308, G7 BC=0.22, muzzle velocity 2600fps
zero = Shot(weapon=Weapon(sight_height=Distance.Inch(3)), ammo=Ammo(DragModel(0.21, TableG7), mv=Velocity.FPS(2650)))
calc = Calculator()
zero_distance = Distance.Yard(100)
zero_elevation = calc.set_weapon_zero(zero, zero_distance)
print(f'Barrel elevation for {zero_distance} zero: {zero_elevation << PreferredUnits.adjustment}')


# Plot trajectory out to 500 yards
shot_result = calc.fire(zero, trajectory_range=Distance.Yard(500),
                        trajectory_step=Distance.Yard(10), flags=TrajFlag.ALL)
ax = shot_result.plot()
# Find danger space for a half-meter tall target at 300 yards
danger_space = shot_result.danger_space(Distance.Yard(300), Distance.Meter(.5))
print(danger_space)
danger_space.overlay(ax)  # Highlight danger space on the plot


# Range card for this zero with 5mph cross-wind from left to right
zero.winds = [Wind(Velocity.MPH(5), Angular.OClock(3))]
range_card = calc.fire(zero, trajectory_range=1000, trajectory_step=5)
# for p in range_card: print(p.formatted())
range_card.dataframe().to_clipboard()
df = range_card.dataframe(True).drop(['slant_height', 'mach', 'angle', 'slant_distance', 'density_ratio', 'drag', 'energy', 'ogw', 'flag'], axis=1).set_index('distance')

df.to_csv("range_card_5mph.csv")
