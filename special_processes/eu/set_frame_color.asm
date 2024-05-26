.relativeinclude on
.nds
.arm


.definelabel MaxSize, 0x810
.include "lib/stdlib_eu.asm"
.definelabel ProcStartAddress, 0x022E7B88
.definelabel ProcJumpAddress, 0x022E8400
.definelabel ChangeGlobalBorderColor, 0x02027D74


; File creation
.create "./code_out.bin", 0x022E7B88
	.org ProcStartAddress
	.area MaxSize
		mov r0,r7
		bl ChangeGlobalBorderColor
		
		b ProcJumpAddress
		.pool
	.endarea
.close
