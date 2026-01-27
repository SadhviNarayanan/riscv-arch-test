##################################
# priv/extensions/interruptsSm.py
#
# InterruptsSm privileged extension test generator.
# sanarayanan@hmc.edu Jan 2026
# SPDX-License-Identifier: Apache-2.0
##################################

"""InterruptsSm privileged extension test generator for machine-mode interrupts."""

from testgen.asm.helpers import comment_banner, write_sigupd
from testgen.data.state import TestData
from testgen.priv.registry import add_priv_test_generator


def _generate_trigger_mti_tests(test_data: TestData) -> list[str]:
    """Generate timer interrupt trigger tests."""
    ######################################
    covergroup = "InterruptsSm_cg"
    coverpoint = "cp_trigger_mti"
    ######################################

    lines = [
        comment_banner(
            "cp_trigger_mti",
            "With mstatus.MIE = {0/1}, and mie = all 1s, use MTIMECMP to cause mip.MTIP",
        ),
        "",
        "LI(t0, -1)               # all 1s",
        "CSRRW(t6, mie, t0)       # enable all interrupts",
        "",
        "# mstatus.MIE = 0 should not take interrupt",
    ]

    lines.extend(
        [
            test_data.add_testcase(coverpoint, "mie_0", covergroup),
            "    CSRRCI(t6, mstatus, 8)   # mstatus.MIE = 0",
            "    RVMODEL_SET_MTIMER_INT   # trigger timer interrupt",
            "    # NOTE: interrupt is not taken",
            "    RVMODEL_CLR_MTIMER_INT   # reset mtimecmp",
            write_sigupd(31, test_data),
        ]
    )

    lines.extend(
        [
            "",
            "# mstatus.MIE = 1 should take interrupt",
            test_data.add_testcase(coverpoint, "mie_1", covergroup),
            "    CSRRSI(t6, mstatus, 8)   # mstatus.MIE = 1",
            "    RVMODEL_SET_MTIMER_INT   # expecting timer interrupt",
            write_sigupd(31, test_data),
        ]
    )

    return lines


def _generate_trigger_msi_tests(test_data: TestData) -> list[str]:
    """Generate software interrupt trigger tests."""
    ######################################
    covergroup = "InterruptsSm_cg"
    coverpoint = "cp_trigger_msi"
    ######################################

    lines = [
        comment_banner(
            "cp_trigger_msi",
            "With mstatus.MIE = {0/1}, and mie = all 1s, use CLINT.MSIP to cause mip.MSIP",
        ),
        "",
        "LI(t0, -1)               # all 1s",
        "CSRRW(t6, mie, t0)       # enable all interrupts",
        "",
        "# mstatus.MIE = 0 should not take interrupt",
    ]

    lines.extend(
        [
            test_data.add_testcase(coverpoint, "mie_0", covergroup),
            "    CSRRCI(t6, mstatus, 8)   # mstatus.MIE = 0",
            "    RVMODEL_SET_MSW_INT      # trigger software interrupt",
            "    RVMODEL_CLR_MSW_INT      # reset mip.MSIP",
            write_sigupd(31, test_data),
        ]
    )

    lines.extend(
        [
            "",
            "# mstatus.MIE = 1 should take interrupt",
            test_data.add_testcase(coverpoint, "mie_1", covergroup),
            "    CSRRSI(t6, mstatus, 8)   # mstatus.MIE = 1",
            "    RVMODEL_SET_MSW_INT      # expecting software interrupt",
            write_sigupd(31, test_data),
        ]
    )

    return lines


def _generate_trigger_mei_tests(test_data: TestData) -> list[str]:
    """Generate machine-mode external interrupt trigger tests."""
    ######################################
    covergroup = "InterruptsSm_cg"
    coverpoint = "cp_trigger_mei"
    ######################################

    lines = [
        comment_banner(
            "cp_trigger_mei",
            "With mstatus.MIE = {0/1}, and mie = all 1s, use PLIC to cause mip.MEIP",
        ),
        "",
        "LI(t0, -1)               # all 1s",
        "CSRRW(t6, mie, t0)       # enable all interrupts",
        "",
        "# mstatus.MIE = 0 should not take interrupt",
    ]

    lines.extend(
        [
            test_data.add_testcase(coverpoint, "mie_0", covergroup),
            "    CSRRCI(t6, mstatus, 8)   # mstatus.MIE = 0",
            "    LI(a3, 0x10)",
            "    RVMODEL_SET_MEXT_INT",
            "    RVMODEL_CLR_MEXT_INT",
            write_sigupd(31, test_data),
        ]
    )

    lines.extend(
        [
            "",
            "# mstatus.MIE = 1 should take interrupt",
            test_data.add_testcase(coverpoint, "mie_1", covergroup),
            "    CSRRSI(t6, mstatus, 8)   # mstatus.MIE = 1",
            "    LI(a3, 0x10)",
            "    RVMODEL_SET_MEXT_INT",
            write_sigupd(31, test_data),
        ]
    )

    return lines


