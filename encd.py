import face_recognition as fr
from pathlib import Path
import os

def get_encoded_faces(folder, names, image):
    """
    looks through the faces folder and encodes all
    the faces

    

    :return: dict of (name, image encoded)
    """

    encoded = []
    i = 0
    ##If You have just one image each person and want them to be recognized by thier image name rather than having many pictures of people and putting them in a single file with a name so they will be recognized by their filename(with better accuracy) then uncomment these lines and comment lines from line 30-53
    # for file in Path(folder).glob('*'):
    #     for dirpath, dnames, fnames in os.walk(f'./{file}'):
    #         for f in fnames:
    #             if "." in f:
    #                 face = fr.load_image_file(f'{file}/{f}')
    #                 encoding = fr.face_encodings(face)[0]
    #                 if '.' in f:
    #                     f = f.split('.')
    #                     f.pop(1)
    #                     f = str(f[0])
    #                 names.append(f), image.append(encoding)

    ##You can make a folder inside your known faces folder and name the folder the name you want those to be recognized(the person's name) name and add all the pictures you have of him(BEST ACCURACY) but if you have only one pic of him you can put his pic by his name and save it directly in the root folder
    for file in Path(folder).glob('*'):
        for dirpath, dnames, fnames in os.walk(f'./{file}'):
            for f in fnames:
                face = fr.load_image_file(f'{file}/{f}')
                encoding = fr.face_encodings(face)[0]
                fl = str(file)
                fl = fl.split("\\")
                fl.pop(0)
                fl = str(fl[0])
                names.append(fl), image.append(encoding)

    for filename in os.listdir(folder):
        f_names = os.path.join(folder, filename)
        if '.' in f_names:
            face = fr.load_image_file(f_names)
            encoding = fr.face_encodings(face)[0]
            if '.' in f_names:
                s = f_names.split('.')
                s.pop(1)
                s = str(s[0])
                s = s.split("\\")
                s.pop(0)
                s = str(s[0])
            names.append(s), image.append(encoding)
