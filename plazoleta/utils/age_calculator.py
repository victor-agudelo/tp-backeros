from datetime import date, datetime



def validate_age(age):
    if isinstance(age, str):
        age = datetime.strptime(age, '%Y-%m-%d')
    calculo = date.today() - age
    return calculo.days // 365.25
