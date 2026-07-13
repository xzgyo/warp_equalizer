# warp_equalizer
创建一堆Warp连接端，连接不同节点，并平均分流（通过docker compose）

## Useage
**示例命令：**
```shell
python3 main.py 8
```
第一个参数是同时启动的warp容器数量，示例中的是一次生成8个warp容器。  
---
将生成的`config.yaml`作为clash的配置文件，生成的`docker-compose.yml`则是可以直接使用的Docker Compose文件  

启动Clash Meta的启动命令示例：
```shell
docker run -it --name mihomo --hostname mihomo --network host --pid host --ipc host --cap-add CAP_NET_ADMIN --security-opt apparmor=unconfined -e LANG=C.UTF-8 -v /srv/mihomo/data:/root/.config/mihomo -v /dev/net/tun:/dev/net/tun -v /etc/localtime:/etc/localtime:ro --restart unless-stopped metacubex/mihomo:latest
```
这将会在`/srv/mihomo/data`目录下创建示例配置文件并自动下载GEOIP以及GEOSITE等数据  
此时配置文件的路径应为`/srv/mihomo/data/config.yaml`，直接将配置文件替换后重启服务即可。  
