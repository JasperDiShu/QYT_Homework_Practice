# 2020.03.09-Homework-file control

import os

os.mkdir('test')
os.chdir('test')
qytang1 = open('qytang1','w')
qytang1.write('test file\n')
qytang1.write('this is qytang\n')
qytang1.close()
qytang2 = open('qytang2','w')
qytang2.write('test file\n')
qytang2.write('qytang python\n')
qytang2.close()
qytang3 = open('qytang3','w')
qytang3.write('test file\n')
qytang3.write('this is python\n')
qytang3.close()
os.mkdir('qytang4')
# os.chdir('qytang4')
# qytang6 = open('qytang6', 'w')
# qytang6.write('this is qytang6\n')
# qytang6.close()
# qytang7 = open('qytang7', 'w')
# qytang7.write('this is qytang7\n')
# qytang7.close()
# os.chdir('..')
os.mkdir('qytang5')

filelist = os.listdir(os.getcwd())
print('文件中包含"qytang"关键字的文件为：')
print('方案一：')
for file_or_dir in filelist:
    if os.path.isfile(file_or_dir):
        filepath = os.path.join(os.getcwd(), file_or_dir)  # 一定要重新获取文件的path
        myfile = open(filepath, 'r')
        readout_str = myfile.read()
        if ('qytang' in readout_str):
            print('\t'+file_or_dir)
        myfile.close()

print('方案二：')
# 这是更优化的递归方案
# topdown的作用！
# True从主目录扫描到子目录
# False从子目录扫描到主目录
for root, dirs, files in os.walk(os.getcwd(), topdown=False):
    if files:
        for file in files:
            filepath = os.path.join(root, file)     # 一定要重新获取文件的path
            myfile = open(filepath,'r')             # 一定要重新获取文件的path，再打开，否则会说No such file or directory
            readout_str = myfile.read()  # http://www.itkeyword.com/doc/2729392219380542x489/ioerror-errno-2-no-such-file-or-directory
            if ('qytang' in readout_str):
                print('\t'+file)
            myfile.close()

# 完成清理工作(一)
# for x in filelist:
#     if os.path.isfile(x):
#         os.remove(x)
#     else:
#         os.rmdir(x)
# os.chdir('..')
# os.rmdir('test')

# 完成清理工作(二)
os.chdir('..')
for root, dirs, files in os.walk('test', topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))
os.removedirs('test')
