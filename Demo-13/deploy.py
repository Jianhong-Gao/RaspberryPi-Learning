import os
from utils_deploy.compile_and_deploy import compile_build_clear,compile_folders,delete_source_py

print("当前工作目录:", os.getcwd())  # 打印当前工作目录


if __name__ == "__main__":
    python_file = "py_package"
    output_dir = "so_package"

    source_paths = ["py_package"]  # or specific python files
    compile_folders(source_paths,output_dir_suffix='_so')
    delete_source_py(source_paths)
    compile_build_clear()