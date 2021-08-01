from os import walk 
from os import path 
from os import makedirs
import cv2 
import shutil 
dir_path = path.dirname(path.realpath(__file__))


files = []


def list_folders(folder_path):
    return [ path.join(folder_path,  folder)  for folder in  next(walk( folder_path), (None, None, []))[1] ] 

def list_video_files(folder_path):
    return [ path.join(folder_path, file)  for file in next(walk(folder_path), (None, None, []))[2] if path.splitext(file)[1] == '.avi'  ] 

def list_all(folder_path):
    all = next(walk(folder_path), (None, None, []))
    return [ path.join(folder_path, file)  for file in all[2] if path.splitext(file)[1] == '.avi'  ] ,  [ path.join(folder_path,  folder)  for folder in all[1] ] 



def list_video_files(path):

    files, folders =list_all(path)
    if not files: 
        files = []
    while(len(folders) > 0):
        folder = folders.pop(0)
        new_files, new_folders = list_all(folder)
        files.extend(new_files)
        folders.extend(new_folders)
    return files

def extractImages(pathIn, pathOut):
    try:
        count = 0
        vidcap = cv2.VideoCapture(pathIn)
        success,image = vidcap.read()
        success = True
        video_duration = vidcap.get(cv2.CAP_PROP_FRAME_COUNT) / vidcap.get(cv2.CAP_PROP_FPS) 
        print("video duration is... " + str(video_duration))
        while success:
            cv2.imwrite( pathOut + "\\frame%d.jpg" % count, image)     # save frame as JPEG file
            vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*333))    # added this line 
            success,image = vidcap.read()
            print ('Read a new frame: ', success)
            count = count + 1
            if( count*333 >= (video_duration * 1000) ): 
                break
        vidcap.release()
    except:
        print('There was aan exception in extractImages')
        pass


##folder = next(walk(path.join(dir_path,  'UCF11_updated_mpg')), (None, None, []))[1] 

#list_files_recursive(path.join(dir_path,  'UCF11_updated_mpg'))
#print(files)

import subprocess
import os



def convert_videos_avi(src):
    for root, dirs, filenames in os.walk(src, topdown=False):
        #print(filenames)
        for filename in filenames:
            print('[INFO] 1',filename)
           
            _format = ''
            if ".flv" in filename.lower():
                _format=".flv"
            elif ".mp4" in filename.lower():
                _format=".mp4"
            elif ".avi" in filename.lower():
                _format=".avi"
            elif ".mpg" in filename.lower():
                _format=".mpg"
            else:
                continue

            inputfile = os.path.join(root, filename)
            print('[INFO] 1',inputfile)
            outputfile = os.path.join(root, filename.lower().replace(_format, ".avi"))
            print('[INFO] 2', outputfile)
            subprocess.call('ffmpeg -i ' + inputfile + ' ' + outputfile, shell=True, env={'PATH': os.getenv('PATH')})  
           


video_paths =  list_video_files("C:\\Users\\jrsla\\Downloads\\UCF50\\UCF50") 
print(video_paths)
#convert_videos_avi( path.join(dir_path,  'UCF11_updated_mpg') )

# cap = cv2.VideoCapture('C:\\Users\\josue.rabanales\\Documents\\action_recognition\\test1\\UCF11_updated_mpg\\UCF11_updated_mpg\\basketball\\v_shooting_01\\v_shooting_01_01.mpg')
# # Check if camera opened successfully
# if (cap.isOpened()== False): 
#   print("Error opening video  file")

# print(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS) )
# print('Frames per second: ', cap.get(cv2.CAP_PROP_FPS))
# print('Frame count: ' , cap.get(cv2.CAP_PROP_FRAME_COUNT))
# print(cap.get(cv2.CAP_PROP_POS_MSEC)*1000)
# # Read until video is completed
# while(cap.isOpened()):
      
#   # Capture frame-by-frame
#   ret, frame = cap.read()
#   if ret == True:
   
#     # Display the resulting frame
#     cv2.imshow('Frame', frame)
   
#     # Press Q on keyboard to  exit
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#       break
   
#   # Break the loop
#   else: 
#     break
   
# # When everything done, release 
# # the video capture object


# cap.release()
   
# # Closes all the frames
# cv2.destroyAllWindows()
# cap.set(cv2.CAP_PROP_POS_AVI_RATIO,1)





#makedirs('C:\\Users\\josue.rabanales\\Documents\\action recognition\\test1\\UCF11_updated_mpg\\UCF11_updated_mpg\\walking\\v_walk_dog_25\\v_walk_dog_25_04')
#extractImages('C:\\Users\\josue.rabanales\\Documents\\action recognition\\test1\\UCF11_updated_mpg\\UCF11_updated_mpg\\walking\\v_walk_dog_25\\v_walk_dog_25_04.mpg', 'C:\\Users\\josue.rabanales\\Documents\\action recognition\\test1\\UCF11_updated_mpg\\UCF11_updated_mpg\\walking\\v_walk_dog_25\\v_walk_dog_25_04')

for video in video_paths:
    new_folder_path_name = path.splitext(video)[0]
    try:
        print('Trying to make frames of video '+ video + " in  "+ new_folder_path_name + " ...")
        makedirs(new_folder_path_name)
        extractImages(video, new_folder_path_name )
        #shutil.rmtree(new_folder_path_name)
        #convert_videos_avi()
    except:
        print('There was an exception..')
    #makedirs(new_folder_path_name)
    #extractImages(video, new_folder_path_name)

print("DONE!")

#print(list_video_files( path.join(dir_path,  'UCF11_updated_mpg')) )


#print(list_video_files('C:\\Users\\josue.rabanales\\Documents\\action recognition\\test1\\UCF11_updated_mpg\\UCF11_updated_mpg\\basketball\\v_shooting_01'))