def _generate_trigger_sti_tests(test_data: TestData) -> list[str]:
    """Generate supervisor timer interrupt trigger tests."""
    ######################################
    covergroup = "InterruptsSm_cg"
    coverpoint = "cp_trigger_sti"
    ######################################

    lines = [
        comment_banner(
            "cp_trigger_sti",
            "With mstatus.MIE = {0/1}, and mie = all 1s, write mip.STIP",
        ),
        "",
        "LI(t0, -1)               # all 1s",
        "CSRRW(t6, mie, t0)       # enable all interrupts",
        "",
        "# mstatus.MIE = 0 should not take interrupt",
    ]

    lines.extend(
        [
            test_data.add_testcase(coverpoint, "mie_0", covergroup),
            "    CSRRCI(t6, mstatus, 8)   # mstatus.MIE = 0",
            "    LI(t0, 32)               # 1 in bit 5",
            "    CSRRS(t6, mip, t0)       # set mip.STIP",
            "    CSRRC(t6, mip, t0)       # reset mip.STIP",
            write_sigupd(31, test_data),
        ]
    )

    lines.extend(
        [
            "",
            "# mstatus.MIE = 1 should take interrupt",
            test_data.add_testcase(coverpoint, "mie_1", covergroup),
            "    CSRRSI(t6, mstatus, 8)   # mstatus.MIE = 1",
            "    LI(t0, 32)               # 1 in bit 5",
            "    CSRRS(t6, mip, t0)       # set mip.STIP, expect interrupt",
            write_sigupd(31, test_data),
        ]
    )

    return lines


def _generate_trigger_ssi_mip_tests(test_data: TestData) -> list[str]:
    """Generate supervisor software interrupt trigger tests via MIP."""
    ######################################
    covergroup = "InterruptsSm_cg"
    coverpoint = "cp_trigger_ssi_mip"
    ######################################

    lines = [
        comment_banner(
            "cp_trigger_ssi_mip",
            "With mstatus.MIE = {0/1}, and mie = all 1s, write mip.SSIP",
        ),
        "",
        "LI(t0, -1)               # all 1s",
        "CSRRW(t6, mie, t0)       # enable all interrupts",
        "",
        "# mstatus.MIE = 0 should not take interrupt",
    ]

    lines.extend(
        [
            test_data.add_testcase(coverpoint, "mie_0", covergroup),
            "    CSRRCI(t6, mstatus, 8)   # mstatus.MIE = 0",
            "    CSRRSI(t6, mip, 2)       # set mip.SSIP",
            "    CSRRCI(t6, mip, 2)       # reset mip.SSIP",
            write_sigupd(31, test_data),
        ]
    )

    lines.extend(
        [
            "",
            "# mstatus.MIE = 1 should take interrupt",
            test_data.add_testcase(coverpoint, "mie_1", covergroup),
            "    CSRRSI(t6, mstatus, 8)   # mstatus.MIE = 1",
            "    CSRRSI(t6, mip, 2)       # set mip.SSIP, expect interrupt",
            write_sigupd(31, test_data),
        ]
    )

    return lines


