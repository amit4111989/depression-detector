from eng_dict import data as dictionary
from math import sqrt
import os

def calculate_data(filename,folder):
    #remove words from .lab that are not in dict
    textfile = folder+'/'+filename+'.lab'
    with open(textfile,'r') as f:
        text = f.read().split(' ')
    
    new_text = []
    for i in range(len(text)):
        if text[i] in dictionary:
            new_text.append(text[i]) 
    #os.system('rm %s'%(text_file))
    with open(textfile,'w+') as f:
        f.write('%s'%(' '.join(new_text)))

    #run aligner to generate textgrid file
    os.system('python3 -m aligner -r ~/prosodylab/Prosodylab-Aligner/eng.zip -a %s -d ~/prosodylab/Prosodylab-Aligner/eng.dict'%(folder))
      
    #remove .lab file
    os.system('rm %s'%(textfile))
    
    #run praat scrip to generate formant values
    os.system('./praat get_formants.praat 0 results.txt %s/'%(folder))
    
    #parse result file
    with open(folder+'/'+'results.txt','r') as f:
        results = f.read().split('\n')
        results = [i.split('\t') for i in results]
        
    
    data = {'a':{},'i':{},'u':{}}
    vowel_a = ['AA1','AA2','AO0','AO1','AO2','AW0','AW1','AW2']
    vowel_i = ['IY1','IY0','IY2']
    vowel_u = ['OW0','OW1','OW2','UW0','UW1','UW2']
    #import ipdb; ipdb.set_trace() 
    data['a']['f1'] = 0.0
    data['i']['f1'] = 0.0
    data['u']['f1'] = 0.0
    data['a']['f2'] = 0.0
    data['i']['f2'] = 0.0
    data['u']['f2'] = 0.0
    data['a']['dur'] = 0.0
    data['i']['dur'] = 0.0
    data['u']['dur'] = 0.0
    count_a = 0.0
    count_i = 0.0
    count_u = 0.0
    #import ipdb; ipdb.set_trace()
    for row in results[1:-1]:
        if not row:
            continue
        if row[1] in vowel_a:
            count_a += 1
            data['a']['f1'] += float(row[2])
            data['a']['f2'] += float(row[3])
            data['a']['dur'] += float(row[4])
 
        if row[1] in vowel_i:
            count_i += 1
            data['i']['f1'] += float(row[2])
            data['i']['f2'] += float(row[3])
            data['i']['dur'] += float(row[4])
        
        if row[1] in vowel_u:
            count_u += 1
            data['u']['f1'] += float(row[2])
            data['u']['f2'] += float(row[3])
            data['u']['dur'] += float(row[4])
    
    # avg values
    if count_a == 0 or count_i==0 or count_u ==0:
        return(data,0)

    data['a']['f1'] = data['a']['f1']/count_a
    data['i']['f1'] = data['a']['f2']/count_a
    data['u']['f1'] = data['a']['dur']/count_a
    data['a']['f2'] = data['i']['f1']/count_i
    data['i']['f2'] = data['i']['f2']/count_i
    data['u']['f2'] = data['i']['dur']/count_i
    data['a']['dur'] = data['u']['f1']/count_u
    data['i']['dur'] = data['u']['f2']/count_u
    data['u']['dur'] = data['u']['dur']/count_u
    # calucalate area of the triangle with Heron's formula
    #import ipdb; ipdb.set_trace() 
    a = sqrt((data['a']['f1']-data['a']['f2'])**2 + (data['i']['f1']-data['i']['f2'])**2)
    b = sqrt((data['i']['f1']-data['i']['f2'])**2 + (data['u']['f1']-data['u']['f2'])**2)
    c = sqrt((data['a']['f1']-data['a']['f2'])**2 + (data['u']['f1']-data['u']['f2'])**2)
    s = (a+b+c)/2.0
    
    area = sqrt(s*(s-a)*(s-b)*(s-c))

    return (data,area)
    
if __name__=='__main__':
    results = calculate_data('sample','data_folder')
    print results
