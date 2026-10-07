import copy
import logging
import math
import pandas
from matplotlib import pyplot as plt
from py_ballisticcalc import TableG7, TableG1
from py_ballisticcalc import Ammo, Atmo, Wind, TrajFlag
from py_ballisticcalc import Weapon, Shot, Calculator
from py_ballisticcalc import PreferredUnits
from py_ballisticcalc.drag_model import *
from py_ballisticcalc.unit import *
from py_ballisticcalc.logger import logger
logger.setLevel(logging.WARNING)
PreferredUnits.adjustment = Angular.MOA

print("Default units:\n"+str(PreferredUnits))  # Print default units

# Establish 100-yard zero for a standard .308, G7 BC=0.22, muzzle velocity 2600fps
zero = Shot(weapon=Weapon(sight_height=Distance.Inch(3)), ammo=Ammo(DragModel(0.21, TableG7), mv=Velocity.FPS(2650)))
calc = Calculator()
zero_distance = Distance.Yard(100)
zero_elevation = calc.set_weapon_zero(zero, zero_distance)
print(f'Barrel elevation for {zero_distance} zero: {zero_elevation << PreferredUnits.adjustment}')

# Plot trajectory out to 500 yards
shot_result = calc.fire(zero, trajectory_range=Distance.Yard(1000),
                        trajectory_step=Distance.Yard(10), flags=TrajFlag.ALL)
ax = shot_result.plot()

# Turn on minor ticks if you want finer grid intervals
ax.minorticks_on()

# Enable dashed grid for major and minor ticks
ax.grid(which='major', linestyle='--', linewidth=0.8, color='gray')
ax.grid(which='minor', linestyle=':', linewidth=0.4, color='lightgray')

# Find danger space for a half-meter tall target at 300 yards
danger_space = shot_result.danger_space(Distance.Yard(300), Distance.Meter(.5))
print(danger_space)
danger_space.overlay(ax)  # Highlight danger space on the plot
plt.grid(True, linestyle='--')
plt.show()

## 308 example

# # Establish 100-yard zero for a standard .308, G7 BC=0.22, muzzle velocity 2600fps
# zero = Shot(weapon=Weapon(sight_height=Distance.Inch(2)), ammo=Ammo(DragModel(0.22, TableG7), mv=Velocity.FPS(2600)))
# calc = Calculator()
# zero_distance = Distance.Yard(100)
# zero_elevation = calc.set_weapon_zero(zero, zero_distance)
# print(f'Barrel elevation for {zero_distance} zero: {zero_elevation << PreferredUnits.adjustment}')
#
# # Plot trajectory out to 500 yards
# shot_result = calc.fire(zero, trajectory_range=Distance.Yard(500),
#                         trajectory_step=Distance.Yard(10), flags=TrajFlag.ALL)
# ax = shot_result.plot()
# # Find danger space for a half-meter tall target at 300 yards
# danger_space = shot_result.danger_space(Distance.Yard(300), Distance.Meter(.5))
# print(danger_space)
# danger_space.overlay(ax)  # Highlight danger space on the plot
# plt.show()
