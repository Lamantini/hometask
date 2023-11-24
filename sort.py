import os
import re 
import shutil

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}

image_l = []
video_l = []
doc_l = []
music_l = []
archive_l = []
not_found_l = []
group = (image_l, video_l, doc_l, music_l, archive_l, not_found_l)

suffix_image = ('.jpeg', '.png', '.jpg','.svg')
suffix_video = ('.avi', '.mp4', '.mov', '.mkv')
suffix_doc = ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx', '.pages')
suffix_music = ('.mp3', '.ogg', '.wav', '.amr')
sufix_archive = ('.zip', '.gz', '.tar')


def normalize_file(file):
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
        file_trans = file.translate(TRANS)
        file_trans = re.sub(r'\W, ^/.', '_', file_trans)

    print (file_trans)
    return file_trans

def rename_file(file, file_trans):
    file = os.rename(file, file_trans)

    return file

def sort_by_fold(fold):

    images = fold + '/images'
    video = fold + '/video'
    documents = fold + '/documents'
    audio = fold + '/audio'
    archives = fold + '/archives'
    not_found = fold + '/not_found'

    if os.path.isdir(fold):
        if len(os.listdir(fold)) == 0:
            print('Empty folder. Deleting...')
            shutil.rmtree(fold)
            
        files = os.listdir(fold)
    
        for file in files:
            try:
                file_trans = normalize_file(file)
                path_file = os.path.join(fold, file)
                os.rename(path_file, path_file.replace(file, file_trans))
                path_file = path_file.replace(file, file_trans)
                file = file_trans
            except FileNotFoundError:
                print('File not found: ', path_file)

            
            if os.path.isdir(path_file) is True:
                print('Folder: ', path_file)
                sort_by_fold(path_file)
            else:
                if file.endswith(suffix_image):
                    if not os.path.exists(images):
                        os.makedirs(images)
                    image_l.append(file)
                    shutil.move(path_file, images)


                elif file.endswith(suffix_video):
                    if not os.path.exists(video):
                        os.makedirs(video)
                    video_l.append(file)
                    shutil.move(path_file, video)


                elif file.endswith(suffix_doc):
                    if not os.path.exists(documents):
                        os.makedirs(documents)
                    doc_l.append(file)
                    shutil.move(path_file, documents)

                elif file.endswith(suffix_music):
                    if not os.path.exists(audio):
                        os.makedirs(audio)
                    music_l.append(file)
                    shutil.move(path_file, audio)

                elif file.endswith(sufix_archive):
                    if not os.path.exists(archives):
                        os.makedirs(archives + '/' + file.split('.')[0])
                    archive_l.append(file)
                    shutil.unpack_archive(path_file, archives + '/' + file.split('.')[0])
                    os.remove(path_file)
                else:
                    if not os.path.exists(not_found):
                        os.makedirs(not_found)
                    not_found_l.append(file)
                    shutil.move(path_file, not_found)
    

    return  group




group = sort_by_fold('test')
print (group)