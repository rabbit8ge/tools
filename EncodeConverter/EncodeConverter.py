# -*- coding: utf-8 -*-  
  
import codecs  
import os  
import sys
import shutil  
import re  
import chardet  
  
def convert_encoding(filename, target_encoding):  
    # Backup the origin file.  
    shutil.copyfile(filename, filename + '.bak')  
  
    # convert file from the source encoding to target encoding  
    content = codecs.open(filename, 'r').read()  
    source_encoding = chardet.detect(content)['encoding']  
    print source_encoding, filename  
    content = content.decode(source_encoding)  # .encode(source_encoding)  
    codecs.open(filename, 'w', encoding=target_encoding).write(content)  
  
def convert_folder(folder, fileext, target_encoding='utf-8'):
    '''
    @param fileext: it should be like '.java' with a dot.
    '''
    for root, dirs, files in os.walk(folder):  
        for f in files:
            if os.path.splitext(f)[1] == fileext:  
                filename = os.path.join(root, f)  
                try:  
                    convert_encoding(filename, target_encoding)  
                except Exception, e:  
                    print('failed to convert ', filename, 'to ', target_encoding)  
  
  
def process_bak_files(action='restore'):
    folder = sys.argv[1]
    ext = sys.argv[2]
    for root, dirs, files in os.walk(folder):  
        for f in files:  
            if f.lower().endswith('.java.bak'):  
                source = os.path.join(root, f)  
                target = os.path.join(root, re.sub('\.java\.bak$', ext, f, flags=re.IGNORECASE))  
                try:  
                    if action == 'restore':  
                        shutil.move(source, target)  
                    elif action == 'clear':  
                        os.remove(source)  
                except Exception, e:  
                    print source  
  
if __name__ == '__main__':
    # process_bak_files(action='clear')
    
    folder = sys.argv[1]
    fileext = sys.argv[2]
    target_encoding = sys.argv[3]
    convert_folder(folder, fileext, target_encoding) 
