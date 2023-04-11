import sys
import json
import os
from pycocotools import mask as mask_utils
import random
import numpy as np 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#print(f"debugging info : {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}")

def defaultEncoder(obj):
    if type(obj).__module__ == np.__name__:
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj.item()
    raise TypeError('Unknown type:', type(obj))



class SkyDataDataset():

    def __init__(self, dataset_path="./gt_files/",gt_filename="train_SKYVOS.json"):
        self.gt_fol = dataset_path
        self.sampled_fake_submission = []

        if not os.path.exists(self.gt_fol):
            print("GT folder not found: " + self.gt_fol)

        with open(os.path.join(self.gt_fol, gt_filename)) as f:
            self.gt_data = json.load(f)

        # Get sequences to eval and check gt files exist
        self.seq_list = [vid['file_names'][0].split('/')[0] for vid in self.gt_data['videos']]
        self.seq_name_to_seq_id = {vid['file_names'][0].split('/')[0]: vid['id'] for vid in self.gt_data['videos']}
        self.seq_lengths = {vid['id']: len(vid['file_names']) for vid in self.gt_data['videos']}
        self.seq_dimensions = {vid['id']: {"height":vid['height'],"width":vid['width']} for vid in self.gt_data['videos']}
        
    def get_seq_dimensions(self, video_id):
        return self.seq_dimensions[video_id]["height"],self.seq_dimensions[video_id]["width"]

    def _prepare_n_annotations_from_gt(self,n=5):
        # only loaded when needed to reduce minimum requirements
        from pycocotools import mask as mask_utils

        self.sampled_fake_submission = []

        for j , track in enumerate (self.gt_data['annotations']):
            # TODO : height and width can be taken from the video metadata

            sequence_id_for_annotation=track['video_id']
            h,w = self.get_seq_dimensions(sequence_id_for_annotation)

            nth_track_dict ={
                "video_id": track['video_id'],
                "score": random.random(),
                "category_id": track['category_id'],
                "segmentations":[None] *  len(track['segmentations']),
            }

            
            for i, seg in enumerate(track['segmentations']):
                if seg:
                    track['segmentations'][i] = mask_utils.frPyObjects(seg, h, w)
                    track['segmentations'][i][0]["counts"] =track['segmentations'][i][0]["counts"].decode("utf-8")
                    track['segmentations'][i] = track['segmentations'][i][0]
                    # track['segmentations'][i] = mask_utils.area(track['segmentations'][i])
                    # track['segmentations'][i] = mask_utils.encode(track['segmentations'][i])[0]
                
                nth_track_dict['segmentations'][i] = track['segmentations'][i]
            
            self.sampled_fake_submission+=[nth_track_dict]

            if j == n:
                break
    
    def save_fake_submission(self, n=20):
        filename=f"./gt_files/fake_submission_from_gt_{n}.json"
        with open(filename, 'w') as f:
            json.dump(self.sampled_fake_submission, f,default=defaultEncoder)

    
    
if __name__ == "__main__":

    SkyDataDataset=SkyDataDataset()
    SkyDataDataset._prepare_n_annotations_from_gt(n=1000)
    SkyDataDataset.save_fake_submission(n=1000)









