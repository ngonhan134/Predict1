import os

# Đường dẫn đến thư mục gốc chứa tất cả các thư mục con và ảnh
root_dir = "./DATA_RGB"

# Tên thư mục đích để chuyển tất cả các ảnh được đổi tên
dest_dir = "Unknow"

# Lặp qua tất cả các thư mục con của thư mục gốc
for subdir in os.listdir(root_dir):
    subdir_path = os.path.join(root_dir, subdir)
    if os.path.isdir(subdir_path):
        # Lặp qua tất cả các file ảnh trong thư mục con và đổi tên
        i = 1
        for file in os.listdir(subdir_path):
            file_path = os.path.join(subdir_path, file)
            if os.path.isfile(file_path) and file.lower().endswith((".jpg", ".jpeg", ".bmp")):
                new_file_name = "{}_{}.{}".format(subdir, i, file.split(".")[-1])
                new_file_path = os.path.join(root_dir, dest_dir, new_file_name)
                os.rename(file_path, new_file_path)
                i += 1
import os

# # Đường dẫn đến thư mục gốc chứa các thư mục con
# root_dir = "DATA_RGB"

# # Đổi tên và chuyển ảnh vào thư mục "Unknow"
# for subdir, dirs, files in os.walk(root_dir):
#     for folder in dirs:
#         folder_path = os.path.join(subdir, folder)
#         new_folder_name = folder.lower()  # đổi tên folder con
#         new_folder_path = os.path.join(subdir, "Unknow", new_folder_name)
#         os.makedirs(new_folder_path, exist_ok=True)

#         # đổi tên và chuyển ảnh vào folder "Unknow"
#         count = 0
#         for file in os.listdir(folder_path):
#             if file.endswith(".bmp"):
#                 count += 1
#                 new_file_name = f"{new_folder_name}_{count}.bmp"
#                 old_file_path = os.path.join(folder_path, file)
#                 new_file_path = os.path.join(new_folder_path, new_file_name)
#                 os.rename(old_file_path, new_file_path)
