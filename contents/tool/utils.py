import sys

def display_progress(percent):
    bar_length=20 #20个字符宽度的进度条;
    hashes = '>' * int(percent/100.0 * bar_length)
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("\rPercent: [%s] %d%%"%(hashes + spaces, percent))
    sys.stdout.flush()
    #time.sleep(0.01)


