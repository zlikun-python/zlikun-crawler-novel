# 小说爬虫

#### 建模
```
# 小说表(novel)
[id, name, author, cover, origin_url, update_time]

# 章节表（novel_${novel_id}）
[id, title, content, origin_url, create_time]
```

#### 爬虫
```
# 构建爬虫镜像
$ docker build -t novel_crawler -f crawler/Dockerfile .

# 运行爬虫容器
$ docker run --rm --name novel_crawler --link mongo novel_crawler
```

#### 阅读
```
# 构建WEB镜像
$ docker build -t novel_web -f web/Dockerfile .

# 运行WEB容器
$ docker run --rm --name novel_web --link mongo -p 40020:80 novel_web
```

#### 构建
```
$ docker-compose up -d
```