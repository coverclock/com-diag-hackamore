Copyright 2014 Digital Aggregates Corporation, Colorado, USA.

----------------------------------------------------------------------

LICENSE

This application and its framework are free software; you can redistribute it
and/or modify it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation; either version 2.1 of the License,
or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA  02111-1307  USA

Alternative commercial licensing terms may be available from the copyright
holder. Contact the copyright holder for more information.

----------------------------------------------------------------------

ABSTRACT

This is the Digital Aggregates Corporation Hackamore package. Hackamore is a
framework and application written in Python that maintains a dynamic model of
the call states of one or more Asterisk PBXes using the Asterisk Management
Interface (AMI). It was inspired by prior work done in C by Mark Jackson at
Aircell Business Aviation Services LLC. Hackamore is a work in progress.
This software is an original work of its author.

If you want to run any of the main programs that execute against a live Asterisk
server, those programs need to know your server(s) hostname or IP address,
AMI port (if not 5038), and the username and secret that you administered in
your

    /etc/asterisk/manager.conf

file(s). You can either define these as the following environmental variables
    
    COM_DIAG_HACKAMORE_NAMEn=server_symbolic_name
    COM_DIAG_HACKAMORE_SERVERn=server_ipaddress_or_hostname
    COM_DIAG_HACKAMORE_PORTn=server_ami_port_number_if_not_5038
    COM_DIAG_HACKAMORE_USERNAMEn=ami_username
    COM_DIAG_HACKAMORE_SECRETn=ami_password

(where "n" begins at "1" and increments for each additional Asterisk server).
Or you can define them with the same names in a dotfile in your home directory
called

    .com_diag_hackamore

from the main programs below will extract them. For example, the dotfile could
contains lines

    COM_DIAG_HACKAMORE_NAME1=PBX1
    COM_DIAG_HACKAMORE_SERVER1=192.168.1.225
    COM_DIAG_HACKAMORE_PORT1=5038
    COM_DIAG_HACKAMORE_USERNAME1=admin
    COM_DIAG_HACKAMORE_SECRET1=password
    COM_DIAG_HACKAMORE_NAME2=PBX2
    COM_DIAG_HACKAMORE_SERVER2=192.168.1.226
    COM_DIAG_HACKAMORE_PORT2=5038
    COM_DIAG_HACKAMORE_USERNAME2=admin
    COM_DIAG_HACKAMORE_SECRET2=password

to process AMI messages from two different Asterisk PBXes. The two main programs
can be run using the command lines

    python src/com/diag/hackamore/Main.py
    
or

    python src/com/diag/hackamore/Mains.py

in which Main is single threaded, multiplexes the AMI sockets using the
select(2) system call, and updates a common model, and Mains is multi-threaded,
processes each AMI socket from a different thread, and updates a common model
by serializing access to it. Either should work, but the latter can leverage
multi-core servers to keep up with higher transaction rates.

----------------------------------------------------------------------

CONTACT

Chip Overclock
mailto:coverclock@diag.com
Digital Aggregates Corporation
3440 Youngfield Street, Suite 209
Wheat Ridge CO 80033 USA
http://www.diag.com
