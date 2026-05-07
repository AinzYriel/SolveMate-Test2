"""Utility functions for physics calculator: units, formatting, steps."""

import math
from formulas import physics_library

# Unit conversion factors (SI base)
CONVERSION_FACTORS = {
    # Speed
    'km/h': 1 / 3.6,
    # Mass
    'g': 0.001,
    'lb': 0.453592,
    # Voltage
    'mV': 0.001,
    'kV': 1000,
    # Current
    'mA': 0.001,
    # Resistance
    'kΩ': 1000,
    'MΩ': 1e6,
    # Length
    'cm': 0.01,
    'ft': 0.3048,
    'nm': 1e-9,
    'mm': 0.001,
    # Frequency
    'kHz': 1000,
    # Time
    'ms': 0.001,
    'min': 60,
    # Acceleration
    'g-force': 9.80665
}


def normalize(val, unit):
    """Convert input value to SI units."""
    if unit == 'deg':
        return math.radians(float(val))
    factor = CONVERSION_FACTORS.get(unit, 1.0)
    return float(val) * factor


def denormalize(val, unit):
    """Convert SI value back to display units."""
    if unit == 'deg':
        return math.degrees(val)
    factor = CONVERSION_FACTORS.get(unit, 1.0)
    return val * factor


def format_value(val, decimals=3):
    """Format value for display with proper scientific notation."""
    if abs(val) == 0:
        return "0"

    if abs(val) < 0.001 or abs(val) > 10000:
        formatted = f"{val:.{decimals - 1}e}"
        mantissa, exponent = formatted.split('e')
        exp_val = int(exponent)
        exp_sign = '⁻' if exp_val < 0 else ''
        exp_abs = abs(exp_val)
        superscript_map = '⁰¹²³⁴⁵⁶⁷⁸⁹'
        superscript = ''.join(superscript_map[int(d)] for d in str(exp_abs))
        return f"{mantissa} × 10<span style='font-size:0.7em;vertical-align:super'>{exp_sign}{superscript}</span>"

    return f"{float(val):.{decimals}g}"


def generate_detailed_steps(fid, target, v_normalized, v_display, units, res_normalized, res_display):
    """Generate detailed, educational step-by-step solution."""
    steps = []
    step_num = 1

    # Step 1: Identify formula
    formula_eq = next((f['equation'] for cat in physics_library.values() for f in cat if f['id'] == fid), "Formula")
    steps.append(f"Step {step_num}: Use the formula: <strong>{formula_eq}</strong>")
    step_num += 1

    # Specific step-by-step for key formulas (KEEP ALL EXISTING LOGIC)
    if fid == 'v_final':
        if target == 'v':
            steps.append(
                f"Step {step_num}: v = {format_value(v_display['u'])} + {format_value(v_display['a'])} × {format_value(v_display['t'])}")
            step_num += 1
            steps.append(
                f"Step {step_num}: {format_value(v_display['a'])} × {format_value(v_display['t'])} = {format_value(v_display['a'] * v_display['t'])}")
            step_num += 1
            steps.append(
                f"Step {step_num}: {format_value(v_display['u'])} + {format_value(v_display['a'] * v_display['t'])} = <strong>{format_value(res_display)}</strong>")
        elif target == 'a':
            steps.append(
                f"Step {step_num}: a = ({format_value(v_display['v'])} - {format_value(v_display['u'])}) / {format_value(v_display['t'])}")
            step_num += 1
            steps.append(
                f"Step {step_num}: ({format_value(v_display['v'])} - {format_value(v_display['u'])}) / {format_value(v_display['t'])} = <strong>{format_value(res_display)}</strong>")

    elif fid == 'f_ma':
        if target == 'F':
            steps.append(
                f"Step {step_num}: F = {format_value(v_display['m'])} × {format_value(v_display['a'])} = <strong>{format_value(res_display)}</strong>")
        elif target == 'a':
            steps.append(
                f"Step {step_num}: a = {format_value(v_display['F'])} / {format_value(v_display['m'])} = <strong>{format_value(res_display)}</strong>")

    elif fid == 'kinetic_e':
        if target == 'KE':
            steps.append(
                f"Step {step_num}: KE = ½ × {format_value(v_display['m'])} × ({format_value(v_display['v'])})<sup>2</sup> = <strong>{format_value(res_display)}</strong>")

    # Generic fallback
    else:
        steps.append(f"Step {step_num}: Substitute known values to solve for <strong>{target}</strong>")
        step_num += 1
        steps.append(f"Step {step_num}: <strong>Result: {format_value(res_display)} {units[target]}</strong>")

    return steps


