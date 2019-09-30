#!/bin/bash
echo "########################################################"
echo "#                                                      #"
echo "#                                                      #"
echo "#                                                      #"
echo "#                    稳健OJ管理系统                    #" 
echo "#                                                      #"
echo "#                   by:养正稳健IT社                    #"
echo "#                                                      #"
echo "#                                                      #"
echo "########################################################"
echo ""
echo ""
echo "1.启动"
echo "2.查看状态"
echo "3.更新"
echo "4.备份"
echo "5.导入数据(bate)"
echo "6.重启"
echo "7.关闭"
read -p "请输入代码：" num
if [ "$num" == "1" ]
    then
    docker-compose up -d
    read -s -p "按回车键继续……" continue
    reset
    ./oj.sh
elif [ "$num" == "2" ]
    then
    docker ps -a
    read -s -p "按回车键继续……" continue
    reset
    ./oj.sh
elif [ "$num" == "3" ]
    then
    git pull
    docker-compose pull && docker-compose up -d
    read -s -p "按回车键继续……" continue
    reset
    ./oj.sh
elif [ "$num" == "4" ]
    then
    cp -r data data_bak
    read -s -p "备份已完成，按回车键继续……" continue
    reset
    ./oj.sh
elif [ "$num" == "5" ]
    then
    echo "请确保题库文件已导入 /home/OnlineJudgeDeploy/data/backend/test_case 文件夹中"
    read -s -p "按回车键继续……" continue
    docker cp old_data.json oj-backend:/app/utils/
    docker exec -it oj-backend /bin/sh
    cd ./utils
    python3 migrate_data.py old_data.json
    read -s -p "按回车键继续……" continue
    reset
    ./oj.sh
elif [ "$num" == "6" ]
    then
    docker-compose restart
    read -s -p "按回车键继续……" continue
    reset
    ./oj.sh
elif [ "$num" == "7" ]
    then
    docker-compose stop
    read -s -p "按回车键继续……" continue
    reset
    ./oj.sh
fi
