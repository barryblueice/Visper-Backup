import os,sys,threading,time
import ujson as json
import shutil
from loguru import logger
from datetime import datetime
from func import (
    env_check,
    web,
    log_check,
    backup,
    hash
    )

if __name__ == '__main__':
    
    today = (datetime.today()).strftime("%Y-%m-%d")

    logger.add(f"{os.path.join(os.getcwd(),'logs',today)}.log", rotation="500 MB", retention="10 days", compression="zip")

    if '.env' not in os.listdir(os.getcwd()):
        logger.warning("未检测到.env文件，正在创建……")
        try:
            env_check.initial_env()
            logger.success('.env文件已成功创建，请修改相关变量后重启该程序！')
        except Exception as e:
            logger.error(f'错误：{e}')
        finally:
            sys.exit(0)

    else:
        source_path,target_backup_path,keeptime,webport=env_check.get_env()
        logger.info(f"备份源文件夹路径：{source_path}")
        logger.info(f"备份文件存放路径：{target_backup_path}")
        logger.info(f"保存时间：{keeptime} Day(s)")
        logger.info(f"WEBLOG端口：{webport}")
        
        if source_path == '':
            logger.error('错误：备份源文件夹路径变量无效！')
            sys.exit(0)
        elif target_backup_path == '':
            logger.error('错误：备份文件存放路径变量无效！')
            sys.exit(0)
        elif keeptime == '':
            logger.error('错误：保存时间变量无效！')
            sys.exit(0)
        elif webport == '':
            logger.error('错误：网络端口变量无效！')
            sys.exit(0)
        elif source_path == target_backup_path:
            logger.error('错误：备份目录和源目录不能一致！')
            sys.exit(0)
            
        try:
            os.mkdir(source_path)
        except:
            pass
        
        try:
            os.mkdir(target_backup_path)
        except:
            pass
            
        logger.info(f".env变量加载成功，正在启动WEBLOG服务器……")
        
        try:
            thread1 = threading.Thread(target=web.web_start, args=(int(webport),))
            thread1.start()
            logger.success('WEBLOG服务器加载成功……')
        except Exception as e:
            logger.error(f'WEBLOG服务器加载失败：{e}')
            sys.exit(0)
            
        logger.info(f'Visper Backup Tools启动成功！访问<ip>:{webport}以查看日志……')
        
        thread2 = threading.Thread(target=backup.hash_check)
        thread2.start()
        
        while True:
            
            if today != (datetime.today()).strftime("%Y-%m-%d"):
                
                today = (datetime.today()).strftime("%Y-%m-%d")
                
                try:
                    if len(os.listdir(os.path.join(target_backup_path))) > int(keeptime):
                        date_objects = sorted([datetime.strptime(date, "%Y-%m-%d") for date in (os.listdir(os.path.join(target_backup_path)))])
                        oldest_date = date_objects[0].strftime("%Y-%m-%d")
                        shutil.rmtree(os.path.join(target_backup_path,oldest_date))
                        logger.success(f"过旧的备份：{oldest_date}已清除……")
                except Exception as e:
                    logger.error(f'错误：{e}')

                try:
                    logger.info(f"开始执行备份任务")
                    backup.backup(output_path=os.path.join(target_backup_path,today,today+'.7z'),folder_path=source_path)
                    logger.success(f"压缩成功！")
                    logger.info(f'开始计算文件SHA256哈希值')
                    
                    hash_list = {}
                    
                    for i in os.listdir(os.path.join(target_backup_path,today)):
                        if not str(i).endswith('.json'):
                            target_hash = hash.calculate_file_sha256((os.path.join(target_backup_path,today,i)))
                            hash_list.update({i:target_hash})
                    with open(os.path.join(target_backup_path,today,'hash.json'),'w') as f:
                        json.dump(hash_list,f,indent=4)
                    logger.info(f'SHA256值已保存')
                    logger.success(f"备份任务执行成功！")
                except Exception as e:
                    logger.error(f"备份任务执行失败：{e}")
            
            time.sleep(60)