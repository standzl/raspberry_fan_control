# raspberry_fan_control
树莓派温控风扇脚本

基于S8550三极管来控制风扇的开启和关闭，三极管的控制级使用的是18号GPIO接口

另外需要注意的是,在脚本中风扇启动设置是将18号引脚设置为低电平，风扇关闭设置的是高电平

这个跟S8550的运作原理有关
