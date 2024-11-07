from PurduePrep.main import main

if __name__ == '__main__':
    test_input = """The IRC network of Figure 2, whose symbolic name (lets
assume) is MyIRCNet, consists of six servers, A, B, C, D, E, and
F, that are connected as shown. [It is important to realize that, in general, all
of these servers will be plugged into the internet and therefore, for the exchange of TCP/IP traffic,
each server can send TCP/IP packets to all other servers. The connectivity that is shown in Figure 2
is only for the exchange of IRC traffic. We can therefore think of the network shown in Figure 2 as
an overlay network.] An IRC overlay is not allowed to have loops.
This is to ensure that, from the standpoint of any server node in
the network, the rest of the network looks like a tree. This
allows each server node to act as a central node vis-a-vis the
rest of the IRC network. With regard to the participating hosts,
an IRC overlay can be thought of as a spanning tree over the
underlying TCP/IP network. The fact that there are no loops
in an IRC overlay means that there is always a unique path
from any one server to any other server. [No loops in the IRC overlay
makes it easier to update all the servers in real time with regard to the latest information regarding
the servers and the users. Basically, it is the responsibility of each server to forward all the received
state information to the servers it is connected to (except the server from which the information was
received) in the overlay network. If the overlay were to contain loops, such a simple algorithm would
not suffice for keeping the entire network synchronized.]
"""
    questions = main(test_input)
    print(len(questions))
    for q, url in questions:
        print(q + '\n\n')
