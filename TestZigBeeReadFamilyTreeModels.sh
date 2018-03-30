python MqttProxyUsCmd.py  --u DemoUser1 --p ZigBee09 --gwid 0x1111 --rw r --contract ZigBeeDeviceCompliance --func ReadFamilyTreeModelAndSku --param '[{"Cert":"ZigBee3","Name":"Acme"}]' --timeout 30
python MqttProxyUsCmd.py  --u DemoUser1 --p ZigBee09 --gwid 0x1111 --rw r --contract ZigBeeDeviceCompliance --func ReadFamilyTreeModelAndSku --param '[{"Cert":"NoCert","Name":"Acme"}]' --timeout 30
