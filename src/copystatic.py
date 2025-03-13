import os
import shutil

def copy_content(destination, source):
    src_dir_path = source
    
    #check if exists, if not, create
    if not os.path.exists(destination):
        os.mkdir(f"{destination}")

    # remove everything from public
    pub_dir = os.listdir(destination)
    for file in pub_dir:
        file_path = os.path.join(destination, file)
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)
    
    text = copy_recursive(src_dir_path,destination)    
    
def copy_recursive(src_dir_path, dest_dir_path) -> str:
        src_dir = os.listdir(src_dir_path)
        
        if not src_dir:
            return ""
        else:
            for file in src_dir:
                file_path = os.path.join(src_dir_path, file)
                if os.path.isdir(file_path):
                    os.mkdir(os.path.join(dest_dir_path,file))
                    return copy_recursive(
                        src_dir_path= os.path.join(file_path),
                        dest_dir_path=os.path.join(dest_dir_path,file))
                    
                else:
                    shutil.copy(src=file_path, dst=dest_dir_path)
                    
                    

