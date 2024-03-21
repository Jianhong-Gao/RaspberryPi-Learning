from setuptools import setup, Extension
from Cython.Build import cythonize
import glob
import shutil
import os
import platform

def compile_build_clear():
    if os.path.exists('build'):
        shutil.rmtree('build')


def get_extension_suffix():
    if platform.system().lower() == 'windows':
        return '.pyd'
    else:
        return '.so'

def compile_and_move_extensions(input_path, output_dir):
    """
    编译Python文件或文件夹中的所有Python文件为C扩展，并将生成的文件移动到指定的输出目录。

    参数:
    input_path (str | list): 要编译的Python文件路径、路径列表或文件夹路径。
    output_dir (str): 生成文件的目标输出目录。
    """
    python_files = []
    extension = get_extension_suffix()

    if isinstance(input_path, list):
        python_files = input_path
    elif os.path.isdir(input_path):
        python_files = glob.glob(os.path.join(input_path, '*.py'))
    else:
        python_files.append(input_path)

    for python_file in python_files:
        module_name = os.path.splitext(os.path.basename(python_file))[0]

        # 编译Python文件为C扩展
        setup(
            ext_modules=cythonize([Extension(module_name, [python_file])], language_level="3"),
            script_args=["build_ext", "--build-lib", output_dir]
        )

        # 搜索匹配的编译文件并移动
        compiled_files = glob.glob(os.path.join(output_dir, module_name + extension))
        for compiled_file in compiled_files:
            print(f"Compiled extension available at {compiled_file}")

        # 删除生成的.c文件
        c_file = os.path.splitext(python_file)[0] + '.c'
        if os.path.exists(c_file):
            os.remove(c_file)
            print(f"Removed intermediate file: {c_file}")


def compile_folders(folders, output_dir_suffix=False):
    for folder in folders:
        if not output_dir_suffix:
            output_dir = folder
        else:
            output_dir = folder + output_dir_suffix
        # 调用已有的编译函数
        compile_and_move_extensions(folder, output_dir)



def delete_source_py(folders):
    for folder in folders:
        python_files = glob.glob(os.path.join(folder, '*.py'))
        for file in python_files:
            try:
                os.remove(file)
                print(f"Deleted source file: {file}")
            except Exception as e:
                print(f"Error deleting file {file}: {e}")