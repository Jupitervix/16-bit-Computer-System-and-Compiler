// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(START)
//initialize i=0
@i
M=0

//initialize j=0
@j
M=0

//check if KBD input or not, jump to corresponding action
@KBD
D=M
@LOOP_BLACK
D;JNE
@LOOP_WHITE
D;JEQ


    (LOOP_BLACK)
        //loop until i==KBD-SCREEN
        @i
        D=M
        @8192
        D=D-A
        @START
        D;JEQ
        
        //color the i:th next block of pixels black
        @SCREEN
        D=A
        @i
        A=D+M
        M=-1

        //i++
        @i
        M=M+1

        @LOOP_BLACK
        0;JMP


    (LOOP_WHITE)
        //loop until j==KBD-SCREEN
        @j
        D=M
        @8192
        D=D-A
        @START
        D;JEQ
        
        //color the j:th next block of pixels white
        @SCREEN
        D=A
        @j
        A=D+M
        M=0

        //j++
        @j
        M=M+1

        @LOOP_WHITE
        0;JMP

    @START
    0;JMP