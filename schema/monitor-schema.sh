#!/usr/bin/env bash

## 利用inotify监控本文件夹，然后合并
## 可以后台持续
## nohup /.../this.sh  > /.../that.log 2>&1 &


inotifywait -q -m -e modify,move,create,delete,close_write .  --format '"%w" "%f" "%e" "%T"' --timefmt '%F %T' \
    | while read DIR FILE EVENT TIME ; do echo $DIR $FILE $EVENT $TIME ; ./schematone.sh ; done
