.relativeinclude on
.nds
.arm

.definelabel MaxSize, 0x810
.definelabel ProcStartAddress, 0x022E7B88
.definelabel ProcJumpAddress, 0x022E8400
.definelabel DEFAULT_HERO_ADDR, 0x20B0818
.definelabel DEFAULT_PARTNER_ADDR, 0x20B081A

.create "./code_out.bin", 0x022E7B88
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
