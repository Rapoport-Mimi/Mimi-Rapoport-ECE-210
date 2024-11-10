`default_nettype none

module perceptron (
    input wire          clk,
    input wire          reset,
    input wire  [3:0]   in1,
    input wire  [3:0]   in2,
    input wire  [6:0]   in3,
    output reg  [0:0]   out,
    input wire  [0:0]    desired_out
);

    reg    [15:0]   threshold;
    reg    [15:0]   we1;
    reg    [15:0]   we2;
    reg    [15:0]   we3;
    wire   [15:0]   weighted;
    parameter LEARNING_RATE_MULT_INV = 16'd10;

    always @(posedge clk or negedge reset) begin
        if (!reset) begin
            out <= 0;
            threshold <= 16'd200; 
            we1 <= 16'd10;       
            we2 <= 16'd20;       
            we3 <= 16'd30; 
        end
        else begin

            out <= (weighted >= threshold);
            
            // Weight updates
            if (out != desired_out) begin
                we1 <= we1 + ((({15'b0, desired_out} - {15'b0, out}) * in1) / LEARNING_RATE_MULT_INV);
                we2 <= we2 + ((({15'b0, desired_out} - {15'b0, out}) * in2) / LEARNING_RATE_MULT_INV); 
                we3 <= we3 + ((({15'b0, desired_out} - {15'b0, out}) * in3) / LEARNING_RATE_MULT_INV);
            end
        end
    end

    // Summation logic
    assign weighted = in1 * we1 + in2 * we2 + in3 * we3; 

endmodule