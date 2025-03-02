import pandas as pd
from pathlib import Path
import re

## Matches frames to words, ignores empty frames.
def frames_only(data):
    frame = []
    for i in range(data.shape[0]):
        row = data.iloc[i]
        f = list(zip(row['sents'],row['frames']))
        ff = [x for x in f if x[1] != '|']
        frame.append([ff])
    return frame

def frame_counter(data):
    for w in data:
        if w != '|':
            if w in frame_count:
                frame_count[w] += 1
            else:
                frame_count[w] = 1
        else:
            pass
    return 'Frames counted.'

if __name__ == '__main__':
   in_path = ''
   pathlist = Path(in_path).rglob('*.csv')

   for path in pathlist:
       file_path  = str(path)
       df = pd.read_csv(file_path)
       df.rename(columns={'0':'sents','1':'frames'}, inplace=True)

       sdf = df.copy()
       sdf['sents'] = sdf['sents'].str.split()
       sdf['frames'] = sdf['frames'].str.split()
       
       frames = frames_only(sdf)
       fdf = pd.DataFrame(frames,columns=['ne_frames'])
       tois = pd.concat([df, fdf], axis=1)
       
       frame_count = {}
       sdf_nona = sdf.dropna(how='all')
       sdf_nona['frames'].apply(frame_counter)
       frames_df = pd.DataFrame(frame_count.items())

       pattern = r"(?<=\/)[a-zäöå]{3,}(?=\_)"
       match = re.findall(pattern,file_path)

       outfile = f'Data/{match[0]}_frames.csv'
       frames_df.to_csv(outfile, index = False)

       tois.to_csv(file_path, index = False)
       print('Written: '+file_path+' to folder.')

   