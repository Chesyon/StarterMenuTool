.relativeinclude on
.nds
.arm

.definelabel MaxSize, 0x810
.definelabel ProcStartAddress, 0x022E7248
.definelabel ProcJumpAddress, 0x022E7AC0
.definelabel DEFAULT_HERO_ADDR, 0x20AFEFC
.definelabel DEFAULT_PARTNER_ADDR, 0x20AFEFE

.create "./code_out.bin", 0x022E7248
	.org ProcStartAddress
	.area MaxSize
		cmp    r7,#0
        ldreq  r1,=DEFAULT_HERO_ADDR
        ldrne  r1,=DEFAULT_PARTNER_ADDR
        strh   r6,[r1,#0x0]
        mov    r0,r6
        
		b ProcJumpAddress
		.pool
	.endarea
.close
