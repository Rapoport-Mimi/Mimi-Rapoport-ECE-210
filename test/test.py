# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    import random
    # Generate a random value for input

    clock = Clock(dut.clk, period = 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut.rst_n.value = 0 
    # 10 clock cycles
    await ClockCycles(dut.clk, 10)
    # Take out of reset
    dut.rst_n.value = 1 

    dut.ui_in.value = 0
    await ClockCycles(dut.clk, 10)

    dut.ui_in.value = 20
    await ClockCycles(dut.clk, 100)

    dut._log.info("Test Complete")




   