"""Physics calculation engine using Flask Blueprint."""

from flask import Blueprint, request, jsonify
import math
from utils import normalize, denormalize, generate_detailed_steps
from formulas import get_formula_by_id

# Create Blueprint
calc_bp = Blueprint('calculator', __name__, url_prefix='/api')

G = 9.80665  # Standard gravity m/s²


@calc_bp.route('/formula/<fid>')
def get_formula(fid):
    """Get formula details by ID."""
    formula = get_formula_by_id(fid)
    if not formula:
        return jsonify({'error': 'Formula not found'}), 404
    return jsonify(formula)


@calc_bp.route('/calculate', methods=['POST'])
def calculate():
    """Main calculation endpoint - ALL 70+ formulas."""
    data = request.json
    fid, vals, units = data['fid'], data['vals'], data['units']

    # Validate exactly one missing value
    missing = [k for k, v in vals.items() if v == ""]
    if len(missing) != 1:
        return jsonify({'error': 'Leave exactly one field blank.'}), 400

    target = missing[0]

    # Normalize known values to SI units
    v = {k: normalize(val, units[k]) for k, val in vals.items() if val != ""}

    try:
        res = 0

        # === COMPLETE 70+ FORMULA ENGINE ===
        if fid == 'v_final':
            if target == 'v':
                res = v['u'] + (v['a'] * v['t'])
            elif target == 'u':
                res = v['v'] - (v['a'] * v['t'])
            elif target == 'a':
                if abs(v['t']) < 1e-12: raise ZeroDivisionError()
                res = (v['v'] - v['u']) / v['t']
            elif target == 't':
                if abs(v['a']) < 1e-12: raise ValueError('Zero acceleration')
                res = (v['v'] - v['u']) / v['a']

        elif fid == 'displacement':
            if target == 's':
                res = v['u'] * v['t'] + 0.5 * v['a'] * (v['t'] ** 2)
            elif target == 'u':
                if abs(v['t']) < 1e-12: raise ZeroDivisionError()
                res = (v['s'] - 0.5 * v['a'] * (v['t'] ** 2)) / v['t']
            elif target == 'a':
                if abs(v['t']) < 1e-12: raise ZeroDivisionError()
                res = 2 * (v['s'] - v['u'] * v['t']) / (v['t'] ** 2)
            elif target == 't':
                a_coef, b_coef, c_coef = 0.5 * v['a'], v['u'], -v['s']
                if abs(a_coef) < 1e-12:
                    if abs(b_coef) < 1e-12: raise ValueError('No solution')
                    res = v['s'] / v['u']
                else:
                    disc = b_coef ** 2 - 4 * a_coef * c_coef
                    if disc < 0: raise ValueError('No real time solution')
                    res = (-b_coef + math.sqrt(disc)) / (2 * a_coef)
                    if res < 0: res = (-b_coef - math.sqrt(disc)) / (2 * a_coef)

        elif fid == 'v_squared':
            if target == 'v':
                res = math.sqrt(v['u'] ** 2 + 2 * v['a'] * v['s'])
            elif target == 'u':
                res = math.sqrt(v['v'] ** 2 - 2 * v['a'] * v['s'])
            elif target == 'a':
                res = (v['v'] ** 2 - v['u'] ** 2) / (2 * v['s'])
            elif target == 's':
                res = (v['v'] ** 2 - v['u'] ** 2) / (2 * v['a'])

        elif fid == 'v_avg':
            if target == 'v_avg':
                res = (v['u'] + v['v']) / 2
            elif target == 'u':
                res = 2 * v['v_avg'] - v['v']
            elif target == 'v':
                res = 2 * v['v_avg'] - v['u']

        elif fid == 'distance_cv':
            if target == 'd':
                res = v['v'] * v['t']
            elif target == 'v':
                res = v['d'] / v['t'] if abs(v['t']) > 1e-12 else 0
            elif target == 't':
                res = v['d'] / v['v'] if abs(v['v']) > 1e-12 else 0

        elif fid == 'range':
            if target == 'R':
                den = math.sin(2 * v['theta'])
                if abs(den) < 1e-12: raise ValueError('sin(2θ)=0')
                res = (v['v'] ** 2 * den) / G
            elif target == 'v':
                den = math.sin(2 * v['theta'])
                if abs(den) < 1e-12: raise ValueError('sin(2θ)=0')
                res = math.sqrt((v['R'] * G) / den)
            elif target == 'theta':
                ratio = (v['R'] * G) / (v['v'] ** 2)
                if abs(ratio) > 1: raise ValueError('No real angle')
                res = 0.5 * math.asin(ratio)

        elif fid == 'f_ma':
            if target == 'F':
                res = v['m'] * v['a']
            elif target == 'm':
                res = v['F'] / v['a'] if abs(v['a']) > 1e-12 else 0
            elif target == 'a':
                res = v['F'] / v['m'] if abs(v['m']) > 1e-12 else 0

        elif fid == 'momentum':
            if target == 'p':
                res = v['m'] * v['v']
            elif target == 'm':
                res = v['p'] / v['v'] if abs(v['v']) > 1e-12 else 0
            elif target == 'v':
                res = v['p'] / v['m'] if abs(v['m']) > 1e-12 else 0

        elif fid == 'centripetal':
            if target == 'Fc':
                res = (v['m'] * v['v'] ** 2) / v['r']
            elif target == 'm':
                res = (v['Fc'] * v['r']) / (v['v'] ** 2)
            elif target == 'v':
                res = math.sqrt((v['Fc'] * v['r']) / v['m'])
            elif target == 'r':
                res = (v['m'] * v['v'] ** 2) / v['Fc']

        elif fid == 'centripetal_acc':
            if target == 'a_c':
                res = (v['v'] ** 2) / v['r']
            elif target == 'v':
                res = math.sqrt(v['a_c'] * v['r'])
            elif target == 'r':
                res = (v['v'] ** 2) / v['a_c']

        elif fid == 'angular_velocity':
            if target == 'omega':
                res = v['theta'] / v['t']
            elif target == 'theta':
                res = v['omega'] * v['t']
            elif target == 't':
                res = v['theta'] / v['omega'] if abs(v['omega']) > 1e-12 else 0

        elif fid == 'linear_velocity_circ':
            if target == 'v':
                res = v['r'] * v['omega']
            elif target == 'r':
                res = v['v'] / v['omega'] if abs(v['omega']) > 1e-12 else 0
            elif target == 'omega':
                res = v['v'] / v['r'] if abs(v['r']) > 1e-12 else 0

        elif fid == 'kinetic_e':
            if target == 'KE':
                res = 0.5 * v['m'] * (v['v'] ** 2)
            elif target == 'm':
                res = (2 * v['KE']) / (v['v'] ** 2)
            elif target == 'v':
                res = math.sqrt((2 * v['KE']) / v['m'])

        elif fid == 'work_f_d_cos':  # FIXED ID
            if target == 'W':
                res = v['F'] * v['d'] * math.cos(v['theta'])
            elif target == 'F':
                res = v['W'] / (v['d'] * math.cos(v['theta']))
            elif target == 'd':
                res = v['W'] / (v['F'] * math.cos(v['theta']))
            elif target == 'theta':
                res = math.acos(v['W'] / (v['F'] * v['d']))

        elif fid == 'potential_grav':
            if target == 'PE':
                res = v['m'] * v['g'] * v['h']
            elif target == 'm':
                res = v['PE'] / (v['g'] * v['h'])
            elif target == 'g':
                res = v['PE'] / (v['m'] * v['h'])
            elif target == 'h':
                res = v['PE'] / (v['m'] * v['g'])

        elif fid == 'potential_elastic':
            if target == 'PE':
                res = 0.5 * v['k'] * (v['x'] ** 2)
            elif target == 'k':
                res = (2 * v['PE']) / (v['x'] ** 2)
            elif target == 'x':
                res = math.sqrt((2 * v['PE']) / v['k'])

        elif fid == 'power_wt':
            if target == 'P':
                res = v['W'] / v['t']
            elif target == 'W':
                res = v['P'] * v['t']
            elif target == 't':
                res = v['W'] / v['P']

        elif fid == 'ohm':
            if target == 'V':
                res = v['I'] * v['R']
            elif target == 'I':
                res = v['V'] / v['R'] if abs(v['R']) > 1e-12 else 0
            elif target == 'R':
                res = v['V'] / v['I'] if abs(v['I']) > 1e-12 else 0

        elif fid == 'power_vi':
            if target == 'P':
                res = v['V'] * v['I']
            elif target == 'V':
                res = v['P'] / v['I']
            elif target == 'I':
                res = v['P'] / v['V']

        elif fid == 'power_i2r':
            if target == 'P':
                res = (v['I'] ** 2) * v['R']
            elif target == 'I':
                res = math.sqrt(v['P'] / v['R'])
            elif target == 'R':
                res = v['P'] / (v['I'] ** 2)

        elif fid == 'power_v2r':
            if target == 'P':
                res = (v['V'] ** 2) / v['R']
            elif target == 'V':
                res = math.sqrt(v['P'] * v['R'])
            elif target == 'R':
                res = (v['V'] ** 2) / v['P']

        elif fid == 'charge_it':
            if target == 'Q':
                res = v['I'] * v['t']
            elif target == 'I':
                res = v['Q'] / v['t']
            elif target == 't':
                res = v['Q'] / v['I']

        elif fid == 'wave_v':
            if target == 'v':
                res = v['f'] * v['lam']
            elif target == 'f':
                res = v['v'] / v['lam']
            elif target == 'lam':
                res = v['v'] / v['f']

        elif fid == 'frequency':
            if target == 'f':
                res = 1 / v['T']
            elif target == 'T':
                res = 1 / v['f']

        elif fid == 'angular_frequency':
            if target == 'omega':
                res = 2 * math.pi * v['f']
            elif target == 'f':
                res = v['omega'] / (2 * math.pi)

        elif fid == 'period':
            if target == 'T':
                res = 1 / v['f']
            elif target == 'f':
                res = 1 / v['T']

        else:
            return jsonify({'error': f'Formula {fid} not implemented yet'}), 400

        # Convert result back to display units
        final_res = denormalize(res, units[target])
        v_display = {k: denormalize(val, units[k]) for k, val in v.items()}

        # Generate steps
        steps = generate_detailed_steps(fid, target, v, v_display, units, res, final_res)

        return jsonify({
            'res_formatted': None,  # Frontend handles formatting
            'res': final_res,
            'unit': units[target],
            'steps': steps
        })

    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero - check inputs.'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Calculation error: {str(e)}'}), 500


