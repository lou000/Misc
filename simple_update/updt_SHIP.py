import getopt
import os
import shutil
import win32com.client
import subprocess
import sys
import fileinput
import ctypes

FILE_COUNT = 0


def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100, file=""):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    if total == 0:
        total = 1
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write('\33[2K\r\33[F\33[F\33[F\33[F')
    sys.stdout.write("\n\nCopying files to %s\n" % os.path.expandvars(r'%APPDATA%\SHIP'))
    sys.stdout.write('%s |%s| %s%s %s\n%s' % (prefix, bar, percents, '%', suffix, file))

    # \33[2K\r
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


def forceMergeFlatDir(srcDir, dstDir, logfile, prevfilecount):
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)
    for item in os.listdir(srcDir):
        srcFile = os.path.join(srcDir, item)
        dstFile = os.path.join(dstDir, item)
        forceCopyFile(srcFile, dstFile, logfile, prevfilecount)


def forceCopyFile(sfile, dfile, logfile, prevfilecount):
    global FILE_COUNT
    if os.path.isfile(sfile) and not sfile == r'\\172.28.1.10\Dane\PUB\SHIP_Deployment\updt_SHIP.exe':
        shutil.copy2(sfile, dfile)
        FILE_COUNT += 1
    print_progress(int(FILE_COUNT), int(prevfilecount), prefix='Progress:', suffix='Complete', bar_length=50,
                   file=sfile)


def isAFlatDir(sDir):
    for item in os.listdir(sDir):
        sItem = os.path.join(sDir, item)
        if os.path.isdir(sItem):
            return False
    return True


def copyTree(src, dst, logfile, prevfilecount):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isfile(s):
            if not os.path.exists(dst):
                os.makedirs(dst)
            forceCopyFile(s, d, logfile, prevfilecount)
        if os.path.isdir(s):
            isRecursive = not isAFlatDir(s)
            if isRecursive:
                copyTree(s, d, logfile, prevfilecount)
            else:
                forceMergeFlatDir(s, d, logfile, prevfilecount)


def main():
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    if not os.path.exists(os.path.expandvars(r'%APPDATA%\SHIP')):
        os.makedirs(os.path.expandvars(r'%APPDATA%\SHIP'))
    num_of_files = 0
    with fileinput.FileInput(r'\\172.28.1.10\Dane\PUB\SHIP_Deployment\update.txt') as file:
        for line in file:
            if line.find("number_of_files") >= 0:
                val = line.split("=")
                if val.__len__() > 1:
                    num_of_files = val[1]
                else:
                    num_of_files = 0

    copyTree(r'\\172.28.1.10\Dane\PUB\SHIP_Deployment', os.path.expandvars(r'%APPDATA%\SHIP'),
             r'\\172.28.1.10\Dane\PUB\SHIP_Deployment\update.txt', num_of_files)
    with fileinput.FileInput(r'\\172.28.1.10\Dane\PUB\SHIP_Deployment\update.txt', inplace=True) as file:
        for line in file:
            if line.find("number_of_files") >= 0:
                newline = "number_of_files=" + str(FILE_COUNT)
                print(newline)
            else:
                print(line, end='')

    desktop = os.path.expanduser("~/Desktop")  # path to where you want to put the .lnk
    path = os.path.join(desktop, 'SHIP.lnk')
    target = os.path.expandvars(r'%APPDATA%\SHIP\SHIP.exe')
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WindowStyle = 7  # 7 - Minimized, 3 - Maximized, 1 - Normal
    shortcut.save()
    subprocess.Popen(r'%APPDATA%\SHIP\SHIP.exe', shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)


if __name__ == "__main__":
    main()
