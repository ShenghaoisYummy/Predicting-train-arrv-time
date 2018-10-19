from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def change_date_format(df):
    for idx, row in df.iterrows():
        row_date = datetime.strptime(row['service_date'], '%d/%m/%Y')
        row_date_str = datetime.strftime(row_date, '%d/%m/%Y')
        df.loc[idx, 'service_date'] = row_date_str

def __datetime(date_str):
    return datetime.strptime(date_str, "%d/%m/%Y %H:%M")

def cal_late_time(df):
    for idx, row in df.iterrows():
        planned_dprt_time = __datetime(str(row['planned_station_dprt_time']))
        actual_dprt_time = __datetime(str(row['actual_station_dprt_time']))
        planned_arrv_time = __datetime(str(row['planned_station_arrv_time']))
        actual_arrv_time = __datetime(str(row['actual_station_arrv_time']))
        delta_arrv = actual_arrv_time - planned_arrv_time
        delta_dprt = actual_dprt_time - planned_dprt_time
        df.loc[idx,'arrv_late_time'] = delta_arrv.total_seconds()
        df.loc[idx,'dprt_late_time'] = delta_dprt.total_seconds()
        print("Currently on row: {}; Currently iterrated {}% of rows".format(idx, (idx + 1)/len(df.index) * 100))


def cal_last_node_late(df):
    for idx, row in df.iloc[1:].iterrows():
        last_node_row = df.loc[(df['service_date'] == row['service_date']) & (df['trip_name'] == row['trip_name']) & (df['node_seq_order'] == row['node_seq_order'] - 1)]
        if last_node_row.empty:
            df.loc[idx, 'last_node_arrv_late_time'] = 0
            df.loc[idx, 'last_node_dprt_late_time'] = 0
        else:
            last_node_arrv_late_time = last_node_row.arrv_late_time.values
            last_node_dprt_late_time = last_node_row.dprt_late_time.values
            df.loc[idx, 'last_node_arrv_late_time'] = last_node_arrv_late_time
            df.loc[idx, 'last_node_dprt_late_time'] = last_node_dprt_late_time
        print("Currently on row: {}; Currently iterrated {}% of rows".format(idx, (idx + 1)/len(df.index) * 100))

def cal_last_n_node_late(df, n):
    for idx, row in df.iterrows():
        arrv_late_time_array = []
        dprt_late_time_array = []
        if row['node_seq_order'] > n:
            for i in range(1, n + 1):
                last_n_node_row = df.loc[(df['service_date'] == row['service_date']) & (df['trip_name'] == row['trip_name']) & (df['node_seq_order'] == row['node_seq_order'] - i)]
                if last_n_node_row.empty:
                    arrv_late_time_array.append(0)
                    dprt_late_time_array.append(0)
                else:
                    arrv_late_time_array.append(last_n_node_row.arrv_late_time.values)
                    dprt_late_time_array.append(last_n_node_row.dprt_late_time.values)
            df.loc[idx, 'last_{}_node_arrv_late_time_sum'.format(n)] = np.sum(arrv_late_time_array)
            df.loc[idx, 'last_{}_node_dprt_late_time_sum'.format(n)] = np.sum(dprt_late_time_array)
            df.loc[idx, 'last_{}_node_arrv_late_time_mean'.format(n)] = np.mean(arrv_late_time_array)
            df.loc[idx, 'last_{}_node_dprt_late_time_mean'.format(n)] = np.mean(dprt_late_time_array)
            df.loc[idx, 'last_{}_node_arrv_late_time_median'.format(n)] = np.median(arrv_late_time_array)
            df.loc[idx, 'last_{}_node_dprt_late_time_median'.format(n)] = np.median(dprt_late_time_array)
            df.loc[idx, 'last_{}_node_arrv_late_time_std'.format(n)] = np.std(arrv_late_time_array)
            df.loc[idx, 'last_{}_node_dprt_late_time_std'.format(n)] = np.std(dprt_late_time_array)
            df.loc[idx, 'last_{}_node_arrv_late_time_max'.format(n)] = np.max(arrv_late_time_array)
            df.loc[idx, 'last_{}_node_dprt_late_time_max'.format(n)] = np.max(dprt_late_time_array)
            df.loc[idx, 'last_{}_node_arrv_late_time_min'.format(n)] = np.min(arrv_late_time_array)
            df.loc[idx, 'last_{}_node_dprt_late_time_min'.format(n)] = np.min(dprt_late_time_array)
        else:
            df.loc[idx, 'last_{}_node_arrv_late_time_sum'.format(n)] = 0
            df.loc[idx, 'last_{}_node_dprt_late_time_sum'.format(n)] = 0
            df.loc[idx, 'last_{}_node_arrv_late_time_mean'.format(n)] = 0
            df.loc[idx, 'last_{}_node_dprt_late_time_mean'.format(n)] = 0
            df.loc[idx, 'last_{}_node_arrv_late_time_median'.format(n)] = 0
            df.loc[idx, 'last_{}_node_dprt_late_time_median'.format(n)] = 0
            df.loc[idx, 'last_{}_node_arrv_late_time_std'.format(n)] = 0
            df.loc[idx, 'last_{}_node_dprt_late_time_std'.format(n)] = 0
            df.loc[idx, 'last_{}_node_arrv_late_time_max'.format(n)] = 0
            df.loc[idx, 'last_{}_node_dprt_late_time_max'.format(n)] = 0
            df.loc[idx, 'last_{}_node_arrv_late_time_min'.format(n)] = 0
            df.loc[idx, 'last_{}_node_dprt_late_time_min'.format(n)] = 0
        print("Currently on row: {}; Currently iterrated {}% of rows".format(idx, (idx + 1)/len(df.index) * 100))
        
