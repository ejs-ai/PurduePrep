from PurduePrep.main import main
import time

if __name__ == '__main__':
    test_input = """AES is a block cipher with a block length of 128 bits.
 AES allows for three different key lengths: 128, 192, or 256 bits.
Most of our discussion will assume that the key length is 128
bits. [With regard to using a key length other than 128 bits,
the main thing that changes in AES is how you generate the
key schedule from the key — an issue I address at the end of
Section 8.8.1. The notion of key schedule in AES is explained
in Sections 8.2 and 8.8.]
 Encryption consists of 10 rounds of processing for 128-bit keys,
12 rounds for 192-bit keys, and 14 rounds for 256-bit keys.
 Except for the last round in each case, all other rounds are
identical.
 Each round of processing includes one single-byte based
substitution step, a row-wise permutation step, a column-wise
mixing step, and the addition of the round key. The order in
which these four steps are executed is different for encryption
and decryption.
3
Computer and Network Security by Avi Kak Lecture 8
 To appreciate the use of “row” and “column” in the previous
bullet, you need to think of the input 128-bit block as consisting
of a 4 × 4 array of bytes, arranged as follows:










byte0 byte4 byte8 byte12
byte1 byte5 byte9 byte13
byte2 byte6 byte10 byte14
byte3 byte7 byte11 byte15










 Notice that the first four bytes of a 128-bit input block
occupy the first column in the 4 × 4 array of bytes. The next
four bytes occupy the second column, and so on.
 The 4 × 4 array of bytes shown above is referred to as the state
array in AES. If you are trying to create your own
implementation of AES in Python, you will find following
statement, which uses the notion of list comprehension in
Python, very useful for creating an initialized structure that
looks like the state array of AES:
statearray = [[0 for x in range(4)] for x in range(4)]
Next, try the following calls in relation to the structure thus
created:
import sys
statearray = [[0 for x in range(4)] for x in range(4)]
print(statearray)
4
Computer and Network Security by Avi Kak Lecture 8
print(statearray[0])
print(statearray[2][3])
block = list(range(128))
print("\n\nblock: ", block)
for i in range(4):
for j in range(4):
statearray[j][i] = block[32*i + 8*j:32*i + 8*(j+1)]
for i in range(4):
sys.stdout.write("\n\n")
for j in range(4):
sys.stdout.write( str(statearray[i][j]) )
sys.stdout.write("\t")
sys.stdout.write("\n\n")
This is a nice warm-up exercise before you start implementing
AES in Python.
 AES also has the notion of a word. A word consists of four
bytes, that is 32 bits. Therefore, each column of the state array
is a word, as is each row.
 Each round of processing works on the input state array and
produces an output state array.
 The output state array produced by the last round is rearranged
into a 128-bit output block.
 Unlike DES, the decryption algorithm differs substantially from
the encryption algorithm. Although, overall, very similar steps
5
Computer and Network Security by Avi Kak Lecture 8
are used in encryption and decryption, their implementations
are not identical and the order in which the steps are invoked is
different, as mentioned previously.
 AES, notified by NIST as a standard in 2001, is a slight
variation of the Rijndael cipher invented by two Belgian
cryptographers Joan Daemen and Vincent Rijmen. [Back in 1999, the
Rijndael cipher was one of the five chosen by NIST as a potential replacement for DES. The other four were:
MARS from IBM; RC6 from RSA Security; Serpent by Ross Anderson, Eli Biham, and Lars Knudsen; and
Twofish by a team led by the always-in-the-news cryptographer Bruce Schneier. Rijndael was selected from
these five after extensive testing that was open to public.]
 Whereas AES requires the block size to be 128 bits, the original
Rijndael cipher works with any block size (and any key size)
that is a multiple of 32 as long as it exceeds 128. The state
array for the different block sizes still has only four rows in the
Rijndael cipher. However, the number of columns depends on
size of the block. For example, when the block size is 192, the
Rijndael cipher requires a state array to consist of 4 rows and 6
columns.
 As explained in Lecture 3, DES was based on the Feistel
network. On the other hand, what AES uses is a
substitution-permutation network in a more general
sense. Each round of processing in AES involves byte-level
substitutions followed by word-level permutations. Speaking
6
Computer and Network Security by Avi Kak Lecture 8
generally, DES also involves substitutions and permutations,
except that the permutations are based on the Feistel notion of
dividing the input block into two halves, processing each half
separately, and then swapping the two halves.
"""
# This test input makes the scrape only look at one site. Why?
    test_input2 = """
Primitive joints can be arranged in parallel as well as in series. Figure 3.2.1 illustrates
such a parallel link mechanism. It is a five-bar-linkage consisting of five links, including the base
link, connected by five joints. This can be viewed as two serial linkage arms connected at a
particular point, point A in the figure. It is important to note that there is a closed kinematic chain
formed by the five links and, thereby, the two serial link arms must conform to a certain
geometric constraint. It is clear from the figure that the end-effecter position is determined if two
of the five joint angles are given. For example, if angles 1? and 3? of joints 1 and 3 are
determined, then all the link positions are determined, as is the end-effecter’s. Driving joints 1
Figure 3.1.7 Gravity-balanced robot with three-revolute joints
Photo removed for copyright reasons.
Figure 3.2.3 Stewart mechanism parallel-link robot
Figure by MIT OCW.
Department of Mechanical Engineering Massachusetts Institute of Technology
Figure 3.2.3 shows the Stewart mechanism, which consists of a moving platform, a fixed
base, and six powered cylinders connecting the moving platform to the base frame. The position
and orientation of the moving platform are determined by the six independent actuators. The load
acting on the moving platform is born by the six "arms". Therefore, the load capacity is generally
large, and dynamic response is fast for this type of robot mechanisms. Note, however, that this
 mechanism has spherical joints, a different type of joints than the primitive joints we considered
 initially.
Figure 3.2.2 Heavy-duty robot with parallel link mechanism
Diagram removed for copyright reasons.
 This type of parallel linkage, having a closed-loop kinematic chain, has significant
features. First, placing both actuators at the base link makes the robot arm lighter, compared to
the serial link arm with the second motor fixed to the tip of link 1. Second, a larger end-effecter
load can be born with the two serial linkage arms sharing the load. Figure 3.2.2 shows a heavyduty robot having a parallel link mechanism
"""
test_input3 = """Eigenvectors for square matrices are defined as non-zero vector values which when multiplied by the square matrices give the scaler multiple of the vector, i.e. we define an eigenvector for matrix A to be “v” if it specifies the condition, Av = λv
The scaler multiple λ in the above case is called the eigenvalue of the square matrix. We always have to find the eigenvalues of the square matrix first before finding the eigenvectors of the matrix."""

start_time = time.time()
questions = main(test_input, 5)
print(len(questions))
end_time = time.time()
for q, url in questions:
    print(q + '\n\nEND QUESTION\n\n')

print(f'Total backend time: {end_time-start_time} seconds')