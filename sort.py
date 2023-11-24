import os
import re 
import shutil

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}

images = '/Users/anastasia/Desktop/test'
video = '/Users/anastasia/Desktop/test'
documents = '/Users/anastasia/Desktop/test'
audio = '/Users/anastasia/Desktop/test'
archives = '/Users/anastasia/Desktop/test'

file_trans = ''
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


def normalize_file (file):
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

def sort_by_fold (fold):


    if os.path.isdir(fold):
        if len(os.listdir(fold)) == 0:
            shutil.rmtree(fold)
        files = os.listdir(fold)
    
        for file in files:
            try:
                file = normalize_file (file)
                file = rename_file(file, file_trans)
                fold = os.path.join(fold, file)
            except FileNotFoundError:
                pass
            
            if os.path.isdir(file) is True:
                sort_by_fold (fold)

            else:
                if file.endswith(suffix_image):
                    if not os.path.exists(images):
                        os.makedirs(images)
                    image_l.append(file)
                    shutil.move(fold, images)


                elif file.endswith(suffix_video):
                    if not os.path.exists(video):
                        os.makedirs(video)
                    video_l.append(file)
                    shutil.move(fold, video)


                elif file.endswith(suffix_doc):
                    if not os.path.exists(documents):
                        os.makedirs(documents)
                    doc_l.append(file)
                    shutil.move(fold, documents)

                elif file.endswith(suffix_music):
                    if not os.path.exists(audio):
                        os.makedirs(audio)
                    music_l.append(file)
                    shutil.move(fold, audio)

                elif file.endswith(sufix_archive):
                    if not os.path.exists(archives):
                        os.makedirs(archives)
                    archive_l.append(file)
                    shutil.unpack_archive(file, archives)

                else:
                    not_found_l.append(file)
    

    return  group




group = sort_by_fold ('/Users/anastasia/Desktop/test')
print (group)
