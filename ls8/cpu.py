"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        
        # Instructions:
        
        self.HLT            = 1
        self.PRINT_NUM      = 3
        self.SAVE           = 130  # Save a value to a register
        self.PRINT_REGISTER = 71  # Print the value in a register
        self.ADD            = 6 
        self.SUB            = 7
        self.MUL            = 162
        self.DIV            = 9

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 162:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
        
    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        
        # ir = [0] * 8
        math_op = ['ADD', 'SUB', 162, 'DIV']
        commands = []
        with open(sys.argv[1], "r") as f:
            line = f.readlines()
            # print(line)
        for i in line:
            if i[0] == "#":
                continue
            else:
                commands.append(int(i[:8],2))
        f.close()
        self.load(commands)
        # print(self.ram)
        while True:
            command = self.ram[self.pc]
            if command in math_op:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.alu(command, reg_a, reg_b)
                self.pc += 3
            elif command == self.SAVE:
                num = self.ram[self.pc + 2]
                ir = self.ram[self.pc + 1]
                self.reg[ir] = num
                self.pc += 3
            elif command == self.PRINT_REGISTER:
                # Print the value in a register
                ir = self.ram[self.pc + 1]
                print(self.reg[ir])
                self.pc += 2
            elif command == self.HLT:
                sys.exit(0)
            else:
                print(f"I did not understand that command: {command}")
                sys.exit(1)

