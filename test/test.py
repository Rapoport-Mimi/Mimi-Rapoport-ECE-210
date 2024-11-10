# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

# import cocotb
# from cocotb.clock import Clock
# from cocotb.triggers import ClockCycles


# @cocotb.test()
# async def test_project(dut):
#     dut._log.info("Start")

#     import random
#     # Generate a random value for input

#     clock = Clock(dut.clk, period = 10, units="ns")
#     cocotb.start_soon(clock.start())

#     # Reset
#     dut.rst_n.value = 0 
#     # 10 clock cycles
#     await ClockCycles(dut.clk, 10)
#     # Take out of reset
#     dut.rst_n.value = 1 

#     dut.ui_in.value = 0
#     await ClockCycles(dut.clk, 10)

#     dut.ui_in.value = 20
#     await ClockCycles(dut.clk, 100)

#     dut._log.info("Test Complete")

# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

@cocotb.test()
async def test_perceptron(dut):
    dut._log.info("Starting perceptron test")

    # Print all available signals in the DUT for debugging purposes
    dut._log.info(f"Available signals: {dut._sigmap.keys()}")

    # Create a clock with a period of 10ns (100 MHz)
    clock = Clock(dut.clk, period=10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset the DUT (active low reset)
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)  # Wait for 10 clock cycles to let the reset propagate
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)   # Wait for a few cycles to ensure the DUT is settled

    # Test Case 1: Check initial reset values
    # After reset, out should be 0, and weights should be at their initialized values
    assert dut.out.value == 0, f"Expected output to be 0, but got {dut.out.value}"
    assert dut.we1.value == 10, f"Expected we1 to be 10, but got {dut.we1.value}"
    assert dut.we2.value == 20, f"Expected we2 to be 20, but got {dut.we2.value}"
    assert dut.we3.value == 30, f"Expected we3 to be 30, but got {dut.we3.value}"

    # Test Case 2: Test input and output when desired_out = 0
    if "in1" in dut._sigmap:
        dut.in1.value = 1
    else:
        dut._log.warning("Signal 'in1' not found in DUT.")
    if "in2" in dut._sigmap:
        dut.in2.value = 1
    else:
        dut._log.warning("Signal 'in2' not found in DUT.")
    if "in3" in dut._sigmap:
        dut.in3.value = 1
    else:
        dut._log.warning("Signal 'in3' not found in DUT.")
    
    dut.desired_out.value = 0
    await ClockCycles(dut.clk, 10)

    # Check output and weights after some clock cycles
    # Based on the initial weights and threshold, the output should be 0
    assert dut.out.value == 0, f"Expected output to be 0, but got {dut.out.value}"

    # Test Case 3: Test input and output when desired_out = 1
    if "in1" in dut._sigmap:
        dut.in1.value = 5
    if "in2" in dut._sigmap:
        dut.in2.value = 5
    if "in3" in dut._sigmap:
        dut.in3.value = 5
    dut.desired_out.value = 1
    await ClockCycles(dut.clk, 10)

    # Check if the perceptron updates its output
    assert dut.out.value == 1, f"Expected output to be 1, but got {dut.out.value}"

    # Wait a few more cycles and check if weights update (by checking `we1`, `we2`, and `we3`)
    await ClockCycles(dut.clk, 50)
    assert dut.we1.value != 10, f"Expected we1 to change, but got {dut.we1.value}"
    assert dut.we2.value != 20, f"Expected we2 to change, but got {dut.we2.value}"
    assert dut.we3.value != 30, f"Expected we3 to change, but got {dut.we3.value}"

    # Test Case 4: Input where the sum doesn't meet the threshold and desired_out is 0
    if "in1" in dut._sigmap:
        dut.in1.value = 8
    if "in2" in dut._sigmap:
        dut.in2.value = 8
    if "in3" in dut._sigmap:
        dut.in3.value = 8
    dut.desired_out.value = 0
    await ClockCycles(dut.clk, 10)

    # Ensure output is 0 since the weighted sum should be above the threshold
    assert dut.out.value == 0, f"Expected output to be 0, but got {dut.out.value}"

    # Test Case 5: Boundary test with zero inputs, expected output = 0
    if "in1" in dut._sigmap:
        dut.in1.value = 0
    if "in2" in dut._sigmap:
        dut.in2.value = 0
    if "in3" in dut._sigmap:
        dut.in3.value = 0
    dut.desired_out.value = 0
    await ClockCycles(dut.clk, 10)

    # The output should be 0 since all inputs are 0 and the weighted sum is below the threshold
    assert dut.out.value == 0, f"Expected output to be 0, but got {dut.out.value}"

    # Test Case 6: Random test for updating weights (desired output mismatches actual output)
    if "in1" in dut._sigmap:
        dut.in1.value = random.randint(0, 15)
    if "in2" in dut._sigmap:
        dut.in2.value = random.randint(0, 15)
    if "in3" in dut._sigmap:
        dut.in3.value = random.randint(0, 127)
    dut.desired_out.value = random.choice([0, 1])
    await ClockCycles(dut.clk, 10)

    # Check if output is correctly calculated based on the weighted sum and threshold
    expected_output = (dut.in1.value * dut.we1.value + 
                       dut.in2.value * dut.we2.value + 
                       dut.in3.value * dut.we3.value) >= dut.threshold.value
    assert dut.out.value == expected_output, f"Expected output to be {expected_output}, but got {dut.out.value}"

    # Wait a few cycles to allow weight updates
    await ClockCycles(dut.clk, 50)

    # Check that weights are updated after the incorrect output
    assert dut.we1.value != 10, f"Expected we1 to change after weight update, but got {dut.we1.value}"
    assert dut.we2.value != 20, f"Expected we2 to change after weight update, but got {dut.we2.value}"
    assert dut.we3.value != 30, f"Expected we3 to change after weight update, but got {dut.we3.value}"

    dut._log.info("Test Complete")

   