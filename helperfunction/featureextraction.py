def __datetime(date_str):
    return datetime.strptime(date_str, "%d/%m/%Y %H:%M")

def cal_late_time(df):
    for index, row in df.iterrows():
        planned_dprt_time = __datetime(str(row['planned_station_dprt_time']))
        actual_dprt_time = __datetime(str(row['actual_station_dprt_time']))
        planned_arrv_time = __datetime(str(row['planned_station_arrv_time']))
        actual_arrv_time = __datetime(str(row['actual_station_arrv_time']))
        delta_arrv = actual_arrv_time - planned_arrv_time
        delta_dprt = actual_dprt_time - planned_dprt_time
        df.loc[index,'arrv_late_time'] = delta_arrv.total_seconds()
        df.loc[index,'dprt_late_time'] = delta_dprt.total_seconds()

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

def change_date_format(df):
    for idx, row in df.iterrows():
        row_date = datetime.strptime(row['service_date'], '%d/%m/%Y')
        row_date_str = datetime.strftime(row_date, '%d/%m/%Y')
        test.loc[idx, 'service_date'] = row_date_str