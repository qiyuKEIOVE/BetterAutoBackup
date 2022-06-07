import os
import time
import yaml
import shutil
import datetime
from mcdreforged.api.all import *

PLUGIN_METADATA = {
    "id": "BAB",
    "version": "0.0.1",
    "name": "BetterAutoBcakup",
    "description": "XDDD",
    "author": "qiyuKEIOVE",
    "link": "https://github.com/qiyuKEIOVE/BetterAutoBcakup"
}
global command
global Mount_target
global World_name
global Plugin_data_route

command = "!!bab"
Mount_target = "/disks/hdd01/6ocB"
#Server_route = "./server"
World_name = "world"
Plugin_data_route = "./BetterAutoBackup"
#Reserved_space = 2048 #MB

global Timing
global BCtime
global Round
global Start_time
global Backup_times
global Auto_Btimes
global Op_Btimes
global Consle_Btimes

def first_run_check():
    if False == os.path.exists("./config/BetterAutoBackup.yml"):
        yaml.dump({"switch":"on","time":BCtime},open("./config/BetterAutoBackup.yml",'w',encoding='utf-8'))
    if False == os.path.exists(Plugin_data_route):
        os.mkdir(Plugin_data_route)
    if False == os.path.exists(Plugin_data_route + "/overwrite"):
        os.mkdir(Plugin_data_route + "/overwrite")

def help_message(source:InfoCommandSource):
    Help_message = RTextList("====== BetterAutoBackup-《插件使用帮助信息》 ======",
                             command + " help   查看本帮助信息\n",                                            
                             command + " stat   查看本插件状态\n",
                             command + " time   设置自动备份频率（分钟/次）\n",
                             command + " on     开启自动备份\n",
                             command + " off    关闭自动备份\n",
                             command + " backup 手动进行备份\n",                      
                             "TIPS:none\n")
    source.reply(Help_message)

def get_run_backup_type(source:CommandSource):
    if True == source.is_player:
        run_backup(server,"Player:" + source.player)
        Op_Btimes + 1
    else:
        run_backup(server,"Console")
        Consle_Btimes + 1

def run_backup(server:PluginServerInterface,Operation_type):
    first_run_check()
    Round = 0
    os.system("rm -rf " + Plugin_data_route + "/overwrite")
    os.mkdir(Plugin_data_route + "/overwrite")
    shutil.copytree("./" + yaml.load(open("./config.yml",encoding='utf-8'))['working_directory'] + "/" + World_name, Plugin_data_route + "/overwrite")
    os.system("tar -zcvf " + Mount_target + "/" +  str(time.time()) + ";" + time.strftime("%Y-%m-%d;%H:%M:%S") + ";" + Operation_type + ".tar.gz " + Plugin_data_route + "/overwrite" + "/")
    server.broadcast("备份完成！耗时" + Round + "秒")
    Round = 0

def on_switch(source:InfoCommandSource):
    first_run_check()
    yaml.dump({"switch":"on","time":yaml.load(open("./config/BetterAutoBackup.yml",encoding='utf-8'))['time']},open("./config/BetterAutoBackup.yml",'w',encoding='utf-8'))
    source.reply("定时备份功能已开启 频率为" + str(yaml.load(open("./config/BetterAutoBackup.yml",encoding='utf-8'))['time']) + "分钟/次")
    source.reply("插件状态已经更新 将在3秒后自动备份一次！")
    time.sleep(3)
    run_backup(server,"AutoBackup")
    Auto_Btimes + 1
    Timeing = 0   

def off_switch(source:InfoCommandSource):
    first_run_check()
    yaml.dump({"switch":"off","time":yaml.load(open("./config/BetterAutoBackup.yml",encoding='utf-8'))['time']},open("./config/BetterAutoBackup.yml",'w',encoding='utf-8'))
    source.reply("定时备份功能已关闭")

def change_time(source:InfoCommandSource,Ctime:dict):
    BCtime = Ctime
    first_run_check()
    yaml.dump({"switch":yaml.load(open("./config/BetterAutoBackup.yml",encoding='utf-8'))['switch'],"time":Ctime},open("./config/BetterAutoBackup.yml",'w',encoding='utf-8'))
    if Ctime == Timing == yaml.load(open("./config/BetterAutoBackup.yml",encoding='utf-8'))['time']:
        source.reply("备份频率已成功更改为" + str(Ctime) + "分钟/次")
        source.reply("插件状态已经更新 将在3秒后自动备份一次！")
        time.sleep(3)
        run_backup(server,"AutoBackup")
        Auto_Btimes + 1
        Timeing = 0
    else:
        change_time(source, BCtime)

def print_stat(source:InfoCommandSource):
    Runtime = int((datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S") - datetime.strptime(Start_time, "%Y-%m-%d %H:%M:%S")).second)
    Runtime_Turn = str(Runtime // 86400) + "天" + str(Runtime // 311040000) + "时" + str(Runtime // 18,662,400,000) + "分" + str(Runtime - (Runtime // 18,662,400,000)) + "秒"
    State_message = RTextList("++++++ BetterAutoBackup-<插件运行状态面板> ++++++\n",
                                "插件运行时间：{}\n".format(Runtime_Turn),
                                "总备份次数：{}次\n".format(str(int(Auto_Btimes + Op_Btimes + Consle_Btimes))),
                                "自动备份次数：{}次\n".format(str(int(Auto_Btimes))),
                                "玩家备份次数：{}次\n".format(str(int(Op_Btimes))),
                                "后台备份次数：{}次\n".format(str(int(Consle_Btimes))),
                                "（计数时间为插件被加载至目前）\n",
                                "插件版本：？"
                                )

def run_1():
    while True:
        time.sleep(60)
        Timing + 1
        if "on" == yaml.load(open("./config/BetterAutoBackup.yml",encoding='utf-8'))['switch']:
            if Timing == yaml.load(open("./config/BetterAutoBackup.yml",encoding='utf-8'))['time']:
                run_backup(server,"AutoBackup")
                server.broadcast("时间已到 开始自动备份...")
                Auto_Btimes + 1
            else:
                first_run_check()
                Timing - 1
        else:
            yaml.dump({"switch":"off","time":yaml.load(open("./config/BetterAutoBackup.yml",encoding='utf-8'))['time']},open("./config/BetterAutoBackup.yml",'w',encoding='utf-8'))
            server.broadcast("配置文件错误 定时备份功能已自动关闭 请使用[" + command + " on]以重新开启！")

def run_2():
    while True:
        time.sleep(1)
        Round + 1

def on_load(server:PluginServerInterface,old):  
    global Timing
    global BCtime
    global Round
    global Start_time
    global Backup_times
    global Auto_Btimes
    global Op_Btimes
    global Consle_Btimes

    Timing = 0
    Round = 0
    BCtime = 360
    Backup_times = 0
    Auto_Btimes = 0
    Op_Btimes = 0
    Consle_Btimes = 0
    Start_time = time.strftime("%Y-%m-%d %H:%M:%S")

    first_run_check()
    run_1()
    run_2()
    
    server.register_help_message("!!bab","获取BetterAutoBackup帮助信息")
    server.register_command(
        Literal("!!bab").runs(help_message).on_error(UnknownArgument,help_message).
            then(Literal("help").runs(help_message)).
            then(Literal("time").then(Integer("time").runs(set_time))).
            then(Literal("on").runs(on_switch())).
            then(Literal("off").runs(off_switch())).
            then(Literal("backup").runs(get_run_backup_type())).
            then(Literal("stat").runs(print_stat()))
    )
