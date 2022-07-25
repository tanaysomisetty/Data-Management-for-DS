import csv

pokemon_rows = []
type_occurs = {}
above_thresh = {}
eqbelow_thresh = {}

# -------- set up --------
def read_csv(file):
    reader = csv.DictReader(open(file))

    with open(file) as csvfile:
        global pokemon_fieldnames
        pokemon_fieldnames = reader.fieldnames
        for row in reader:
            pokemon_rows.append(row)

# -------- # 1.1 --------
def find_percentage(file, type='fire', level=40):
    fire_cnt = 0
    above40_cnt = 0
    for row in pokemon_rows:
        if row['type'] == type:
            fire_cnt = fire_cnt + 1
            if (float(row['level']) >= 40):
                above40_cnt = above40_cnt + 1

    percentage = (above40_cnt / fire_cnt) * 100
    percentage = round(percentage)
    with open(file,'w') as txtfile:
        txtfile.write(f'Percentage of {type} type Pokemons at or above level {level} = {percentage}')

# -------- # 1.2 --------
def create_type_dict():
    for row in pokemon_rows:
        weakness = row['weakness']
        type = row['type']
        weak_dict = {}
        if weakness in type_occurs:
            weak_dict = type_occurs[weakness]
        if type != 'NaN':
                if type in weak_dict:
                    type_cnt = weak_dict[type]
                    weak_dict[type] = type_cnt + 1
                else:
                    weak_dict[type] = 1
                type_occurs[weakness] = weak_dict

def fill_type():
    for row in pokemon_rows:
        weakness = row['weakness']
        type = row['type']
        if type == 'NaN':
            sorted_types = sorted(type_occurs[weakness].items(), key=lambda x:x[1], reverse=True)
            row['type'] = sorted_types[0][0]

# -------- # 1.3 --------
def find_avg_values(threshold):
    #attack
    hi_atk_sum = 0
    hi_atk_cnt = 0
    lo_atk_sum = 0
    lo_atk_cnt = 0

    for row in pokemon_rows:
        lvl = row['level']
        atk = row['atk']
        if atk != 'NaN':
            if float(lvl) > threshold:
                hi_atk_sum += float(atk)
                hi_atk_cnt += 1
            else:
                lo_atk_sum += float(atk)
                lo_atk_cnt += 1

    # defense
    hi_def_sum = 0
    hi_def_cnt = 0
    lo_def_sum = 0
    lo_def_cnt = 0

    for row in pokemon_rows:
        lvl = row['level']
        den = row['def']
        if den != 'NaN':
            if float(lvl) > threshold:
                hi_def_sum += float(den)
                hi_def_cnt += 1
            else:
                lo_def_sum += float(den)
                lo_def_cnt += 1

    # hit points
    hi_hp_sum = 0
    hi_hp_cnt = 0
    lo_hp_sum = 0
    lo_hp_cnt = 0

    for row in pokemon_rows:
        lvl = row['level']
        hp = row['hp']
        if hp != 'NaN':
            if float(lvl) > threshold:
                hi_hp_sum += float(hp)
                hi_hp_cnt += 1
            else:
                lo_hp_sum += float(hp)
                lo_hp_cnt += 1

    if(hi_atk_cnt > 0):
        above_thresh['atk'] = round((hi_atk_sum/hi_atk_cnt),1)
    if(hi_def_cnt > 0):
        above_thresh['def'] = round((hi_def_sum / hi_def_cnt),1)
    if (hi_hp_cnt > 0):
        above_thresh['hp'] = round((hi_hp_sum / hi_hp_cnt),1)

    if (lo_atk_cnt > 0):
        eqbelow_thresh['atk'] = round((lo_atk_sum / lo_atk_cnt),1)
    if (lo_def_cnt > 0):
        eqbelow_thresh['def'] = round((lo_def_sum / lo_def_cnt),1)
    if (lo_hp_cnt > 0):
        eqbelow_thresh['hp'] = round((lo_hp_sum / lo_hp_cnt),1)


def fill_value(threshold=40):
    find_avg_values(threshold)

    for row in pokemon_rows:
        atk = row['atk']
        den = row['def']
        hp = row['hp']
        lvl = row['level']

        if atk == 'NaN':
            if (float(lvl) > threshold):
                row['atk'] = str(above_thresh['atk'])
            else:
                row['atk'] = str(eqbelow_thresh['atk'])

        if den == 'NaN':
            if (float(lvl) > threshold):
                row['def'] = str(above_thresh['def'])
            else:
                row['def'] = str(eqbelow_thresh['def'])

        if hp == 'NaN':
            if (float(lvl) > threshold):
                row['hp'] = str(above_thresh['hp'])
            else:
                row['hp'] = str(eqbelow_thresh['hp'])

def output_result(file):
    with open(file,'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=pokemon_fieldnames, delimiter=',')
        writer.writeheader()

        for row in pokemon_rows:
            writer.writerow(row)

# -------- # 1.4 --------
def map_types(in_file,out_file):
    types = {}
    reader = csv.DictReader(open(in_file))

    with open(in_file) as csvfile:
        for row in reader:
            type = row['type']
            personality = row['personality']
            type_lst = []
            if type in types:
                type_lst = types[type]
            if personality not in type_lst:
                type_lst.append(personality)
            types[type] = type_lst

    for key,list in types.items():
        list = sorted(list)
        types[key] = list

    sorted_types = sorted(types.items(), key=lambda x: x[0])

    with open(out_file,'w') as txtfile:
        txtfile.write('Pokemon type to personality mapping:\n\n')
        for item in sorted_types:
            joint_str = ', '.join(item[1])
            txtfile.write(f'\t {item[0]}: {joint_str}\n')

# -------- # 1.5 --------
def find_avg_hp(in_file, out_file, stage='3.0'):
    reader = csv.DictReader(open(in_file))

    hp_sum = 0
    hp_cnt = 0

    with open(in_file) as csvfile:
        for row in reader:
            curr_stage = row['stage']
            if curr_stage == stage:
                hp_sum += float(row['hp'])
                hp_cnt += 1

    avg_hp = round(hp_sum / hp_cnt)

    with open(out_file,'w') as txtfile:
        txtfile.write(f'Average hit point for Pokemons of stage {stage} = {avg_hp}')


# -------- main function --------
def main():
    read_csv('pokemonTrain.csv')
    find_percentage('pokemon1.txt')
    create_type_dict()
    fill_type()
    fill_value()
    output_result('pokemonResult.csv')
    map_types('pokemonResult.csv','pokemon4.txt')
    find_avg_hp('pokemonResult.csv','pokemon5.txt')

main()