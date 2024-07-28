import subprocess
import os
import time
import shutil
from datetime import datetime
from loguru import logger
import ujson as json
from .hash import calculate_file_sha256
from .env_check import get_env

source_path,target_backup_path,keeptime,webport=get_env()

def backup(output_path,folder_path):
    
    chunk_size = 1 * 1024 * 1024 * 1024
    
    command = [
        '7z', 'a', '-t7z', '-v{}b'.format(chunk_size), output_path, folder_path
    ]
    
    subprocess.run(command, check=True)
    
def hash_check():
    today = (datetime.today()).strftime("%Y-%m-%d")
    logger.add(f"{os.path.join(os.getcwd(),'logs',today)}.log", rotation="500 MB", retention="10 days", compression="zip")
    while True:
        if os.path.exists(os.path.join(target_backup_path,today)):
            try:
                logger.info('开始执行SHA256检查任务')
                hash_list = {}
                for i in os.listdir(os.path.join(target_backup_path,today)):
                    if not str(i).endswith('.json'):
                        target_hash = calculate_file_sha256((os.path.join(target_backup_path,today,i)))
                        hash_list.update({i:target_hash})
                hash_error = False
                with open(os.path.join(target_backup_path,today,'hash.json'),'r') as f:
                    original_hash_data = json.load(f)
                
                for i in list(hash_list.keys()):
                    if hash_list[i] == original_hash_data[i]:
                        pass
                    else:
                        hash_error = True
                        logger.warning(f'文件{i} SHA256值出错！')
                        break
                
                if not hash_error:
                    logger.success('SHA256检查完成，未发现错误')
                    
                else:
                    try:
                        logger.info(f"开始重新执行备份任务")
                        shutil.rmtree(os.path.join(target_backup_path,today))
                        backup(output_path=os.path.join(target_backup_path,today,today+'.7z'),folder_path=source_path)
                        logger.success(f"压缩成功！")
                        logger.info(f'开始计算文件SHA256哈希值')
                        
                        hash_list = {}
                        
                        for i in os.listdir(os.path.join(target_backup_path,today)):
                            if not str(i).endswith('.json'):
                                target_hash = calculate_file_sha256((os.path.join(target_backup_path,today,i)))
                                hash_list.update({i:target_hash})
                        with open(os.path.join(target_backup_path,today,'hash.json'),'w') as f:
                            json.dump(hash_list,f,indent=4)
                        logger.info(f'SHA256值已保存')
                        logger.success(f"备份任务执行成功！")
                    except Exception as e:
                        logger.error(f"备份任务执行失败：{e}")
            except Exception as e:
                logger.error(f"SHA256检查任务执行失败：{e}")
                        
        time.sleep(3600)
            


# folder_path = '.\\4K'
# chunk_size = 1 * 1024 * 1024 * 1024

# compress_folder_7z(folder_path, chunk_size)