def rowelement(colname, df):
    list = []
    for index, row in df.iterrows():
        if row[colname] not in list:
            list.append(row[colname])
    return list

def col_group(df, group_col_str):
    df_describe_arrv = df.groupby(group_col_str).arrv_late_time.mean().describe().values
    df_describe_dprt = df.groupby(group_col_str).dprt_late_time.mean().describe().values
    for idx, row in df.iterrows():
        if row['arrv_late_time'] < df_describe_arrv[4]:
            df.loc[idx,'{}_arrv_group'.format(group_col_str)] = 'less_than_.25'
        if df_describe_arrv[4] < row['arrv_late_time'] < df_describe_arrv[5]:
            df.loc[idx,'{}_arrv_group'.format(group_col_str)] = '.25_to_.50'
        if df_describe_arrv[5] < row['arrv_late_time'] < df_describe_arrv[6]:
            df.loc[idx,'{}_arrv_group'.format(group_col_str)] = '.50_to_.75'
        if df_describe_arrv[6] < row['arrv_late_time']:
            df.loc[idx,'{}_arrv_group'.format(group_col_str)] = 'great_than_.75'
            
        if row['dprt_late_time'] < df_describe_dprt[4]:
            df.loc[idx,'{}_dprt_group'.format(group_col_str)] = 'less_than_.25'
        if df_describe_dprt[4] < row['dprt_late_time'] < df_describe_dprt[5]:
            df.loc[idx,'{}_dprt_group'.format(group_col_str)] = '.25_to_.50'
        if df_describe_dprt[5] < row['dprt_late_time'] < df_describe_dprt[6]:
            df.loc[idx,'{}_dprt_group'.format(group_col_str)] = '.50_to_.75'
        if df_describe_dprt[6] < row['dprt_late_time']:
            df.loc[idx,'{}_dprt_group'.format(group_col_str)] = 'great_than_.75'
        print("Currently on row: {}; Currently iterrated {}% of rows".format(idx, (idx + 1)/len(df.index) * 100))

