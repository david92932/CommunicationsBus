set server [socket 127.0.0.1 65432]         ;# Open the connection
fconfigure $server -buffering line


puts $server createCamera                         ;# Send a string
after 250


puts $server insertCapture
after 250


puts $server insertMode
after 250

puts $server field0,1,0,45,1,0,45,9,9,1009,4000009
after 250

puts $server save
after 250

puts $server exit
after 250

