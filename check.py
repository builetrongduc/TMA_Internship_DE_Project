import pandas as pd
from faker import Faker

fake = Faker()

# short_description = fake.text()
# print(short_description)

df=pd.read_csv('./lazada/productData/finalLazada2.csv')

# Insert Fake text in each description
# for i in range(len(df['description'])):
#     df['description'][i] = fake.text()

# print(df['description'].head())


# Duplicate each product has 3 sizes S, M, L and add suffix ID with IDL, IDM, IDS
# Tạo size variants S, M, L
# Danh sách các size cần thêm
# size_variants = ["S", "M", "L"]

# Tạo bản sao của dữ liệu gốc với size
# expanded_rows = []
# for _, row in df.iterrows():
#     for size in size_variants:
#         new_row = row.copy()
#         new_row["ID"] = f"{row['ID']}{size}"  # Thêm hậu tố _S, _M, _L vào ID
#         new_row["size"] = size  # Thêm cột size
#         expanded_rows.append(new_row)

# Tạo DataFrame mới với các bản ghi đã nhân bản
# df_expanded = pd.DataFrame(expanded_rows)
# print(df_expanded.info())


# Delete row duplicate ID 


print(df['ID'].duplicated().sum())  # Kiểm tra số lượng ID trùng lặp
print(df[df['ID'].duplicated(keep=False)])


print('Done')