def _generate_trigger_sei_plic_tests(test_data: TestData) -> list[str]:
    """Generate supervisor external interrupt trigger tests via PLIC."""
    ######################################
    covergroup = "InterruptsSm_cg"
    coverpoint = "cp_trigger_sei_plic"
    ######################################

    lines = [
        comment_banner(
            "cp_trigger_sei_plic",
            "With mstatus.MIE = {0/1}, and mie = all 1s, use PLIC to cause mip.SEIP",
        ),
        "",
        "LI(t0, -1)               # all 1s",
        "CSRRW(t6, mie, t0)       # enable all interrupts",
        "",
        "# mstatus.MIE = 0 should not take interrupt",
    ]

    lines.extend(
        [
            test_data.add_testcase(coverpoint, "mie_0", covergroup),
            "    CSRRCI(t6, mstatus, 8)   # mstatus.MIE = 0",
            "    LI(a3, 0x10)",
            "    RVMODEL_SET_SEXT_INT",
            "    RVMODEL_CLR_SEXT_INT",
            write_sigupd(31, test_data),
        ]
    )

    lines.extend(
        [
            "",
            "# mstatus.MIE = 1 should take interrupt",
            test_data.add_testcase(coverpoint, "mie_1", covergroup),
            "    CSRRSI(t6, mstatus, 8)   # mstatus.MIE = 1",
            "    LI(a3, 0x10)",
            "    RVMODEL_SET_SEXT_INT",
            write_sigupd(31, test_data),
        ]
    )

    return lines


def _generate_trigger_sei_sie_tests(test_data: TestData) -> list[str]:
    """Generate supervisor external interrupt trigger tests via SIE."""
    ######################################
    covergroup = "InterruptsSm_cg"
    coverpoint = "cp_trigger_sei_sie"
    ######################################

    lines = [
        comment_banner(
            "cp_trigger_sei_sie",
            "With mstatus.MIE = {0/1}, and mie = all 1s, write mip.SEIP",
        ),
        "",
        "LI(t0, -1)               # all 1s",
        "CSRRW(t6, mie, t0)       # enable all interrupts",
        "",
        "# mstatus.MIE = 0 should not take interrupt",
    ]

    lines.extend(
        [
            test_data.add_testcase(coverpoint, "mie_0", covergroup),
            "    CSRRCI(t6, mstatus, 8)   # mstatus.MIE = 0",
            "    LI(t0, 512)              # 1 in bit 9",
            "    CSRRS(t6, mip, t0)       # set mip.SEIP",
            "    CSRRC(t6, mip, t0)       # reset mip.SEIP",
            write_sigupd(31, test_data),
        ]
    )

    lines.extend(
        [
            "",
            "# mstatus.MIE = 1 should take interrupt",
            test_data.add_testcase(coverpoint, "mie_1", covergroup),
            "    CSRRSI(t6, mstatus, 8)   # mstatus.MIE = 1",
            "    LI(t0, 512)              # 1 in bit 9",
            "    CSRRS(t6, mip, t0)       # set mip.SEIP, expect interrupt",
            write_sigupd(31, test_data),
        ]
    )

    return lines


def _generate_interrupt_cross_tests(test_data: TestData) -> list[str]:
    """Generate interrupt cross-product tests (mstatus.MIE x mtvec.MODE x mip x mie)."""
    ######################################
    covergroup = "InterruptsSm_cg"
    coverpoint = "cp_interrupts"
    ######################################

    lines = [
        comment_banner(
            "cp_interrupts",
            "Cross of mstatus.MIE = {0/1}, mtvec.MODE = 00, 3 walking 1s in mip.MTIP/MSIP/MEIP,\n"
            "3 walking 1s in mie.MTIE/MSIE/MEIE (2 x 3 x 3 bins)",
        ),
        "",
        "CSRRCI(t6, mtvec, 3)     # mtvec.MODE = 00",
    ]

    # Unroll the nested loops: mstatus.MIE x mie enables x mip pending
    for mstatus_mie in [0, 1]:
        if mstatus_mie == 0:
            lines.append("CSRRCI(t6, mstatus, 8)   # mstatus.MIE = 0")
        else:
            lines.append("CSRRSI(t6, mstatus, 8)   # mstatus.MIE = 1")

        # 3 interrupt enables: s1 = 2 (MEIE), 1 (MTIE), 0 (MSIE)
        for s1 in [2, 1, 0]:
            # Calculate mie enable bit position: bit (3 + s1*4)
            mie_bit = 3 + s1 * 4
            mie_val = 1 << mie_bit
            enable_name = ["MSIE", "MTIE", "MEIE"][s1]

            lines.extend(
                [
                    f"LI(t4, {mie_val})            # enable {enable_name}",
                    "CSRRW(t6, mie, t4)       # set enable, clear others",
                ]
            )

            # 3 interrupt pending: s2 = 2 (MEIP), 1 (MTIP), 0 (MSIP)
            for s2 in [2, 1, 0]:
                int_name = ["MSIP", "MTIP", "MEIP"][s2]
                binname = f"mie_{mstatus_mie}_{int_name.lower()}_{enable_name.lower()}"

                lines.extend(
                    [
                        test_data.add_testcase(coverpoint, binname, covergroup),
                        "    CSRR(t6, mie)            # save mie (trap clears it)",
                    ]
                )

                if s2 == 2:  # MEIP
                    lines.extend(
                        [
                            "    RVMODEL_SET_MEXT_INT",
                            "    RVMODEL_CLR_MEXT_INT",
                        ]
                    )
                elif s2 == 1:  # MTIP
                    lines.extend(
                        [
                            "    RVMODEL_SET_MTIMER_INT",
                            "    RVMODEL_CLR_MTIMER_INT",
                        ]
                    )
                else:  # MSIP (s2 == 0)
                    lines.extend(
                        [
                            "    RVMODEL_SET_MSW_INT",
                            "    RVMODEL_CLR_MSW_INT",
                        ]
                    )

                lines.extend(
                    [
                        "    CSRW(mie, t6)            # restore mie",
                        write_sigupd(31, test_data),
                    ]
                )

    return lines


