import bluetooth

def receiveMessages():

  
  server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  
  port = 2
  server_sock.bind(("",port))
  server_sock.listen(2)
  
  client_sock,address = server_sock.accept()
  print ("Accepted connection from " + str(address))
  
  lock = 1
  while(lock == 1):
    b_data = client_sock.recv(1024).rstrip()
    print(b_data)
    if(b_data == "done!"):
      lock = 0
  
  client_sock.close()
  server_sock.close()
  print("Disconnected from Bluetooth")
  
receiveMessages()
