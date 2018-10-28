import sys

def display_progress(percent,msg):
    bar_length=20 #20个字符宽度的进度条;
    hashes = '>' * int(percent/100.0 * bar_length)
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("\rPercent: [%s] %d%%[%s]"%(hashes + spaces, percent,msg))
    sys.stdout.flush()
    #time.sleep(0.01)


