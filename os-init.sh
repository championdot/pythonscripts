#!/bin/bash

#yum install -y  nload dnstop telnet nmap nc redhat-lsb vim

#if [ `lsb_release -a|grep Release|awk '{print $2}'|awk -F . '{print $1}'` -eq 6 ]; then
if [ `cat /etc/redhat-release |awk -F . '{print $1}'|awk '{print $NF}'` -eq 6 ]; then
#centos 6
#增加系统命令操作时间

if [ `cat /etc/bashrc |grep HISTTIMEFORMAT|wc -l` -eq 0 ]; then
        echo 'export HISTTIMEFORMAT="%F  %T  `whoami`   "' >> /etc/bashrc
else
        echo "histtimefommat is exist"
fi
#初始化关闭不必要的服务
source /etc/bashrc
export LANG=en
chkconfig --list|grep 3:on|grep -v -E "crond|network|rsyslog|syslog|sysstat|sshd"|awk '{print $1}'|xargs -t -i{} service {} stop
chkconfig --list|grep 3:on|grep -v -E "crond|network|rsyslog|syslog|sysstat|sshd"|awk '{print $1}'|xargs -t -i{} chkconfig {} off

#统一字符集
cp /etc/sysconfig/i18n /etc/sysconfig/i18n.bak
cat > /etc/sysconfig/i18n <<EOF
LANG="zh_CN.UTF-8"
SUPPORTED="zh_CN.GBK:zh:zh_CN.GB2312:zh:zh_CN.UTF-8:zh_CN:zh:en_US.UTF-8:en_US:en"
SYSFONT="lat0-sun16"
EOF
#
cp /etc/ssh/sshd_config  /etc/ssh/sshd_config.bak
cat > /etc/ssh/sshd_config <<EOFEOF
Port 22
Protocol 2
SyslogFacility AUTHPRIV
PasswordAuthentication yes
PermitRootLogin yes
ChallengeResponseAuthentication no
UseDNS no
X11Forwarding no
Subsystem sftp /usr/libexec/openssh/sftp-server
EOFEOF
#关闭SELINUX
sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config
#调整默认打开文件个数
if [ `cat /etc/security/limits.conf |grep ^*|wc -l` -eq 0 ]; then
        sed -i 's/1024/65535/g' /etc/security/limits.d/90-nproc.conf
        sed -i '/End of file/i\* soft nproc 65535' /etc/security/limits.conf 
        sed -i '/End of file/i\* hard nproc 65535' /etc/security/limits.conf 
        sed -i '/End of file/i\* soft nofile 65535' /etc/security/limits.conf 
        sed -i '/End of file/i\* hard nofile 65535' /etc/security/limits.conf 
else
        echo "open files is exist"
fi
#time_wait
if [ `cat /etc/sysctl.conf |grep "^net.ipv4.tcp_keepalive_time"|wc -l` -eq 0 ]; then
cat >> /etc/sysctl.conf <<EOFEOF
#内核要发送多少个 SYN 连接请求才决定放弃,默认值是5,对应于180秒左右时间.
net.ipv4.tcp_syn_retries=2
#关闭TCP连接之前重试多少次。缺省值是7，相当于50秒~16分钟(取决于RTO).
net.ipv4.tcp_orphan_retries=3
#保持在FIN-WAIT-2状态的时间
net.ipv4.tcp_fin_timeout=30
#表示SYN队列的长度，默认为1024
net.ipv4.tcp_max_syn_backlog=8192
#允许Time-wait sockets重新用于新的TCP连接
net.ipv4.tcp_tw_reuse=1
#开启TCP连接中Time-wait sockets的快速回收
net.ipv4.tcp_tw_recycle=1
#每个网络接口接收数据包速率比内核处理这些包的速率快时，允许送到队列的数据包的最大数目。
net.core.netdev_max_backlog=3000
#当启用keepalive时，默认120分钟。
net.ipv4.tcp_keepalive_time=30
net.ipv4.tcp_keepalive_probes=1
net.ipv4.tcp_keepalive_intvl=2
EOFEOF
sysctl -p
else
        echo "time_wait is exist"
fi


elif [ `cat /etc/redhat-release |awk -F . '{print $1}'|awk '{print $NF}'` -eq 7 ]; then
#centos 7
if [ `cat /etc/bashrc |grep HISTTIMEFORMAT|wc -l` -eq 0 ]; then
        echo 'export HISTTIMEFORMAT="%F  %T  `whoami`   "' >> /etc/bashrc
else
        echo "histtimefommat is exist"
fi
#
source /etc/bashrc
#
export LANG=en
systemctl list-unit-files|grep enabled|egrep -v "crond|NetworkManager|rsyslog|sshd"|awk '{print $1}'|grep -v @ |xargs -n 1 -i{} systemctl disable {}
#
cp /etc/locale.conf /etc/locale.conf.bak
cat > /etc/locale.conf  <<EOF
LANG="zh_CN.UTF-8"
SUPPORTED="zh_CN.GBK:zh:zh_CN.GB2312:zh:zh_CN.UTF-8:zh_CN:zh:en_US.UTF-8:en_US:en"
SYSFONT="lat0-sun16"
EOF
#
cat > /etc/ssh/sshd_config <<EOFEOF
Port 22
Protocol 2
SyslogFacility AUTHPRIV
PasswordAuthentication yes
PermitRootLogin yes
ChallengeResponseAuthentication no
UseDNS no
X11Forwarding no
Subsystem sftp /usr/libexec/openssh/sftp-server
EOFEOF

sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config
#open files
if [ `cat /etc/security/limits.conf |grep ^*|wc -l` -eq 0 ]; then
                    sed -i 's/1024/65535/g' /etc/security/limits.d/90-nproc.conf
        sed -i '/End of file/i\* soft nproc 65535' /etc/security/limits.conf
        sed -i '/End of file/i\* hard nproc 65535' /etc/security/limits.conf
        sed -i '/End of file/i\* soft nofile 65535' /etc/security/limits.conf
        sed -i '/End of file/i\* hard nofile 65535' /etc/security/limits.conf
else
        echo "open files is exist"
fi

#time_wait
if [ `cat /etc/sysctl.conf |grep "^net.ipv4.tcp_keepalive_time"|wc -l` -eq 0 ]; then
cat >> /etc/sysctl.conf <<EOFEOF
#内核要发送多少个 SYN 连接请求才决定放弃,默认值是5,对应于180秒左右时间.
net.ipv4.tcp_syn_retries=2
#关闭TCP连接之前重试多少次。缺省值是7，相当于50秒~16分钟(取决于RTO).
net.ipv4.tcp_orphan_retries=3
#保持在FIN-WAIT-2状态的时间
net.ipv4.tcp_fin_timeout=30
#表示SYN队列的长度，默认为1024
net.ipv4.tcp_max_syn_backlog=8192
#允许Time-wait sockets重新用于新的TCP连接
net.ipv4.tcp_tw_reuse=1
#开启TCP连接中Time-wait sockets的快速回收
net.ipv4.tcp_tw_recycle=1
#每个网络接口接收数据包速率比内核处理这些包的速率快时，允许送到队列的数据包的最大数目。
net.core.netdev_max_backlog=3000
#当启用keepalive时，默认120分钟。
net.ipv4.tcp_keepalive_time=30
net.ipv4.tcp_keepalive_probes=1
net.ipv4.tcp_keepalive_intvl=2
EOFEOF
sysctl -p
else
        echo "time_wait is exist"
fi


fi