def cal_last_n_days_late(df, n):
    df_start_date_str = df.loc[1]['service_date']
    df_start_date = datetime.strptime(df_start_date_str, '%d/%m/%Y')
    loop_start_date_str = datetime.strftime(df_start_date + timedelta(n), '%d/%m/%Y')
    for idx, row in df.iterrows():
        arrv_late_time_array = []
        dprt_late_time_array = []
        row_service_date = datetime.strptime(row['service_date'], '%d/%m/%Y')
        loop_start_date = datetime.strptime(loop_start_date_str, '%d/%m/%Y')
        if row_service_date >= loop_start_date:
            for i in range(1, n + 1):
                pre_n_service_date_str = datetime.strftime(row_service_date - timedelta(i), '%d/%m/%Y')
                last_n_days_rows = df.loc[(df['service_date'] == pre_n_service_date_str) & (df['actual_stop_node'] == row['actual_stop_node'])]
                for index, last_n_days_row in last_n_days_rows.iterrows():
                    if last_n_days_row.empty:
                        arrv_late_time_array.append(0)
                        dprt_late_time_array.append(0)
                    else:
                        arrv_late_time_array.append(last_n_days_row['arrv_late_time'])
                        dprt_late_time_array.append(last_n_days_row['dprt_late_time'])
            if(all(v == 0 for v in  dprt_late_time_array) == False):
                df.loc[idx, 'last_{}_days_arrv_late_time_sum'.format(n)] = np.sum(arrv_late_time_array)
                df.loc[idx, 'last_{}_days_dprt_late_time_sum'.format(n)] = np.sum(dprt_late_time_array)
                df.loc[idx, 'last_{}_days_arrv_late_time_mean'.format(n)] = np.mean(arrv_late_time_array)
                df.loc[idx, 'last_{}_days_dprt_late_time_mean'.format(n)] = np.mean(dprt_late_time_array)
                df.loc[idx, 'last_{}_days_arrv_late_time_median'.format(n)] = np.median(arrv_late_time_array)
                df.loc[idx, 'last_{}_days_dprt_late_time_median'.format(n)] = np.median(dprt_late_time_array)
                df.loc[idx, 'last_{}_days_arrv_late_time_std'.format(n)] = np.std(arrv_late_time_array)
                df.loc[idx, 'last_{}_days_dprt_late_time_std'.format(n)] = np.std(dprt_late_time_array)
                df.loc[idx, 'last_{}_days_arrv_late_time_max'.format(n)] = np.max(arrv_late_time_array)
                df.loc[idx, 'last_{}_days_dprt_late_time_max'.format(n)] = np.max(dprt_late_time_array)
                df.loc[idx, 'last_{}_days_arrv_late_time_min'.format(n)] = np.min(arrv_late_time_array)
                df.loc[idx, 'last_{}_days_dprt_late_time_min'.format(n)] = np.min(dprt_late_time_array)
            else:
                df.loc[idx, 'last_{}_days_arrv_late_time_sum'.format(n)] = 0
                df.loc[idx, 'last_{}_days_dprt_late_time_sum'.format(n)] = 0
                df.loc[idx, 'last_{}_days_arrv_late_time_mean'.format(n)] = 0
                df.loc[idx, 'last_{}_days_dprt_late_time_mean'.format(n)] = 0
                df.loc[idx, 'last_{}_days_arrv_late_time_median'.format(n)] = 0
                df.loc[idx, 'last_{}_days_dprt_late_time_median'.format(n)] = 0
                df.loc[idx, 'last_{}_days_arrv_late_time_std'.format(n)] = 0
                df.loc[idx, 'last_{}_days_dprt_late_time_std'.format(n)] = 0
                df.loc[idx, 'last_{}_days_arrv_late_time_max'.format(n)] = 0
                df.loc[idx, 'last_{}_days_dprt_late_time_max'.format(n)] = 0
                df.loc[idx, 'last_{}_days_arrv_late_time_min'.format(n)] = 0
                df.loc[idx, 'last_{}_days_dprt_late_time_min'.format(n)] = 0
        else:
            df.loc[idx, 'last_{}_days_arrv_late_time_sum'.format(n)] = 0
            df.loc[idx, 'last_{}_days_dprt_late_time_sum'.format(n)] = 0
            df.loc[idx, 'last_{}_days_arrv_late_time_mean'.format(n)] = 0
            df.loc[idx, 'last_{}_days_dprt_late_time_mean'.format(n)] = 0
            df.loc[idx, 'last_{}_days_arrv_late_time_median'.format(n)] = 0
            df.loc[idx, 'last_{}_days_dprt_late_time_median'.format(n)] = 0
            df.loc[idx, 'last_{}_days_arrv_late_time_std'.format(n)] = 0
            df.loc[idx, 'last_{}_days_dprt_late_time_std'.format(n)] = 0
            df.loc[idx, 'last_{}_days_arrv_late_time_max'.format(n)] = 0
            df.loc[idx, 'last_{}_days_dprt_late_time_max'.format(n)] = 0
            df.loc[idx, 'last_{}_days_arrv_late_time_min'.format(n)] = 0
            df.loc[idx, 'last_{}_days_dprt_late_time_min'.format(n)] = 0
        print("Currently on row: {}; Currently iterrated {}% of rows".format(idx, (idx + 1)/len(df.index) * 100))

def is_same_stop_station(df):
    df['is_same_stop_node'] = np.where(df['planned_stop_node'] == df['actual_stop_node'] , 1, 0)
    df['is_same_stop_station'] = np.where(df['planned_stop_station'] == df['actual_stop_station'] , 1, 0)

def date_to_week(df):
    datetime = pd.to_datetime(df['service_date'], format='%d/%m/%Y')
    df['day_of_week'] = datetime.dt.dayofweek
    df['is_weekend'] = np.where((test['day_of_week'] == 5) | (test['day_of_week'] == 6) , 1, 0)


def split_date(df, col_str):
    datetime = pd.to_datetime(df[col_str], format="%d/%m/%Y %H:%M")
    df['{}_month'.format(col_str)] = datetime.dt.strftime('%-m').apply(int)
    df['{}_days'.format(col_str)] = datetime.dt.strftime('%-d').apply(int)
    df['{}_hours'.format(col_str)] = datetime.dt.strftime('%-H').apply(int)
    df['{}_minutes'.format(col_str)] = datetime.dt.strftime('%-M').apply(int)

def is_peak_time(df):
    df['is_peak_time'] = np.where(((6 <= df['actual_station_arrv_time_hours']) & (df['actual_station_arrv_time_hours'] <= 8)) | ((16 <= df['actual_station_arrv_time_hours'])& ( df['actual_station_arrv_time_hours']<= 19)), 1, 0)