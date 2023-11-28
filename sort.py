import os
import re 
import shutil
import sys

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


def normalize (file):
    
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
        file_trans = file.translate(TRANS)
        
        file = file_trans

        file = re.sub(r'[^a-zA-Z0-9.]', '_', file)
    
        
        

    
    return file



def sort_by_fold (fold, first_path):

    images = first_path + '/images'
    video = first_path + '/video'
    documents = first_path + '/documents'
    audio = first_path + '/audio'
    archives = first_path + '/archives'
    not_found = first_path + '/not_found'
    fold_list = ['images', 'video', 'documents', 'audio', 'archives', 'not_found', '.DS_Store']

    if os.path.isdir(fold):
        
        if len(os.listdir(fold)) == 0:
            print('Empty folder. Deleting...', fold)
            shutil.rmtree(fold)
            return group
            
            
        else:
            files = os.listdir(fold)
        
        
        for file in files:
            if file in fold_list:
                continue
            

            try:
                
            
                path_file = os.path.join(fold, file)
                file_new = normalize(file)
                new_path = os.path.join(fold, file_new)
                
                os.rename(path_file, new_path)
                file = file_new
                


            except FileNotFoundError:
                print('File not found: ', new_path)

            
            if os.path.isdir(new_path) is True:
                
                if len(os.listdir(fold)) == 0:
                    print('Empty folder. Deleting...')
                    shutil.rmtree(fold)
                    continue
                    
            
                sort_by_fold (new_path, first_path)

                    

            else:
                if file.lower().endswith(suffix_image):
                    if not os.path.exists(images):
                        os.makedirs(images)
                    image_l.append(file)
                    try:
                        shutil.move(new_path, images)
                    except Exception as e:
                       print ("This file already exists: ", file)



                elif file.lower().endswith(suffix_video):
                    if not os.path.exists(video):
                        os.makedirs(video)
                    video_l.append(file)
                    try:
                        shutil.move(new_path, video)
                    except Exception as e:
                       print ("This file already exists: ", file)


                elif file.lower().endswith(suffix_doc):
                    if not os.path.exists(documents):
                        os.makedirs(documents)
                    doc_l.append(file)
                    try:
                        shutil.move(new_path, documents)
                    except Exception as e:
                       print ("This file already exists: ", file)

                elif file.lower().endswith(suffix_music):
                    if not os.path.exists(audio):
                        os.makedirs(audio)
                    music_l.append(file)
                    try:
                        shutil.move(new_path, audio)
                    except Exception as e:
                       print ("This file already exists: ", file)

                elif file.lower().endswith(sufix_archive):
                    if not os.path.exists(archives):
                        os.makedirs(archives + '/' + file.split('.')[0])
                    archive_l.append(file)
                    try:
                        shutil.unpack_archive(new_path, archives + '/' + file.split('.')[0])
                        os.remove(new_path)
                    except Exception as e:
                       print ("Something went wrong: ", e)
                       shutil.move(new_path, archives)


                else:
                    if not os.path.exists(not_found):
                        os.makedirs(not_found)
                    not_found_l.append(file)
                    shutil.move(new_path, not_found)

    
    return  group



def known_extension(group):
    pattern = r'\.([a-zA-Z0-9]+)$'
    all_names = ''
    known_extension_set = set()
    for list in group:
        if list is not_found_l:
            continue
        
        for name in list:
            all_names += name
            match = re.search(pattern, all_names)
            if match:
                known_extension_set.add(match.group())
            
    return known_extension_set


def unknown_extension(group):
    pattern = r'\.([a-zA-Z0-9]+)$'
    all_not_names = ''
    unknown_extension_set = set()   
    for name_not in not_found_l:
        all_not_names += name_not
        match = re.search(pattern, all_not_names)
        if match:
            unknown_extension_set.add(match.group())
        
    return unknown_extension_set


def remove_empty_folder(fold):
    if not os.path.isdir(fold):
        return

    for item in os.listdir(fold):
        item_path = os.path.join(fold, item)
        if os.path.isdir(item_path):
            remove_empty_folder(item_path) 

    
    if not os.listdir(fold):
        os.rmdir(fold)
        print(f"Deleted empty folder: {fold}")

def main():
    path_file = sys.argv[1]
    
    group = sort_by_fold (path_file, path_file)

    known_extension_set = known_extension (group)
    unknown_extension_set = unknown_extension(group)
    remove_empty_folder(path_file)
    print ('images = ', image_l, "; video = ", video_l, \
        "; documents = ", doc_l, '; music = ', music_l,\
            '; archives = ', archive_l, '; unknown = ', not_found_l,\
                '\n', 'Known_extension  =', known_extension_set, \
                '\n', 'Unknown_extension =', unknown_extension_set)
if __name__ == '__main__':
    main()
