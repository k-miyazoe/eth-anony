FROM --platform=linux/x86_64 mysql:5.7

EXPOSE 3306

#MySQL設定ファイルをイメージ内にコピー
ADD ./mysql/my.cnf /etc/mysql/conf.d/my.cnf
#Todo コマンドの意味を調べる
CMD ["mysqld"]