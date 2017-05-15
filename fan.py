#!/usr/bin/python
#-*- coding:utf-8 -*-
import time,os,datetime
import RPi.GPIO as GPIO

GPIO_OUT=18 #我在树莓派上使用的引脚编号
FAN_MAX_TEMPERATURE=50 #风扇开启的临界值
FAN_MIN_TEMPERATURE=40 #风扇关闭的临界值
SLEEP_TIME=15 #温度检测的频率
LOG_PATH='/var/log/fan_control.log' #日志目录
IS_DEBUG=False

#获取温度
def read_cpu_temperature():
	with open("/sys/class/thermal/thermal_zone0/temp",'r') as f:
		temperature=round(float(f.read())/1000,0)
	log('DEBUG','Current CPU temperature is %s' % temperature)
	return temperature

#日志处理
def log(level,msg):
	log_msg='[%s]: %s (%s)' % (level,msg,datetime.datetime.now())
	if IS_DEBUG:
		print log_msg
		return
	try:
		with open(LOG_PATH,'a') as f:
			f.write(log_msg+'\n')
	except Exception as e:
		print "Unable to log, %s " % e

#开启风扇,此处需要注意的是
#网络上说开启风扇树莓派的引脚需要输出高电平
#但是经过本人亲自实验,开启风扇需要输出低电平
#这个可能跟我接的三极管的运作原理有关系
#我使用的三极管是S8550,查询后得知,该款三极管的B级(控制级)输出高电平时风扇断开，输出低电平风扇接通
def start_fan():
	log('INFO','fan power on.')
	GPIO.output(GPIO_OUT,GPIO.LOW)

#关闭风扇
def stop_fan():
	log('INFO','fan power off')
	GPIO.output(GPIO_OUT,GPIO.HIGH)

#初始化GPIO
def setup_GPIO():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(GPIO_OUT,GPIO.OUT)

#风扇控制的核心方法
def control_fan():
	is_close=True
	try:
		while True:
			temp=read_cpu_temperature()
			if is_close: #如果风扇是关闭的
				if temp>=FAN_MAX_TEMPERATURE:
					start_fan()
					is_close=False
			else:#如果风扇是开启的
				if temp<=FAN_MIN_TEMPERATURE:
					stop_fan()
					is_close=True
			time.sleep(SLEEP_TIME)
	except Exception as e:
		GPIO.cleanup()
		log('WARN',e)

if __name__=='__main__':
	os.environ["TZ"]='Asia/Shanghai'
	time.tzset()
	log('INFO','started.')
	setup_GPIO()
	stop_fan()
	control_fan()
	log('INFO','quit.')
