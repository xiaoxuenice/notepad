# 下载地址
curl  https://get.acme.sh | sh -s email=my@example.com

# html认证
acme.sh  --issue  --force  -d taobao.com -d www.taobao.com --webroot /usr/share/nginx/html/taobao.com

# DNS认证
export Ali_Key="########"
export Ali_Secret="###########"
for i in `cat yuming.txt`;do
/root/.acme.sh/acme.sh --issue --force --dns dns_ali -d ${i} -d www.${i}
if [ $? -eq 0 ];then
\cp /root/.acme.sh/${i}/${i}.key .
\cp /root/.acme.sh/${i}/fullchain.cer ./${i}.crt
echo -e "\033[32m  =================================================================  \033[0m"
echo -e "\033[48;32;5m                       $i        域名更新成功                    \033[0m"
echo -e "\033[32m  =================================================================  \033[0m"
else
echo -e "\033[31m  =================================================================  \033[0m"
echo -e "\033[48;31;5m                       $i        域名更新失败                    \033[0m"
echo -e "\033[31m  =================================================================  \033[0m"
fi
done


