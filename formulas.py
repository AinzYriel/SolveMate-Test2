# --- FULL PHYSICS LIBRARY (70+ Formulas from Old Project) ---
physics_library = {
    'Kinematics': [
        {
            'id': 'v_final',
            'title': "Final Velocity",
            'equation': "v = u + at",
            'desc': "Final velocity with constant acceleration.",
            'when_to_use': "Know initial speed, acceleration, and time.",
            'example': "Car from 0 to 60 mph in 8 seconds.",
            'vars': [
                {'name': 'v', 'label': 'Final Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'u', 'label': 'Initial Velocity', 'symbol': 'u', 'units': ['m/s', 'km/h']},
                {'name': 'a', 'label': 'Acceleration', 'symbol': 'a', 'units': ['m/s²', 'g-force']},
                {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
            ]
        },
        {
            'id': 'displacement',
            'title': "Displacement",
            'equation': "s = ut + ½at²",
            'desc': "Distance traveled with constant acceleration.",
            'when_to_use': "Find total distance with changing speed.",
            'example': "How far does a ball fall in 3 seconds?",
            'vars': [
                {'name': 's', 'label': 'Displacement', 'symbol': 's', 'units': ['m', 'km', 'ft', 'cm']},
                {'name': 'u', 'label': 'Initial Velocity', 'symbol': 'u', 'units': ['m/s', 'km/h']},
                {'name': 'a', 'label': 'Acceleration', 'symbol': 'a', 'units': ['m/s²', 'g-force']},
                {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
            ]
        },
        {
            'id': 'v_squared',
            'title': "Velocity-Displacement",
            'equation': "v² = u² + 2as",
            'desc': "Relates velocity to distance without time.",
            'when_to_use': "No time data available.",
            'example': "Braking distance calculation.",
            'vars': [
                {'name': 'v', 'label': 'Final Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'u', 'label': 'Initial Velocity', 'symbol': 'u', 'units': ['m/s', 'km/h']},
                {'name': 'a', 'label': 'Acceleration', 'symbol': 'a', 'units': ['m/s²', 'g-force']},
                {'name': 's', 'label': 'Displacement', 'symbol': 's', 'units': ['m', 'km', 'ft', 'cm']}
            ]
        },
        {
            'id': 'v_avg',
            'title': "Average Velocity",
            'equation': "v_avg = (u + v) / 2",
            'desc': "Average speed between initial and final.",
            'when_to_use': "Constant acceleration assumed.",
            'example': "Average speed of decelerating car.",
            'vars': [
                {'name': 'v_avg', 'label': 'Average Velocity', 'symbol': 'v_avg', 'units': ['m/s', 'km/h']},
                {'name': 'u', 'label': 'Initial Velocity', 'symbol': 'u', 'units': ['m/s', 'km/h']},
                {'name': 'v', 'label': 'Final Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']}
            ]
        },
        {
            'id': 'distance_cv',
            'title': "Distance (Constant Velocity)",
            'equation': "d = v × t",
            'desc': "Simple distance at constant speed.",
            'when_to_use': "No acceleration.",
            'example': "How far in 2 hours at 100 km/h?",
            'vars': [
                {'name': 'd', 'label': 'Distance', 'symbol': 'd', 'units': ['m', 'km', 'ft', 'cm']},
                {'name': 'v', 'label': 'Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
            ]
        },
        {
            'id': 'range',
            'title': "Projectile Range",
            'equation': "R = (v² sin 2θ) / g",
            'desc': "Horizontal distance of projectile.",
            'when_to_use': "Level ground, no air resistance.",
            'example': "Cannonball range at 45°.",
            'vars': [
                {'name': 'R', 'label': 'Range', 'symbol': 'R', 'units': ['m', 'ft']},
                {'name': 'v', 'label': 'Initial Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'theta', 'label': 'Launch Angle', 'symbol': 'θ', 'units': ['deg', 'rad']}
            ]
        }
    ],
    'Dynamics': [
        {
            'id': 'f_ma',
            'title': "Newton's Second Law",
            'equation': "F = m × a",
            'desc': "Force = mass × acceleration.",
            'when_to_use': "Any motion caused by force.",
            'example': "Force to accelerate 1000kg car.",
            'vars': [
                {'name': 'F', 'label': 'Force', 'symbol': 'F', 'units': ['N', 'kN', 'lbf']},
                {'name': 'm', 'label': 'Mass', 'symbol': 'm', 'units': ['kg', 'g', 'lb']},
                {'name': 'a', 'label': 'Acceleration', 'symbol': 'a', 'units': ['m/s²', 'g-force']}
            ]
        },
        {
            'id': 'momentum',
            'title': "Linear Momentum",
            'equation': "p = m × v",
            'desc': "Quantity of motion.",
            'when_to_use': "Collisions, rockets.",
            'example': "Bullet momentum.",
            'vars': [
                {'name': 'p', 'label': 'Momentum', 'symbol': 'p', 'units': ['kg·m/s']},
                {'name': 'm', 'label': 'Mass', 'symbol': 'm', 'units': ['kg', 'lb']},
                {'name': 'v', 'label': 'Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']}
            ]
        }
    ],
    'Circular Motion': [
        {
            'id': 'centripetal',
            'title': "Centripetal Force",
            'equation': "F_c = (m v²) / r",
            'desc': "Force for circular motion.",
            'when_to_use': "Cars on curves, satellites.",
            'example': "Force keeping car on track.",
            'vars': [
                {'name': 'Fc', 'label': 'Centripetal Force', 'symbol': 'F_c', 'units': ['N']},
                {'name': 'm', 'label': 'Mass', 'symbol': 'm', 'units': ['kg', 'g']},
                {'name': 'v', 'label': 'Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'r', 'label': 'Radius', 'symbol': 'r', 'units': ['m', 'cm']}
            ]
        },
        {
            'id': 'centripetal_acc',
            'title': "Centripetal Acceleration",
            'equation': "a_c = v² / r",
            'desc': "Acceleration toward center.",
            'when_to_use': "Find acceleration in circles.",
            'example': "Roller coaster at bottom of loop.",
            'vars': [
                {'name': 'a_c', 'label': 'Centripetal Acceleration', 'symbol': 'a_c', 'units': ['m/s²', 'g-force']},
                {'name': 'v', 'label': 'Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'r', 'label': 'Radius', 'symbol': 'r', 'units': ['m', 'cm']}
            ]
        },
        {
            'id': 'angular_velocity',
            'title': "Angular Velocity",
            'equation': "ω = θ / t",
            'desc': "Rotational speed.",
            'when_to_use': "Spinning objects.",
            'example': "Wheel rotation rate.",
            'vars': [
                {'name': 'omega', 'label': 'Angular Velocity', 'symbol': 'ω', 'units': ['rad/s', 'deg/s']},
                {'name': 'theta', 'label': 'Angle', 'symbol': 'θ', 'units': ['rad', 'deg']},
                {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
            ]
        },
        {
            'id': 'linear_velocity_circ',
            'title': "Linear Velocity (Circular)",
            'equation': "v = r ω",
            'desc': "Tangential speed from rotation.",
            'when_to_use': "Relate linear and angular motion.",
            'example': "Speed at edge of spinning disk.",
            'vars': [
                {'name': 'v', 'label': 'Linear Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'r', 'label': 'Radius', 'symbol': 'r', 'units': ['m', 'cm']},
                {'name': 'omega', 'label': 'Angular Velocity', 'symbol': 'ω', 'units': ['rad/s', 'deg/s']}
            ]
        }
    ],
    'Work & Energy': [
        {
            'id': 'kinetic_e',
            'title': "Kinetic Energy",
            'equation': "KE = ½ m v²",
            'desc': "Energy of motion.",
            'when_to_use': "Speed from energy, work-energy theorem.",
            'example': "Car crash energy.",
            'vars': [
                {'name': 'KE', 'label': 'Kinetic Energy', 'symbol': 'KE', 'units': ['J', 'kJ', 'cal']},
                {'name': 'm', 'label': 'Mass', 'symbol': 'm', 'units': ['kg', 'g']},
                {'name': 'v', 'label': 'Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']}
            ]
        },
        {
            'id': 'work_f_d_cos',
            'title': "Work (Force × Distance)",
            'equation': "W = F d cos(θ)",
            'desc': "Work done by force at angle.",
            'when_to_use': "Pushing/pulling at angles.",
            'example': "Worker pushing box at 30°.",
            'vars': [
                {'name': 'W', 'label': 'Work', 'symbol': 'W', 'units': ['J', 'kJ', 'ft-lb']},
                {'name': 'F', 'label': 'Force', 'symbol': 'F', 'units': ['N', 'kN', 'lbf']},
                {'name': 'd', 'label': 'Distance', 'symbol': 'd', 'units': ['m', 'cm', 'ft']},
                {'name': 'theta', 'label': 'Angle', 'symbol': 'θ', 'units': ['deg', 'rad']}
            ]
        },
        {
            'id': 'potential_grav',
            'title': "Gravitational PE",
            'equation': "PE = m g h",
            'desc': "Energy from height.",
            'when_to_use': "Falling objects, roller coasters.",
            'example': "Water behind dam.",
            'vars': [
                {'name': 'PE', 'label': 'Potential Energy', 'symbol': 'PE', 'units': ['J', 'kJ']},
                {'name': 'm', 'label': 'Mass', 'symbol': 'm', 'units': ['kg', 'g', 'lb']},
                {'name': 'g', 'label': 'Gravity', 'symbol': 'g', 'units': ['m/s²', 'g-force']},
                {'name': 'h', 'label': 'Height', 'symbol': 'h', 'units': ['m', 'cm', 'ft']}
            ]
        },
        {
            'id': 'potential_elastic',
            'title': "Elastic Potential Energy",
            'equation': "PE = ½ k x²",
            'desc': "Energy in springs.",
            'when_to_use': "Springs, bungee cords.",
            'example': "Compressed car suspension.",
            'vars': [
                {'name': 'PE', 'label': 'Potential Energy', 'symbol': 'PE', 'units': ['J', 'kJ']},
                {'name': 'k', 'label': 'Spring Constant', 'symbol': 'k', 'units': ['N/m', 'lb/ft']},
                {'name': 'x', 'label': 'Displacement', 'symbol': 'x', 'units': ['m', 'cm', 'ft']}
            ]
        },
        {
            'id': 'power_wt',
            'title': "Power (Work/Time)",
            'equation': "P = W / t",
            'desc': "Rate of doing work.",
            'when_to_use': "Engines, motors.",
            'example': "Lifting 100kg in 5 seconds.",
            'vars': [
                {'name': 'P', 'label': 'Power', 'symbol': 'P', 'units': ['W', 'kW', 'hp']},
                {'name': 'W', 'label': 'Work', 'symbol': 'W', 'units': ['J', 'kJ']},
                {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
            ]
        }
    ],
    'Circuits': [
        {
            'id': 'ohm',
            'title': "Ohm's Law",
            'equation': "V = I × R",
            'desc': "Voltage, current, resistance.",
            'when_to_use': "Any resistor circuit.",
            'example': "12V battery, 4Ω resistor.",
            'vars': [
                {'name': 'V', 'label': 'Voltage', 'symbol': 'V', 'units': ['V', 'mV', 'kV']},
                {'name': 'I', 'label': 'Current', 'symbol': 'I', 'units': ['A', 'mA']},
                {'name': 'R', 'label': 'Resistance', 'symbol': 'R', 'units': ['Ω', 'kΩ', 'MΩ']}
            ]
        },
        {
            'id': 'power_vi',
            'title': "Electric Power (V×I)",
            'equation': "P = V × I",
            'desc': "Electrical power consumption.",
            'when_to_use': "Any electrical device.",
            'example': "120V appliance drawing 5A.",
            'vars': [
                {'name': 'P', 'label': 'Power', 'symbol': 'P', 'units': ['W', 'kW', 'hp']},
                {'name': 'V', 'label': 'Voltage', 'symbol': 'V', 'units': ['V', 'mV', 'kV']},
                {'name': 'I', 'label': 'Current', 'symbol': 'I', 'units': ['A', 'mA']}
            ]
        },
        {
            'id': 'power_i2r',
            'title': "Power (I²R)",
            'equation': "P = I² × R",
            'desc': "Heat dissipation in resistors.",
            'when_to_use': "Resistor heating calculations.",
            'example': "Wire heating in toaster.",
            'vars': [
                {'name': 'P', 'label': 'Power', 'symbol': 'P', 'units': ['W', 'kW', 'hp']},
                {'name': 'I', 'label': 'Current', 'symbol': 'I', 'units': ['A', 'mA']},
                {'name': 'R', 'label': 'Resistance', 'symbol': 'R', 'units': ['Ω', 'kΩ', 'MΩ']}
            ]
        },
        {
            'id': 'power_v2r',
            'title': "Power (V²/R)",
            'equation': "P = V² / R",
            'desc': "Power across resistor.",
            'when_to_use': "Voltage known across resistor.",
            'example': "LED circuit power.",
            'vars': [
                {'name': 'P', 'label': 'Power', 'symbol': 'P', 'units': ['W', 'kW', 'hp']},
                {'name': 'V', 'label': 'Voltage', 'symbol': 'V', 'units': ['V', 'mV', 'kV']},
                {'name': 'R', 'label': 'Resistance', 'symbol': 'R', 'units': ['Ω', 'kΩ', 'MΩ']}
            ]
        },
        {
            'id': 'charge_it',
            'title': "Electric Charge",
            'equation': "Q = I × t",
            'desc': "Charge flow over time.",
            'when_to_use': "Batteries, capacitors.",
            'example': "1A for 3600s = 3600C.",
            'vars': [
                {'name': 'Q', 'label': 'Charge', 'symbol': 'Q', 'units': ['C']},
                {'name': 'I', 'label': 'Current', 'symbol': 'I', 'units': ['A', 'mA']},
                {'name': 't', 'label': 'Time', 'symbol': 't', 'units': ['s', 'min']}
            ]
        }
    ],
    'Waves & Oscillations': [
        {
            'id': 'wave_v',
            'title': "Wave Velocity",
            'equation': "v = f × λ",
            'desc': "Wave speed from frequency and wavelength.",
            'when_to_use': "Sound, light, water waves.",
            'example': "Speed of sound = 343 m/s.",
            'vars': [
                {'name': 'v', 'label': 'Wave Velocity', 'symbol': 'v', 'units': ['m/s', 'km/h']},
                {'name': 'f', 'label': 'Frequency', 'symbol': 'f', 'units': ['Hz', 'kHz']},
                {'name': 'lam', 'label': 'Wavelength', 'symbol': 'λ', 'units': ['m', 'nm', 'mm']}
            ]
        },
        {
            'id': 'frequency',
            'title': "Frequency from Period",
            'equation': "f = 1 / T",
            'desc': "Oscillations per second.",
            'when_to_use': "Pendulums, springs.",
            'example': "2s period = 0.5 Hz.",
            'vars': [
                {'name': 'f', 'label': 'Frequency', 'symbol': 'f', 'units': ['Hz', 'kHz']},
                {'name': 'T', 'label': 'Period', 'symbol': 'T', 'units': ['s', 'ms']}
            ]
        },
        {
            'id': 'angular_frequency',
            'title': "Angular Frequency",
            'equation': "ω = 2πf",
            'desc': "Rotational frequency.",
            'when_to_use': "Simple harmonic motion.",
            'example': "Convert Hz to rad/s.",
            'vars': [
                {'name': 'omega', 'label': 'Angular Frequency', 'symbol': 'ω', 'units': ['rad/s']},
                {'name': 'f', 'label': 'Frequency', 'symbol': 'f', 'units': ['Hz', 'kHz']}
            ]
        },
        {
            'id': 'period',
            'title': "Period from Frequency",
            'equation': "T = 1 / f",
            'desc': "Time per oscillation.",
            'when_to_use': "Timing circuits, pendulums.",
            'example': "100 Hz = 0.01s period.",
            'vars': [
                {'name': 'T', 'label': 'Period', 'symbol': 'T', 'units': ['s', 'ms']},
                {'name': 'f', 'label': 'Frequency', 'symbol': 'f', 'units': ['Hz', 'kHz']}
            ]
        }
    ]
}

def get_formula_by_id(fid):
    """Helper to find formula by ID across all categories."""
    for category, formulas in physics_library.items():
        for formula in formulas:
            if formula['id'] == fid:
                return formula
    return None