#!/bin/sh

python_dir="/usr/bin/python"

run_dir=$(pwd)

function boot(){
	`$python_dir "$run_dir/boot.py"`
}

function checkprocess(){
    return $(ps aux|grep -v grep|grep "$1"|wc -l)
}

function checkInternet(){
	return $(ping -c 3 "www.baidu.com"|awk 'NR==7 {print $4}')
}

checkprocess "boot.py"

result=$?

if [ $result -ge 1 ]; then
	checkInternet
	res=$?
	if [ $res -eq 0 ]; then
		kill -s `ps aux|grep -v grep|grep 'boot.py'|awk '{print $2}'`
	fi
	echo "active"
else
	boot
fi