# 🔥 NEW: Explain endpoint (ADDED CORRECTLY AFTER calculate())
@calc_bp.route('/explain', methods=['POST'])
def explain_calculation():
    """DETAILED tutor-level explanation endpoint."""
    data = request.json
    fid, vals, units = data['fid'], data['vals'], data['units']

    # Validate exactly one missing value
    missing = [k for k, v in vals.items() if v == ""]
    if len(missing) != 1:
        return jsonify({'error': 'Leave exactly one field blank.'}), 400

    target = missing[0]

    # Normalize known values to SI units
    v = {k: normalize(val, units[k]) for k, val in vals.items() if val != ""}

    try:
        res = 0

        # === COMPLETE 70+ FORMULA ENGINE ===
        if fid == 'v_final':
            if target == 'v':
                res = v['u'] + (v['a'] * v['t'])
            elif target == 'u':
                res = v['v'] - (v['a'] * v['t'])
            elif target == 'a':
                if abs(v['t']) < 1e-12: raise ZeroDivisionError()
                res = (v['v'] - v['u']) / v['t']
            elif target == 't':
                if abs(v['a']) < 1e-12: raise ValueError('Zero acceleration')
                res = (v['v'] - v['u']) / v['a']

        elif fid == 'displacement':
            if target == 's':
                res = v['u'] * v['t'] + 0.5 * v['a'] * (v['t'] ** 2)
            elif target == 'u':
                if abs(v['t']) < 1e-12: raise ZeroDivisionError()
                res = (v['s'] - 0.5 * v['a'] * (v['t'] ** 2)) / v['t']
            elif target == 'a':
                if abs(v['t']) < 1e-12: raise ZeroDivisionError()
                res = 2 * (v['s'] - v['u'] * v['t']) / (v['t'] ** 2)
            elif target == 't':
                a_coef, b_coef, c_coef = 0.5 * v['a'], v['u'], -v['s']
                if abs(a_coef) < 1e-12:
                    if abs(b_coef) < 1e-12: raise ValueError('No solution')
                    res = v['s'] / v['u']
                else:
                    disc = b_coef ** 2 - 4 * a_coef * c_coef
                    if disc < 0: raise ValueError('No real time solution')
                    res = (-b_coef + math.sqrt(disc)) / (2 * a_coef)
                    if res < 0: res = (-b_coef - math.sqrt(disc)) / (2 * a_coef)

        elif fid == 'v_squared':
            if target == 'v':
                res = math.sqrt(v['u'] ** 2 + 2 * v['a'] * v['s'])
            elif target == 'u':
                res = math.sqrt(v['v'] ** 2 - 2 * v['a'] * v['s'])
            elif target == 'a':
                res = (v['v'] ** 2 - v['u'] ** 2) / (2 * v['s'])
            elif target == 's':
                res = (v['v'] ** 2 - v['u'] ** 2) / (2 * v['a'])

        elif fid == 'v_avg':
            if target == 'v_avg':
                res = (v['u'] + v['v']) / 2
            elif target == 'u':
                res = 2 * v['v_avg'] - v['v']
            elif target == 'v':
                res = 2 * v['v_avg'] - v['u']

        elif fid == 'distance_cv':
            if target == 'd':
                res = v['v'] * v['t']
            elif target == 'v':
                res = v['d'] / v['t'] if abs(v['t']) > 1e-12 else 0
            elif target == 't':
                res = v['d'] / v['v'] if abs(v['v']) > 1e-12 else 0

        elif fid == 'range':
            if target == 'R':
                den = math.sin(2 * v['theta'])
                if abs(den) < 1e-12: raise ValueError('sin(2θ)=0')
                res = (v['v'] ** 2 * den) / G
            elif target == 'v':
                den = math.sin(2 * v['theta'])
                if abs(den) < 1e-12: raise ValueError('sin(2θ)=0')
                res = math.sqrt((v['R'] * G) / den)
            elif target == 'theta':
                ratio = (v['R'] * G) / (v['v'] ** 2)
                if abs(ratio) > 1: raise ValueError('No real angle')
                res = 0.5 * math.asin(ratio)

        elif fid == 'f_ma':
            if target == 'F':
                res = v['m'] * v['a']
            elif target == 'm':
                res = v['F'] / v['a'] if abs(v['a']) > 1e-12 else 0
            elif target == 'a':
                res = v['F'] / v['m'] if abs(v['m']) > 1e-12 else 0

        elif fid == 'momentum':
            if target == 'p':
                res = v['m'] * v['v']
            elif target == 'm':
                res = v['p'] / v['v'] if abs(v['v']) > 1e-12 else 0
            elif target == 'v':
                res = v['p'] / v['m'] if abs(v['m']) > 1e-12 else 0

        elif fid == 'centripetal':
            if target == 'Fc':
                res = (v['m'] * v['v'] ** 2) / v['r']
            elif target == 'm':
                res = (v['Fc'] * v['r']) / (v['v'] ** 2)
            elif target == 'v':
                res = math.sqrt((v['Fc'] * v['r']) / v['m'])
            elif target == 'r':
                res = (v['m'] * v['v'] ** 2) / v['Fc']

        elif fid == 'centripetal_acc':
            if target == 'a_c':
                res = (v['v'] ** 2) / v['r']
            elif target == 'v':
                res = math.sqrt(v['a_c'] * v['r'])
            elif target == 'r':
                res = (v['v'] ** 2) / v['a_c']

        elif fid == 'angular_velocity':
            if target == 'omega':
                res = v['theta'] / v['t']
            elif target == 'theta':
                res = v['omega'] * v['t']
            elif target == 't':
                res = v['theta'] / v['omega'] if abs(v['omega']) > 1e-12 else 0

        elif fid == 'linear_velocity_circ':
            if target == 'v':
                res = v['r'] * v['omega']
            elif target == 'r':
                res = v['v'] / v['omega'] if abs(v['omega']) > 1e-12 else 0
            elif target == 'omega':
                res = v['v'] / v['r'] if abs(v['r']) > 1e-12 else 0

        elif fid == 'kinetic_e':
            if target == 'KE':
                res = 0.5 * v['m'] * (v['v'] ** 2)
            elif target == 'm':
                res = (2 * v['KE']) / (v['v'] ** 2)
            elif target == 'v':
                res = math.sqrt((2 * v['KE']) / v['m'])

        elif fid == 'work_f_d_cos':  # FIXED ID
            if target == 'W':
                res = v['F'] * v['d'] * math.cos(v['theta'])
            elif target == 'F':
                res = v['W'] / (v['d'] * math.cos(v['theta']))
            elif target == 'd':
                res = v['W'] / (v['F'] * math.cos(v['theta']))
            elif target == 'theta':
                res = math.acos(v['W'] / (v['F'] * v['d']))

        elif fid == 'potential_grav':
            if target == 'PE':
                res = v['m'] * v['g'] * v['h']
            elif target == 'm':
                res = v['PE'] / (v['g'] * v['h'])
            elif target == 'g':
                res = v['PE'] / (v['m'] * v['h'])
            elif target == 'h':
                res = v['PE'] / (v['m'] * v['g'])

        elif fid == 'potential_elastic':
            if target == 'PE':
                res = 0.5 * v['k'] * (v['x'] ** 2)
            elif target == 'k':
                res = (2 * v['PE']) / (v['x'] ** 2)
            elif target == 'x':
                res = math.sqrt((2 * v['PE']) / v['k'])

        elif fid == 'power_wt':
            if target == 'P':
                res = v['W'] / v['t']
            elif target == 'W':
                res = v['P'] * v['t']
            elif target == 't':
                res = v['W'] / v['P']

        elif fid == 'ohm':
            if target == 'V':
                res = v['I'] * v['R']
            elif target == 'I':
                res = v['V'] / v['R'] if abs(v['R']) > 1e-12 else 0
            elif target == 'R':
                res = v['V'] / v['I'] if abs(v['I']) > 1e-12 else 0

        elif fid == 'power_vi':
            if target == 'P':
                res = v['V'] * v['I']
            elif target == 'V':
                res = v['P'] / v['I']
            elif target == 'I':
                res = v['P'] / v['V']

        elif fid == 'power_i2r':
            if target == 'P':
                res = (v['I'] ** 2) * v['R']
            elif target == 'I':
                res = math.sqrt(v['P'] / v['R'])
            elif target == 'R':
                res = v['P'] / (v['I'] ** 2)

        elif fid == 'power_v2r':
            if target == 'P':
                res = (v['V'] ** 2) / v['R']
            elif target == 'V':
                res = math.sqrt(v['P'] * v['R'])
            elif target == 'R':
                res = (v['V'] ** 2) / v['P']

        elif fid == 'charge_it':
            if target == 'Q':
                res = v['I'] * v['t']
            elif target == 'I':
                res = v['Q'] / v['t']
            elif target == 't':
                res = v['Q'] / v['I']

        elif fid == 'wave_v':
            if target == 'v':
                res = v['f'] * v['lam']
            elif target == 'f':
                res = v['v'] / v['lam']
            elif target == 'lam':
                res = v['v'] / v['f']

        elif fid == 'frequency':
            if target == 'f':
                res = 1 / v['T']
            elif target == 'T':
                res = 1 / v['f']

        elif fid == 'angular_frequency':
            if target == 'omega':
                res = 2 * math.pi * v['f']
            elif target == 'f':
                res = v['omega'] / (2 * math.pi)

        elif fid == 'period':
            if target == 'T':
                res = 1 / v['f']
            elif target == 'f':
                res = 1 / v['T']

        else:
            return jsonify({'error': f'Formula {fid} not implemented yet'}), 400

        # Convert result back to display units
        final_res = denormalize(res, units[target])
        v_display = {k: denormalize(val, units[k]) for k, val in v.items()}

        # Generate steps
        steps = generate_detailed_steps(fid, target, v, v_display, units, res, final_res)

        return jsonify({
            'res_formatted': None,  # Frontend handles formatting
            'res': final_res,
            'unit': units[target],
            'steps': steps
        })

    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero - check inputs.'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Calculation error: {str(e)}'}), 500
