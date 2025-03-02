import pandas as pd
import math
from pathlib import Path
import re
    
def ff_icf(t,f,m,n):
    '''Takes in a frame count for a TOI and calculates the FF-ICF.
    t is the total number of frames for frame in question, f is the total frames for subcorpus
    m is the total number of documents, and n is the total count for frame in question in corpus'''
    prod = t/f
    lsum = math.log(m/n)
    return prod*lsum

def no_common_frames(data):
    # Removes frames which are not required for analysis.
    df = data.drop(data[data['0'] == '|People|'].index)
    df = df.drop(df[df['0'] == '|Existence|'].index)
    df = df.drop(df[df['0'] == '|Possession|'].index)
    return df

def typical_frames(data, m, total):
    # Total number of all frames for toi
    icf_values = []
    fi = data['1'].sum()
    
    for i, r in data.iterrows():
        # Total # of specific frame for toi
        ti = r['1']
        # Frame name
        tt = r['0']
        # Total # of specific frame in corpus
        tx = total[total['0'] == tt].index[0]
        tn = total[tx,1]
        
        result = ff_icf(ti,fi,m,tn)
        icf_values.append(result)
        
    data = data['ff_icf'] = icf_values
    return data
        

if __name__== '__main__':
    # DF of frames for entire corpus.
    file = ''
    frame_df = pd.read_csv(file)
    total_docs = len(frame_df) 

    # DF of frames for each TOI
    in_path = ''
    pathlist = Path(in_path).rglob('*.csv')
    for path in pathlist:
        file_path  = str(path)
        df = pd.read_csv(file_path)
        
        df = no_common_frames(df)

        result_df = typical_frames(df,total_docs,frame_df)
        
        pattern = r"(?<=\/)[a-zäöå]{3,}(?=\_)"
        match = re.findall(pattern,file_path)
        outfile = f'data/output_{match[0]}.csv'
        
        result_df.to_csv(file_path, index=False)
        