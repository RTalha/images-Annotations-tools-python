import cv2
import numpy as np
import os
import argparse
# from  yolotococo_ak import bboxYoloToCoco


def bboxYoloToCoco(ls,imgshape):
    # print(ls)
    x1,y1,x2,y2=ls
    height,width=imgshape
    if height==-1:
        return -1,-1,-1,-1
    x1,y1,x2,y2=float(x1),float(y1),float(x2),float(y2)
    x2=x2*width
    y2=y2*height
    x1=(x1*width)-(x2/2)
    y1=(y1*height)-(y2/2)
    return int(x1),int(y1),int(x1+x2),int(y1+y2)


def start (ann_dir,img_dir,result_dir):
	over=False
	if not os.path.exists(result_dir):
		os.mkdir(result_dir)
	ls_sorted=os.listdir(os.path.join(os.getcwd(),ann_dir))
	# print(lambda x: int("".join([i for i in x if i.isdigit()])))
	# ls_sorted=sorted(ls, key=lambda x: int("".join([i for i in x if i.isdigit()])))
	imgind=0
	while imgind>=0 and imgind<len(ls_sorted):
		file_name=ls_sorted[imgind]
		print(file_name)
		if not file_name in ['classes.txt']:
			img_name=list(os.path.splitext(file_name))
			img_name[-1]='jpg'
			img_name='.'.join(img_name)
			ann_name=os.path.join(os.getcwd(),ann_dir,file_name)
			fimg_name=os.path.join(os.getcwd(),img_dir,img_name)
			# img=cv2.imread(fimg_name)
			anns=[i.strip() for i in open(ann_name,'r').readlines()]
			an_w=open(ann_name,'r').readlines()
			anns_bk=anns
			ind=0
			while ind<len(anns) and not over:
				j=anns[ind]
				img=cv2.imread(fimg_name)
				print(img)
				x1,y1,x2,y2=bboxYoloToCoco(list(map(float,j.split()))[1:],img.shape[:-1])
				cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),5)
				while ind<len(anns) and not over:
					cv2.imshow(str(img_name),img)
					keypress=cv2.waitKey(1)
					if keypress==ord('d'):
						ind+=1
						break
					elif keypress==ord('x'):
						anns.pop(ind)
						an_w.pop(ind)
						ind+1
						break
					elif keypress==ord('a'):
						ind-=1
						if ind<0:
							imgind-=2
							ind=0
						break
					elif keypress==ord('q'):
						over=True
						break
					elif keypress==ord('r'):
						anns=[i.strip() for i in open(ann_name,'r').readlines()]
						an_w=open(ann_name,'r').readlines()
						anns_bk=anns
			imgind+=1
			cv2.destroyWindow(str(img_name))
			rf=open(os.path.join(result_dir,file_name),'w')
			rf.write(''.join(an_w))
			rf.close()
			if over :
				break
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--ann", type=str,
                    default="ann/", dest="ann")
parser.add_argument("-i", "--img", type=str, default="images", dest="images",
                    help='Use ":amazon" for amazon filer')
parser.add_argument("-r", "--result", type=str, default="results", dest="results")

args = vars(parser.parse_args())
ann_dir=args['ann']
img_dir=args['images']
result_dir=args['results']
start(ann_dir,img_dir,result_dir)