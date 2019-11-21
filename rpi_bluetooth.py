import bluetooth

def receiveMessages():

  pixel_data = open("img_data.txt","r").read()
  
  server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  
  port = 1
  server_sock.bind(("",port))
  server_sock.listen(1)
  
  client_sock,address = server_sock.accept()
  print ("Accepted connection from " + str(address))
  
  server_sock2=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  
  server_sock2.connect(("B8:27:EB:88:3F:16",2))
  
  index = 0
  DATA_LENGTH = len(pixel_data)
  while index < DATA_LENGTH - 1:
      b_data = client_sock.recv(1024)
      data = b_data.rstrip()
      print(data)
      #key_pressed = input('Press ENTER to continue: ')
      if data == 'h':
        temp_char = pixel_data[index]
        server_sock2.send("hello")
        if temp_char in ['1']:
          print("High\n")
        else:
          print("Low\n")
        index = index + 1
  print("Done! and waiting for instructions")    
  
  server_sock2.send("done!")
  
  next_instruction = client_sock.recv(1024).rstrip()
  if next_instruction != "AAA":
      open("img_data.txt","w").truncate(0)
      open("img_data.txt","w").write(next_instruction)
  #data = client_sock.recv(1024)
  #print(data)
  
  #str_data = data.rstrip()
  #print(str_data)

  #if str_data == 'hello':
    #print("ok")
  #else:
    #print("not ok")

  #print ("received [%s]" % data)

  #data2 = client_sock.recv(1024)
  
  #print(data2)
  client_sock.close()
  server_sock.close()
  server_sock2.close()
  print("Disconnected from Bluetooth")

  
def sendMessageTo(targetBluetoothMacAddress):
  port = 1
  sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  sock.connect((targetBluetoothMacAddress, port))
  sock.send("hello!!")
  sock.close()
  
def sendDoneMessage(targetBluetoothMacAddress):
  port = 1
  sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  sock.connect((targetBluetoothMacAddress, port))
  sock.send("done!")
  sock.close()
  
def lookUpNearbyBluetoothDevices():
  nearby_devices = bluetooth.discover_devices()
  for bdaddr in nearby_devices:
    print (str(bluetooth.lookup_name( bdaddr )) + " [" + str(bdaddr) + "]")
    
receiveMessages()   
#sendMessageTo("B8:27:EB:88:3F:16") 
