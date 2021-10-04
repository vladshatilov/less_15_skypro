import sqlite3 #нужно ли в модуле? без него ругается питон

#Приведение к именованному формату вывода
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#Возвращает результат запроса к базе по номеру котика
def search_db(num):
    query = f'''select 
                "index",age_upon_outcome,animal_type,coalesce(name,'no_name_:(') as name,
                breed, coalesce(ci1.color,'') as color1, coalesce(ci2.color,'') as color2,
                date_of_birth,outcome_subtype,outcome_type,outcome_month,outcome_year
            from animals_index_table aa
            left join breed_index_table bi on aa.breed_index = bi.breed_index
            left join colors_index_table ci1 on aa.color_index1 = ci1.color_index
            left join colors_index_table ci2 on aa.color_index2 = ci2.color_index
            where "index" = {num}'''
    conn = sqlite3.connect('animal.db')
    conn.row_factory = dict_factory
    curs = conn.cursor()
    curs.execute(query)
    one_result = curs.fetchall()
    curs.close()
    return one_result

#get length of the array
def get_len_db():
    query = f'''select 
                max("index") as len_num
            from animals_index_table aa'''
    conn = sqlite3.connect('animal.db')
    conn.row_factory = dict_factory
    curs = conn.cursor()
    curs.execute(query)
    one_result = curs.fetchall()
    curs.close()
    return one_result

#создаем базу с индексами по основной таблице.
# привёл в качестве примера замену на индексы для породы и цвета,
# для остальных полей методика схожая, поэтому не стал дублировать много кода
query_create_animals_index_table = '''drop table if exists animals_index_table;
    CREATE TABLE animals_index_table (
        "index" INT,
        age_upon_outcome VARCHAR(80),
        animal_id VARCHAR(40),
        animal_type VARCHAR(20),
        name VARCHAR(40),
            breed_index INT,
            color_index1 INT,
            color_index2 INT,
        date_of_birth VARCHAR(20),
        outcome_subtype VARCHAR(20),
        outcome_type VARCHAR(20),
        outcome_month INT,
        outcome_year INT
            );		
    INSERT INTO animals_index_table(
            "index",age_upon_outcome,animal_id,animal_type,name,
            breed_index, color_index1,color_index2,
            date_of_birth,outcome_subtype,outcome_type,outcome_month,outcome_year)
    select 
        "index",age_upon_outcome,animal_id,animal_type,name,
    --		breed,
            breed_index,
    --		color1,color2,
            ci1.color_index as color_index1,ci2.color_index as color_index2,
            date_of_birth,outcome_subtype,outcome_type,outcome_month,outcome_year
    from animals aa
    left join breed_index_table bi on aa.breed = bi.breed
    left join colors_index_table ci1 on aa.color1 = ci1.color
    left join colors_index_table ci2 on aa.color2 = ci2.color;'''


#создаем базу с индексами для породы
query_create_breed_index_table = '''drop table if exists breed_index_table;
    CREATE TABLE breed_index_table (
        breed VARCHAR(40),
            breed_index INT
            );		
    INSERT INTO breed_index_table(
            breed,
            breed_index)
    WITH st1 as (
            select distinct breed 
            from animals a 
        )
         select 
          'Null' as breed, cast(1 as integer) as breed_index
        from st1
        UNION
        select 
          breed, cast((1+row_number() over( order by breed)) as integer) as breed_index
        from st1
        where breed!=0 and breed!='0' and breed!='' and not breed is null
        order by 2
       ;'''


#создаем базу с индексами для цвета
query_create_colors_index_table = '''drop table if exists colors_index_table;
    CREATE TABLE colors_index_table (
        color VARCHAR(40),
            color_index INT
            );		
    INSERT INTO colors_index_table(
            color,
            color_index)
    WITH colors as (
        select
            distinct trim(color1) as color
        from animals a 
        Union
        select
            distinct trim(color2)  as color
        from animals a 
    )
     select 
      'Null' as color, cast(1 as integer) as color_index
      from colors
    UNION
    select 
      color, cast((1+row_number() over( order by color)) as integer) as color_index
    from colors
    where color!=0 and color!='0' and color!='' and not color is null
       ;'''
