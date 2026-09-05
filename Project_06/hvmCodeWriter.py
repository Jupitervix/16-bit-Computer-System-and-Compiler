"""
hvmCodeWriter.py -- Code Writer class for Hack VM translator
"""

import os
from hvmCommands import *

debug = False

class CodeWriter(object):
    
    def __init__(self, outputName):
        """
        Open 'outputName' and gets ready to write it.
        """
        self.file = open(outputName, 'w')
        self.SetFileName(outputName)

        self.labelNumber = 0
        self.returnLabel = None
        self.callLabel = None
        self.cmpLabels = {}
        self.needHalt = True


    def Debug(self, value):
        """
        Set debug mode.
        Debug mode writes useful comments in the output stream.
        """
        global debug
        debug = value


    def Close(self):
        """
        Write a jmp $ and close the output file.
        """
        if self.needHalt:
            if debug:
                self.file.write('    // <halt>\n')
            label = self._UniqueLabel()
            self._WriteCode('@%s, (%s), 0;JMP' % (label, label))
        self.file.close()


    def SetFileName(self, fileName):
        """
        Sets the current file name to 'fileName'.
        Restarts the local label counter.

        Strips the path and extension.  The resulting name must be a
        legal Hack Assembler identifier.
        """
        if (debug):
            self.file.write('    // File: %s\n' % (fileName))
        self.fileName = os.path.basename(fileName)
        self.fileName = os.path.splitext(self.fileName)[0]
        self.functionName = None


    def Write(self, line):
        """
        Raw write for debug comments.
        """
        self.file.write(line + '\n')

    def _UniqueLabel(self):
        """
        Make a globally unique label.
        The label will be _sn where sn is an incrementing number.
        """
        self.labelNumber += 1
        return '_' + str(self.labelNumber)


    def _LocalLabel(self, name):
        """
        Make a function/module unique name for the label.
        If no function has been entered, the name will be
        FileName$$name. Otherwise it will be FunctionName$name.
        """
        if self.functionName != None:
            return self.functionName + '$' + name
        else:
            return self.fileName + '$$' + name


    def _StaticLabel(self, index):
        """
        Make a name for static variable 'index'.
        The name will be FileName.index
        """
        return self.fileName + '.' + str(index)    


    def _WriteCode(self, code):
        """
        Write the comma separated commands in 'code'.
        """
        code = code.replace(',', '\n').replace(' ', '')
        self.file.write(code + '\n')
   

    def WritePushPop(self, commandType, segment, index):
        """
        Write Hack code for 'commandType' (C_PUSH or C_POP).
        'segment' (string) is the segment name.
        'index' (int) is the offset in the segment.
	To be implemented as part of Project 6
	
	    For push: Pushes the content of segment[index] onto the stack. It is a good idea to move the value to be pushed into a register first, then push the content of the register to the stack.
        For pop: Pops the top of the stack into segment[index]. You may need to use a general purpose register (R13-R15) to store some temporary results.
        Hint: Recall that there are 8 memory segments in the VM model, but only 5 of these exist in the assembly definition. Also, not all 8 VM segments allow to perform both pop and push on them. Chapter 7.3 of the book explains memory segment mapping.
        Hint: Use pen and paper first. Figure out how to compute the address of segment[index] (except for constant). Then figure out how you move the value of segment[index] into a register (by preference D). Then figure out how to push a value from a register onto the stack. 
        Hint: For pop, you already know how to compute the address of segment[index]. Store it in a temporary register (you can use R13 to R15 freely). Then read the value from the top of the stack, adjust the top of the stack, and then store the value at the location stored in the temporary register.
    
    PUSH constant is implemented as an example. Other solutions are possible too.

        """
        if (debug):
            debugCodePush = "//PUSH,"
            debugCodePop = "//POP,"
        else:
            debugCodePush = ""
            debugCodePop = ""
                  
        #stores specific code for push or pop depending on commandType
        asmPush = debugCodePush + 'A=D,D=M,@SP,A=M,M=D,@SP,M=M+1'
        asmPop = debugCodePop + '@R13,M=D,@SP,M=M-1,A=M,D=M,@R13,A=M,M=D'
       
        if commandType == C_PUSH: #We add something to the stack
            if segment == 'constant':
                code = debugCodePush
                code += "@" + index + "," 
                code += "D=A,"
                code += "@SP,"
                code += "A=M,"
                code += "M=D,"
                code += "@SP,"
                code += "M=M+1,"
                self._WriteCode(code)
                
        #general code for all commandTypes and each segment      
        if segment == 'local':
            code = "@LCL,"
            code += "D=M,"
            code += "@" + index + ","
            code += "D=D+A,"
            #code += self._PushPopHelperFunction
            if commandType == C_PUSH:
                code += asmPush
            else:
                code += asmPop
            self._WriteCode(code)
        elif segment == 'argument':
            code = "@ARG,D=M,@" + index + ",D=D+A,"
            if commandType == C_PUSH:
                code += asmPush
            else:
                code += asmPop
            self._WriteCode(code)
        elif segment == 'this':
            code = "@THIS,D=M,@" + index + ",D=D+A,"
            if commandType == C_PUSH:
                code += asmPush
            else:
                code += asmPop
            self._WriteCode(code)
        elif segment == 'that':
            code = "@THAT,D=M,@" + index + ",D=D+A,"
            if commandType == C_PUSH:
                code += asmPush
            else:
                code += asmPop
            self._WriteCode(code)
        elif segment == 'static':
            code = "@" + self._StaticLabel(index) + ",D=A,"
            if commandType == C_PUSH:
                code += asmPush
            else:
                code += asmPop
            self._WriteCode(code)
        elif segment == 'temp':
            code = "@5,D=A,@" + index + ",D=D+A,"
            if commandType == C_PUSH:
                code += asmPush
            else:
                code += asmPop
            self._WriteCode(code)
        elif segment == 'pointer':
            if index == '0':
                code = "@THIS,D=A,"
                if commandType == C_PUSH:
                    code += asmPush
                else:
                    code += asmPop
            elif index == '1':
                code = "@THAT,D=A,"
                if commandType == C_PUSH:
                    code += asmPush
                else:
                    code += asmPop
                    
            self._WriteCode(code)
        
        
    def WriteArithmetic(self, command):
        """
        Write Hack code for stack arithmetic 'command' (str).
    To be implemented as part of Project 6
        
        Compiles the arithmetic VM command into the corresponding ASM code. Recall that the operands (one or two, depending on the command) are on the stack and the result of the operation should be placed on the stack.
        The unary and the logical and arithmetic binary operators are simple to compile. 
         The three comparison operators (EQ, LT and GT) do not exist in the assembly language. The corresponding assembly commands are the conditional jumps JEQ, JLT and JGT. You need to implement the VM operations using these conditional jumps. 
         You need two labels, one for the true condition and one for the false condition and you have to put the correct result on the stack.
        """
        if (debug):
            commandForDebug = "//" + command
        else:
            commandForDebug = ""

        #creates unique labels for all of the labels used
        trueEq = self._UniqueLabel()
        continueEq = self._UniqueLabel()
        trueLt = self._UniqueLabel()
        continueLt = self._UniqueLabel()
        trueGt = self._UniqueLabel()
        continueGt = self._UniqueLabel()
        
        #stores specific binary arithmetic expression depending on command
        if command in ['add', 'sub', 'eq', 'lt', 'gt', 'and', 'or'] :
            if command == 'add':
                placeholderBinary = "D=D+M,"
            elif command == 'sub':
                placeholderBinary = "D=D-M,"
            elif command == 'eq':
                placeholderBinary = "D=D-M,@" + trueEq + ",D;JEQ,D=0,@" + continueEq + ",0;JMP,(" + trueEq + "),D=-1,(" + continueEq + "),"
            elif command == 'lt':
                placeholderBinary = "D=D-M,@" + trueLt + ",D;JLT,D=0,@" + continueLt + ",0;JMP,(" + trueLt + "),D=-1,(" + continueLt + "),"     
            elif command == 'gt':
                placeholderBinary = "D=D-M,@" + trueGt + ",D;JGT,D=0,@" + continueGt + ",0;JMP,(" + trueGt + "),D=-1,(" + continueGt + "),"  
            elif command == 'and':
                placeholderBinary = "D=D&M,"
            elif command == 'or':
                placeholderBinary = "D=D|M,"
                
            #general code for all the binary commands
            code = f"""{commandForDebug}
            @SP
            A=M-1
            D=M
            @R13
            M=D
            @2
            D=A
            @SP
            AM=M-D
            D=M
            @R13       
            {placeholderBinary}
            @SP
            A=M
            M=D
            @SP
            M=M+1""".strip()

        #stores specific unary arithmetic expression depending on command
        elif command in ['not', 'neg']:
            if command == 'not':
                placeholderUnary = "M=!M,"
            elif command == 'neg':
                placeholderUnary = "M=-M,"
            
            #general code for all the unary commands
            code  = f"""{commandForDebug}
            @SP
            A=M-1
            {placeholderUnary}""".strip()
        
        self._WriteCode(code)
        
        
    def WriteInit(self, sysinit = True):
        """
        Write the VM initialization code:
    To be implemented as part of Project 7
        """
        if (debug):
            self.file.write('    // Initialization code\n')
        if sysinit == True:
            #sets SP = 256
            code = "@256,"
            code += "D=A,"
            code += "@SP,"
            code += "M=D,"
            self._WriteCode(code)
            
            #calls on Sys.init
            self.WriteCall("Sys.init", 0)
            
            
    def WriteLabel(self, label):
        """
        Write Hack code for 'label' VM command.
	To be implemented as part of Project 7

        """
        #creates label called after the variable 'label'
        code = "(" + self._LocalLabel(label) + "),"
        self._WriteCode(code)
        
        
    def WriteGoto(self, label):
        """
        Write Hack code for 'goto' VM command.
	To be implemented as part of Project 7
        """
        #goes to 'label'
        code = "@" + self._LocalLabel(label) + ",0;JMP,"
        self._WriteCode(code)
        
        
    def WriteIf(self, label):
        """
        Write Hack code for 'if-goto' VM command.
	To be implemented as part of Project 7
        """
        #goes to 'label' if value in stack != 0
        code = "@SP,"
        code += "AM=M-1,"
        code += "D=M,"
        code += "@" + self._LocalLabel(label) + ","
        code += "D;JNE,"
        self._WriteCode(code)


    def WriteFunction(self, functionName, numLocals):
        """
        Write Hack code for 'function' VM command.
	To be implemented as part of Project 7
        """
       #declares label for functionName
        code = "(" + functionName + "),"
 
        #allocates numLocals amount of variables to stack
        for i in range(int(numLocals)):
            code += "@SP,"
            code += "A=M,"
            code += "M=0,"
            code += "@SP,"
            code += "M=M+1,"
        self._WriteCode(code)


    def WriteReturn(self):
        """
        Write Hack code for 'return' VM command.
	To be implemented as part of Project 7
        """
        if (debug):
            code = "//RETURN,"
        else:
            code = ""
            
        #sets endFrame = LCL
        code += "@LCL,"
        code += "D=M,"
        code += "@endFrame,"
        code += "M=D,"
        
        #gets returnAddress and saves in retAddr
        code += "@5,"
        code += "D=A,"
        code += "@endFrame,"
        code += "A=M-D,"
        code += "D=M,"
        code += "@retAddr,"
        code += "M=D,"
        
        #pop ARG 
        code += "@SP,"
        code += "AM=M-1,"
        code += "D=M,"
        code += "@ARG,"
        code += "A=M,"
        code += "M=D,"
        
        #sets SP = ARG + 1
        code += "@ARG,"
        code += "D=M,"
        code += "@SP,"
        code += "M=D+1,"
        
        #restores THAT, THIS, ARG, LCL
        toRestore = ["THAT", "THIS", "ARG", "LCL"]
        for i in range(len(toRestore)):
            restoreNow = toRestore[i]
            code += "@" + str(i) + ","
            code += "D=A+1,"
            code += "@endFrame,"
            code += "A=M-D,"
            code += "D=M,"
            code += "@" + restoreNow + ","
            code += "M=D,"
            
        #goes to returnAddress through saved value in retAddr
        code += "@retAddr,"
        code += "A=M,"
        code += "0;JMP,"
        
        self._WriteCode(code)
        
        
    def WriteCall(self, functionName, numArgs):
        """
        Write Hack code for 'call' VM command.
	To be implemented as part of Project 7
        """
        if (debug):
            code = "//CALL,"
        else:
            code = ""
            
        #generate labelname for returnAddress
        returnAddress = self._UniqueLabel()
        
        #push returnAddress
        code += "@" + returnAddress + ","
        code += "D=A,"
        code += "@SP,"
        code += "A=M,"
        code += "M=D,"
        code += "@SP,"
        code += "M=M+1,"
        
        #push LCL, ARG, THIS, THAT
        toSave = ["LCL", "ARG", "THIS", "THAT"]
        for i in toSave:
            code += "@" + i + ","
            code += "D=M,"
            code += "@SP,"
            code += "A=M,"
            code += "M=D,"
            code += "@SP,"
            code += "M=M+1,"
        
        #sets ARG = SP-5-numArgs
        code += "@" + str(numArgs)  + ","
        code += "D=A,"
        code += "@5,"
        code += "D=D+A,"
        code += "@SP,"
        code += "D=M-D,"
        code += "@ARG,"
        code += "M=D,"
        
        #sets LCL = SP
        code += "@SP,"
        code += "D=M,"
        code += "@LCL,"
        code += "M=D,"
        
        #goto functionName
        code += "@" + functionName + ","
        code += "0;JMP,"
        
        #declare returnAddress as label
        code += "(" + returnAddress+ "),"
        
        self._WriteCode(code)    
    
