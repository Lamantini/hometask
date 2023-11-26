import os
import re 
import shutil

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}



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
        file = file_trans
        
        

    
    return file



def sort_by_fold (fold):

    images = fold + '/images'
    video = fold + '/video'
    documents = fold + '/documents'
    audio = fold + '/audio'
    archives = fold + '/archives'
    not_found = fold + '/not_found'
    fold_list = ['images', 'video', 'documents', 'audio', 'archives', 'not_found']

    if os.path.isdir(fold):
        
        if len(os.listdir(fold)) == 0:
            print('Empty folder. Deleting...')
            shutil.rmtree(fold)
            
            
        else:
            files = os.listdir(fold)
        
        
        for file in files:
            if file == '.DS_Store':
                continue
            if file in fold_list:
                continue
            

            try:
                
                
                file_new = normalize_file(file)
                path_file = os.path.join(fold, file)
                new_path = os.path.join(fold, file_new)
                os.rename(path_file, new_path)
                file = file_new
                


            except FileNotFoundError:
                print('File not found: ', path_file)

            
            if os.path.isdir(path_file) is True:
                
                if len(os.listdir(fold)) == 0:
                    print('Empty folder. Deleting...')
                    shutil.rmtree(fold)
                    continue
                    
            
                sort_by_fold (path_file)

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



def Known_extension(group):
    pattern = r'\.([a-zA-Z0-9]+)$'
    all_names = ''
    Known_extension_set = set()
    for list in group:
        if list is not_found_l:
            continue
        
        for name in list:
            all_names += name
            match = re.search(pattern, all_names)
            if match:
                Known_extension_set.add(match.group())
            else:
                Known_extension_set.add("None")
    return Known_extension_set


def Unknown_extension(group):
    pattern = r'\.([a-zA-Z0-9]+)$'
    all_not_names = ''
    Unknown_extension_set = set()   
    for name_not in not_found_l:
        all_not_names += name_not
        match = re.search(pattern, all_not_names)
        if match:
            Unknown_extension_set.add(match.group())
        else:
            Unknown_extension_set.add("None")
    return Unknown_extension_set

group = sort_by_fold ('/Users/anastasia/Desktop/test2')
Known_extension_set = Known_extension (group)
Unknown_extension_set = Unknown_extension(group)

print ('images = ', image_l, "; video = ", video_l, \
       "; documents = ", doc_l, '; music = ', music_l,\
        '; archives = ', archive_l, '; unknown = ', not_found_l,\
            '\n', 'Known_extension  =', Known_extension_set, \
            '\n', 'Unknown_extension =', Unknown_extension_set)