def _generate_vectored_tests(test_data: TestData) -> list[str]:
    """Generate vectored interrupt mode tests."""
    ######################################
    covergroup = "InterruptsSm_cg"
    coverpoint = "cp_vectored"
    ######################################

    lines = [
        comment_banner(
            "cp_vectored",
            "Cross of mtvec.MODE = 01, mstatus.MIE=1, all 3 of mie.MTIE/MSIE/MEIE,\n"
            "3 walking 1s in mip.MTIP/MSIP/MEIP (3 bins)",
        ),
        "",
        "CSRRCI(t6, mtvec, 3)",
        "CSRRSI(t6, mtvec, 1)     # mtvec.MODE = 01",
        "CSRRSI(t6, mstatus, 8)   # mstatus.MIE = 1",
        "CSRRW(t6, mie, zero)     # clear all enables",
        "LI(s1, 0x888)            # MEIE/MTIE/MSIE",
        "CSRRS(t6, mie, s1)       # enable all three",
    ]

    # Raise each interrupt type: s2 = 2 (MEIP), 1 (MTIP), 0 (MSIP)
    for s2 in [2, 1, 0]:
        int_name = ["msip", "mtip", "meip"][s2]

        lines.append(test_data.add_testcase(coverpoint, int_name, covergroup))

        if s2 == 2:  # MEIP
            lines.extend(
                [
                    "    CSRR(t6, mie)            # save mie",
                    "    RVMODEL_SET_MEXT_INT",
                    "    RVMODEL_CLR_MEXT_INT",
                    "    CSRW(mie, t6)            # restore mie",
                ]
            )
        elif s2 == 1:  # MTIP
            lines.extend(
                [
                    "    CSRR(t6, mie)            # save mie",
                    "    RVMODEL_SET_MTIMER_INT",
                    "    RVMODEL_CLR_MTIMER_INT",
                    "    CSRW(mie, t6)            # restore mie",
                ]
            )
        else:  # MSIP
            lines.extend(
                [
                    "    CSRR(t6, mie)            # save mie",
                    "    RVMODEL_SET_MSW_INT",
                    "    RVMODEL_CLR_MSW_INT",
                    "    CSRW(mie, t6)            # restore mie",
                ]
            )

        lines.append(write_sigupd(31, test_data))

    return lines


