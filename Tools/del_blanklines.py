# 去除文件中的空白行

in_file = input("请输入原始文件名称：")
out_file = input("请输入目标文件名称：")


def delblankline(infile, outfile):
    infopen = open(infile, 'r')
    outfopen = open(outfile, 'w')
    lines = infopen.readlines()
    for line in lines:
        if line.split():
            outfopen.writelines(line)
        else:
            outfopen.writelines("")
    infopen.close()
    outfopen.close()


delblankline(in_file, out_file)

print("%s文件中的空格已删除，保存为%s" % (in_file, out_file))