def generate_tutor_explanation(fid, target, v_normalized, v_display, units, res_normalized, res_display):
    """Generate TUTOR-LEVEL detailed explanation with physics concepts."""
    explanation = []

    # Step 1: Formula + Why it applies
    formula = get_formula_by_id(fid)
    explanation.append(f"🧠 <strong>Formula:</strong> {formula['equation']}")
    explanation.append(f"📚 <strong>Why this formula:</strong> {formula['desc']}")
    explanation.append(
        f"🎯 <strong>Solving for:</strong> {formula['vars'][[v['name'] for v in formula['vars']].index(target)]['label']}")
    explanation.append("")

    # Step 2: Variable meanings + assumptions
    explanation.append("📖 <strong>Variable Meanings & Assumptions:</strong>")
    var_info = []
    for var in formula['vars']:
        if var['name'] in v_display or var['name'] == target:
            value = f"{format_value(v_display.get(var['name'], res_display))} {units.get(var['name'], units.get(target, ''))}"
            var_info.append(f"• {var['symbol']} = {value} ({var['label']})")
    explanation.extend(var_info)
    explanation.append("")

    # Step 3: Detailed step-by-step with physics reasoning
    explanation.append("🔢 <strong>Detailed Calculation:</strong>")

    if fid == 'v_final':
        if target == 'v':
            explanation.extend([
                f"1. This is the first kinematic equation for <strong>constant acceleration</strong>",
                f"2. Acceleration × Time = {format_value(v_display['a'])} × {format_value(v_display['t'])} = {format_value(v_display['a'] * v_display['t'])} {units['a'].replace('m/s²', 'm/s')}",
                f"3. Add initial velocity: {format_value(v_display['u'])} + {format_value(v_display['a'] * v_display['t'])} = <strong>{format_value(res_display)}</strong> {units[target]}",
                ""
            ])
        elif target == 'a':
            explanation.extend([
                f"1. Rearrange: a = (v - u) / t",
                f"2. Change in velocity: {format_value(v_display['v'])} - {format_value(v_display['u'])} = {format_value(v_display['v'] - v_display['u'])}",
                f"3. Divide by time: {format_value(v_display['v'] - v_display['u'])} / {format_value(v_display['t'])} = <strong>{format_value(res_display)}</strong>",
                ""
            ])

    elif fid == 'f_ma':
        explanation.extend([
            f"1. Newton's 2nd Law: Force causes acceleration proportional to mass",
            f"2. F = m × a = {format_value(v_display['m'])} × {format_value(v_display['a'])} = <strong>{format_value(res_display)}</strong> N",
            f"3. 1 Newton = 1 kg·m/s² (SI unit definition)",
            ""
        ])

    elif fid == 'kinetic_e':
        explanation.extend([
            f"1. Kinetic energy from ½mv² (work-energy theorem)",
            f"2. v² = ({format_value(v_display['v'])})<sup>2</sup> = {format_value(v_display['v'] ** 2)}",
            f"3. ½ × {format_value(v_display['m'])} × {format_value(v_display['v'] ** 2)} = <strong>{format_value(res_display)}</strong> J",
            f"4. Joule = kg·m²/s² (energy unit)",
            ""
        ])

    elif fid == 'ohm':
        explanation.extend([
            f"1. Ohm's Law: V = IR (linear relationship)",
            f"2. Resistance opposes current flow",
            f"3. {format_value(v_display['I'])} A × {format_value(v_display['R'])} Ω = <strong>{format_value(res_display)}</strong> V",
            f"4. Volt = Joule/Coulomb (energy per charge)",
            ""
        ])

    # Generic fallback with rich explanation
    else:
        explanation.extend([
            f"1. Rearranged {formula['equation']} to solve for {target}",
            f"2. All values converted to consistent SI units first",
            f"3. Calculated: <strong>{format_value(res_display)} {units[target]}</strong>",
            ""
        ])

    # Step 4: Physics interpretation + real-world meaning
    explanation.append("🌍 <strong>Physics Interpretation:</strong>")
    interpretations = {
        'v_final': "Object reaches this speed after constant acceleration. Used in cars, rockets, falling objects.",
        'f_ma': "Net force determines acceleration. More mass = harder to accelerate.",
        'kinetic_e': "Total energy of motion. Converts to heat/sound in crashes.",
        'ohm': "Higher resistance = lower current for same voltage (circuit design).",
        'range': "Maximum horizontal distance for projectiles (45° is optimal)."
    }
    interp = interpretations.get(fid, "This result follows fundamental physics conservation laws.")
    explanation.append(f"• {interp}")

    explanation.append("")
    explanation.append(
        f"✅ <strong>Final Answer:</strong> <span style='font-size:1.3em'>{format_value(res_display)} {units[target]}</span>")

    return explanation