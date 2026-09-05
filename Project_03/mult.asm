// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

//initialize i=0
@i
M=0

//initialize R2=0
@R2
M=0

//compare R0 and R1. JMP if R1 less then or equal to R0
@R0
D=M
@R1
D=M-D
@LOOP
D;JLE

//switch values of R0 and R1
@R1
D=M
@temp
M=D
@R0
D=M
@R1
M=D
@temp
D=M
@R0
M=D

(LOOP)
    //loop until i==R1
    @i
    D=M
    @R1
    D=D-M
    @END
    D;JEQ

    //adds R0 to R2, R2 acting as a sum
    @R0
    D=M
    @R2
    M=D+M

    //i++
    @i
    M=M+1

    @LOOP
    0;JMP


(END)
    @END
    0;JMP