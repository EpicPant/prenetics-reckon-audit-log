date_row = 1
date_col = 1

for i in range(30):
    if date_col == 7:
        date_col = 1
        date_row += 1
    else:
        date_col += 1

    print(f'Row: {date_row}, Col: {date_col}')
