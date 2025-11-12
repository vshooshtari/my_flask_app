from flask import Flask, render_template, request
import csv

def read_csv_file():
    fields = []
    with open('fields.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Strip whitespace from keys/values
            cleaned = {k.strip(): v.strip() for k, v in row.items()}
            # Ensure the new keys exist
            cleaned.setdefault('field_type', 'text')
            cleaned.setdefault('options', '')
            cleaned.setdefault('validation', '')
            fields.append(cleaned)
    return fields

def validate_form(data, fields):
    errors = {}
    for f in fields:
        key = f['field_name'].replace(' ', '_')
        value = data.get(key, '').strip()
        rules = f.get('validation', '')

        if 'required' in rules and not value:
            errors[key] = 'این فیلد الزامی است.'

        if f['field_type'] == 'number' and value:
            try:
                num = float(value)
                if 'min:' in rules:
                    min_val = float(rules.split('min:')[1].split('|')[0])
                    if num < min_val:
                        errors[key] = f'عدد باید بزرگتر یا مساوی {min_val} باشد.'
                if 'max:' in rules:
                    max_val = float(rules.split('max:')[1].split('|')[0])
                    if num > max_val:
                        errors[key] = f'عدد باید کوچکتر یا مساوی {max_val} باشد.'
            except ValueError:
                errors[key] = 'عدد معتبر نیست.'

        # add more rule handling as needed
    return errors


app = Flask(__name__)


@app.route('/')
def index():
    fields = read_csv_file()
    print(fields)
    return render_template('form.html', fields=fields)

@app.route('/submit', methods=['POST'])
def submit():
    fields = read_csv_file()          # same definition used for rendering
    form_data = request.form.to_dict()
    errors = validate_form(form_data, fields)

    if errors:
        # re‑render the form with error messages
        return render_template('form.html', fields=fields, errors=errors, old=form_data)

    # … existing processing logic …

    context = {key: value for key, value in request.form.items()}
    print("Form Keys:", context.keys())  # debug line to view keys    
    print("Form Submitted Data:", context)
    value_j2_text = context.get('value_j2')
# processing of the input data-------------------------------------Logic----
    #def al_frame_calculate():
    lenght_al_frame_ver=int(context.get('H_vrodi')) \
    - int(context.get('bdkh_ver'))
    lenght_al_frame_hor=int(context.get('w_vrodi')) \
    - int(context.get('bdkh_hor'))*2
    door_thickness= context.get('dtkh')
    prd_desc = context.get('prd_desc') + ' ضخامت تمام شده درب  ' + door_thickness
    roye_thk = int(context.get('roye_thk'))
    size_choob = int(door_thickness) - roye_thk*2
    txt_choob_kalaf_darb = ' کلاف درب جنس: چوب' + str(size_choob)
    txt_mat_klaf_darb = ' چوب ' + str(size_choob)
    door_acc_w = int(context.get('w_vrodi'))-2*60
    door_acc_h = int(context.get('H_vrodi'))-67 
    txt_mat_roye_darb = ' رویه ' + context.get('mat_roye') + ' به ضخامت ' + str(roye_thk)
    klaf_door_baho_len_with_margin = door_acc_h + 10
    klaf_door_pasar_len_with_margin = door_acc_w + 10
    roye_w_with_margin = door_acc_w + 10
    roye_h_with_margin = door_acc_h + 10
    prname = 'درب فریم لس تیپ A '
    choob_in_al_ver = lenght_al_frame_ver - 34 - 9
    choob_in_al_hor = lenght_al_frame_hor - 10 * 2

    processed_data = {
        'value_a2': context.get('value_a2', ''),
        'value_j2': value_j2_text ,
        'value_b6': prd_desc,
        'value_h6': door_acc_w,
        'value_i6': door_acc_h,
        'value_j6': context.get('value_j6'),
        'value_a8': 'فریم آلومینیوم  از جنس پروفیل آلومینیوم - 50',
        'value_prname': prname,
        'value_c10': 'فریم آلومینیوم قطعه عمودی',
        'value_d10': 'پروفیل آلومینیوم - 50',
        'value_e10': '2',
        'value_f10': 'مطابق نمونه',
        'value_i10': lenght_al_frame_ver ,#context.get('H_vrodi'), 
        'value_c11': 'فریم آلومینیوم قطعه افقی',
        'value_d11': 'پروفیل آلومینیوم - 50',
        'value_e11': '1',
        'value_f11': 'مطابق نمونه',
        'value_i11': lenght_al_frame_hor,
        'value_a13': txt_mat_roye_darb,
        'value_b15': 'رویه درب',
        'value_c15': '2',
        'value_d15': roye_w_with_margin,
        'value_e15': roye_h_with_margin,
        'value_f15': context.get('ارتفاع دقیق نهایی درب', ''),
        'value_g15': context.get('ارتفاع دقیق نهایی درب', ''),
        'value_h15': context.get('ارتفاع دقیق نهایی درب', ''),
        'value_i15': context.get('ارتفاع دقیق نهایی درب', ''),
        'value_j15': context.get('ارتفاع دقیق نهایی درب', ''),
        'value_a17': txt_choob_kalaf_darb,
        'value_b19': prname,
        'value_d19': txt_mat_klaf_darb,
        'value_e19': '2',
        'value_f19': '55',
        'value_h19': klaf_door_baho_len_with_margin,
        'value_d20': txt_mat_klaf_darb,
        'value_e20': '1',
        'value_f20': '55',
        'value_g20': klaf_door_pasar_len_with_margin,
        'value_e25': choob_in_al_ver,
        'value_e26': choob_in_al_hor,
        'value_c30': context.get('door_ori', ''),
        'value_g30': context.get('ارتفاع دقیق نهایی درب', ''),
        'value_h30': context.get('ارتفاع دقیق نهایی درب', ''),
        'value_c31': context.get('door_color', ''),
        'value_d31': context.get('ارتفاع دقیق نهایی درب', ''),
        'value_e31': context.get('ارتفاع دقیق نهایی درب', ''),
        'value_f31': context.get('ارتفاع دقیق نهایی درب', ''),
    }
    
    return render_template('output.html', **processed_data)

if __name__ == '__main__':
    # global fields2
    app.run(debug=True)
