.relativeinclude on
.nds
.arm


.definelabel MaxSize, 0x810
.include "lib/stdlib_us.asm"
.definelabel ProcStartAddress, 0x022E7248
.definelabel ProcJumpAddress, 0x022E7AC0
.definelabel ChangeGlobalBorderColor, 0x02027A80


; File creation
.create "./code_out.bin", 0x022E7248
	.org ProcStartAddress
	.area MaxSize
		mov r0,r7
		bl ChangeGlobalBorderColor
		
		b ProcJumpAddress
		.pool
	.endarea
.close
