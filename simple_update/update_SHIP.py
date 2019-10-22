import getopt
import os
import shutil
import win32com.client
import subprocess
import sys
import fileinput


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
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    os.system('cls')
    sys.stdout.write('\n\nUpdate in progress:\n')
    sys.stdout.write('\r%s |%s| %s%s %s\n%s' % (prefix, bar, percents, '%', suffix, file))

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
    if os.path.isfile(sfile):
        shutil.copy2(sfile, dfile)
    filecount = 0
    with fileinput.FileInput(logfile, inplace=True,
                             backup='.bak') as file:
        for line in file:
            if line.find("number_of_files") >= 0:
                val = line.split("=")
                if val.__len__() > 1:
                    val = val[1]
                else:
                    val = 0
                newline = "number_of_files=" + str(int(val) + 1)
                filecount = str(int(val) + 1)
                print(newline, end='')
    print_progress(int(filecount), int(prevfilecount), prefix='Progress:', suffix='Complete', bar_length=50, file=sfile)


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


def main(argv):
    updateflag = True
    try:
        opts, args = getopt.getopt(argv, "", ["update"])
    except getopt.GetoptError:
        print('Wrong argument. Use -update')
        sys.exit(2)
    for opt, arg in opts:
        if opt in "update":
            updateflag = True
    else:
        if not os.path.exists(os.path.expandvars(r'%APPDATA%\SHIP')):
            os.makedirs(os.path.expandvars(r'%APPDATA%\SHIP'))
        print("Copying files to " + os.path.expandvars(r'%APPDATA%\SHIP'))
        num_of_files = 0
        with fileinput.FileInput(r'\\172.28.1.10\Dane\PUB\SHIP_Deployment\update.txt', inplace=True,
                                 backup='.bak') as file:
            for line in file:
                if line.find("number_of_files") >= 0:
                    val = line.split("=")
                    if val.__len__() > 1:
                        num_of_files = val[1]
                    else:
                        num_of_files = 0
                    newline = "number_of_files=" + str(0)
                    print(newline, end='')

        copyTree(r'\\172.28.1.10\Dane\PUB\SHIP_Deployment', os.path.expandvars(r'%APPDATA%\SHIP'),
                 r'\\172.28.1.10\Dane\PUB\SHIP_Deployment\update.txt', num_of_files)
        # if updateflag:
            # desktop = os.path.expanduser("~/Desktop")  # path to where you want to put the .lnk
            # path = os.path.join(desktop, 'SHIP.lnk')
            # target = os.path.expandvars(r'%APPDATA%\SHIP\SHIP.exe')
            # # icon = r'C:\path\to\icon\resource.ico'  # not needed, but nice
            # shell = win32com.client.Dispatch("WScript.Shell")
            # shortcut = shell.CreateShortCut(path)
            # shortcut.Targetpath = target
            # # shortcut.IconLocation = icon
            # shortcut.WindowStyle = 7  # 7 - Minimized, 3 - Maximized, 1 - Normal
            # shortcut.save()

    # subprocess.Popen(r'%systemdrive%\SHIP\SHIP.exe', shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    # (os.path.expandvars(r'%systemdrive%\SHIP\SHIP.exe'))


if __name__ == "__main__":
    main(sys.argv[1:])