def _generate_priority_tests(test_data: TestData) -> list[str]:
    """Generate interrupt priority tests."""
    ######################################
    covergroup = "InterruptsSm_cg"
    coverpoint = "cp_priority"
    ######################################

    lines = [
        comment_banner(
            "cp_priority",
            "With mstatus.MIE = 1, write cross product of 8 values of mie.{MSIE/MTIE/MEIE}\n"
            "with hardware events giving the 8 values of mip.{MSIP/MTIP/MEIP} (8 x 8 bins)",
        ),
        "",
        "CSRRSI(t6, mstatus, 8)   # mstatus.MIE = 1",
    ]

    # Unroll s1 loop: 7 down to 0 (mie values)
    for s1 in range(7, -1, -1):
        # Build mie value from s1
        lines.extend(
            [
                "CSRRW(t6, mie, zero)     # clear all enables",
                f"LI(t0, {s1 & 4})         # check bit 2",
                "SLLI(t0, t0, 9)          # mie.MEIE position",
                "MV(s3, t0)",
                f"LI(t0, {s1 & 2})         # check bit 1",
                "SLLI(t0, t0, 6)          # mie.MTIE position",
                "OR(s3, s3, t0)",
                f"LI(t0, {s1 & 1})         # check bit 0",
                "SLLI(t0, t0, 3)          # mie.MSIE position",
                "OR(s3, s3, t0)",
            ]
        )

        # Unroll s2 loop: 7 down to 0 (mip values)
        for s2 in range(7, -1, -1):
            binname = f"mie_{s1:03b}_mip_{s2:03b}"

            lines.append(test_data.add_testcase(coverpoint, binname, covergroup))

            # Trigger interrupts based on s2
            if s2 & 4:  # bit 2: MEIP
                lines.append("    RVMODEL_SET_MEXT_INT")
            if s2 & 2:  # bit 1: MTIP
                lines.append("    RVMODEL_SET_MTIMER_INT")
            if s2 & 1:  # bit 0: MSIP
                lines.append("    RVMODEL_SET_MSW_INT")

            lines.extend(
                [
                    "    CSRRS(t6, mie, s3)       # enable interrupts",
                    "    CSRRC(t6, mie, s3)       # disable for next test",
                    "    RVMODEL_CLR_MEXT_INT",
                    "    RVMODEL_CLR_MTIMER_INT",
                    "    RVMODEL_CLR_MSW_INT",
                    write_sigupd(31, test_data),
                ]
            )

    return lines


def _generate_wfi_tests(test_data: TestData) -> list[str]:
    """Generate WFI instruction tests."""
    ######################################
    covergroup = "InterruptsSm_cg"
    coverpoint = "cp_wfi"
    ######################################

    lines = [
        comment_banner(
            "cp_wfi",
            "Cross Product of mstatus.MIE = {0/1}, mstatus.TW = {0/1}, mie.MTIE = 1\n"
            "Set MTIMECMP = TIME + 0x100 to interrupt in the future\n"
            "WFI instruction",
        ),
    ]

    # Unroll s2 loop: 3 down to 0
    for s2 in range(3, -1, -1):
        mie_val = (s2 >> 1) & 1  # bit 1
        tw_val = s2 & 1  # bit 0
        binname = f"mie_{mie_val}_tw_{tw_val}"

        lines.extend(
            [
                test_data.add_testcase(coverpoint, binname, covergroup),
                "    LI(t0, 0x20000A)",
                "    CSRRC(t6, mstatus, t0)   # clear TW, MIE, SIE",
            ]
        )

        # Set MIE if bit 1 is set
        if s2 & 2:
            lines.append("    CSRRSI(t6, mstatus, 8)   # set mstatus.MIE")

        # Set TW if bit 0 is set
        if s2 & 1:
            lines.extend(
                [
                    "    LA(t0, 0x200000)",
                    "    CSRRS(t6, mstatus, t0)   # set mstatus.TW",
                ]
            )

        lines.extend(
            [
                "    LI(t0, 0x80)",
                "    CSRRW(t6, mie, t0)       # set mie.MTIE = 1",
                "    RVMODEL_SET_MTIMER_INT_SOON",
                "    nop",
                "    wfi",
                "    nop",
                write_sigupd(31, test_data),
            ]
        )

    return lines


@add_priv_test_generator("InterruptsSm")
def make_interruptssm(test_data: TestData) -> list[str]:
    """Generate tests for InterruptsSm machine-mode interrupts."""
    lines: list[str] = [
        "",
        "LA(sp, scratch)",
        "RVMODEL_CLR_MTIMER_INT",
        "",
    ]

    lines.extend(_generate_trigger_mti_tests(test_data))
    lines.extend(_generate_trigger_msi_tests(test_data))
    lines.extend(_generate_trigger_mei_tests(test_data))

    lines.extend(_generate_trigger_sti_tests(test_data))
    lines.extend(_generate_trigger_ssi_mip_tests(test_data))
    lines.extend(_generate_trigger_sei_plic_tests(test_data))
    lines.extend(_generate_trigger_sei_sie_tests(test_data))

    lines.extend(_generate_interrupt_cross_tests(test_data))
    lines.extend(_generate_vectored_tests(test_data))
    lines.extend(_generate_priority_tests(test_data))
    lines.extend(_generate_wfi_tests(test_data))

    return lines
