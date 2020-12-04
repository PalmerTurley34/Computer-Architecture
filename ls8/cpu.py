"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self, program_file):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = 0
        self.program_file = program_file

    def load(self):
        """Load a program into memory."""

        address = 0
        program = []
        f = open(sys.argv[1])
        line = f.readline()
        while line != '':
            if line[0] in ['0', '1']:
                program.append(int(line[:8], 2))
            line = f.readline() 
        f.close()


        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
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

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001
        PRN = 0b01000111
        LDI = 0b10000010
        MUL = 0b10100010
        IC = self.ram_read(self.pc)
        operand_a = self.ram_read(self.pc+1)
        operand_b = self.ram_read(self.pc+2)
        while IC != HLT:
            if IC == LDI:
                self.registers[operand_a] = operand_b
                self.pc += 3
            elif IC == PRN:
                print(self.registers[operand_a])
                self.pc += 2
            elif IC == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            IC = self.ram[self.pc]
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

    def ram_read(self, MAR):
        return self.ram[MAR]
    
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
