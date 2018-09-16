import pandas as pd

def find_financial_quarter(date):
    if(date.month >= 1 and date.month <= 3):
        return 'FQ3'
    if(date.month >= 4 and date.month <= 6):
        return 'FQ4'
    if(date.month >= 7 and date.month <= 9):
        return 'FQ1'
    if(date.month >= 10 and date.month <= 12):
        return 'FQ2'
   
def find_season(date):
    if(date.month == 12 or date.month <= 2):
        return 'Summer'
    if(date.month >= 3 or date.month <= 5):
        return 'Autumn'
    if(date.month >= 6 or date.month <= 8):
        return 'Winter'
    if(date.month >= 9 or date.month <= 11):
        return 'Spring'

def find_holiday(date):
    if(date.month == 12 and date.day == 25): # Christmas
        return 'holiday'
    if(date.month == 12 and date.day == 26): # Boxing
        return 'holiday'
    if(date.month == 1 and date.day == 1): # New Year
        return 'holiday'
    if(date.month == 1 and date.day == 28): # Australia Day
        return 'holiday'
    if(date.month == 3 and date.day == 11): # Canberra Day
        return 'holiday'
    if(date.month == 4 and date.day == 25): # Anzac
        return 'holiday'
    if(date.month == 5 and date.day == 28): # Reconciliation Day
        return 'holiday'
    if(date.month == 6 and date.day == 11): # Queen's Birthday
        return 'holiday'
    else:
        return 'workday'

def  is_weekend(date):
    if(date.isoweekend() == 6 or date.isoweekend() == 7):
        return 1
    else:
        return 0
        
def is_on_time(planed_time, actual_time):
    if planed_time < actual_time:
        return 0
    else:
        return 1
