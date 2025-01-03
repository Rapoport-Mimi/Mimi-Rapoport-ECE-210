`default_nettype none

module perceptron (
    input wire          clk,
    input wire          reset,
    input wire  [3:0]   in1,
    input wire  [3:0]   in2,
    input wire  [3:0]   in3,
    output reg  [0:0]   out,
    input wire  [0:0]    desired_out
);

    reg    [3:0]   threshold;
    reg    [3:0]   we1;
    reg    [3:0]   we2;
    reg    [3:0]   we3;
    wire   [3:0]   weighted;
    parameter LEARNING_RATE_MULT_INV = 4'd10;

    always @(posedge clk or negedge reset) begin
        if (!reset) begin
            out <= 0;
            threshold <= 4'd15; 
            we1 <= 4'd5;       
            we2 <= 4'd4;       
            we3 <= 4'd3; 
        end
        else begin

            out <= (weighted >= threshold);
            
            // Weight updates
            if (out != desired_out) begin
                we1 <= we1 + (({4'b0, (desired_out - out)} * in1) / LEARNING_RATE_MULT_INV);
                we2 <= we2 + (({4'b0, (desired_out -  out)} * in2) / LEARNING_RATE_MULT_INV); 
                we3 <= we3 + (({4'b0, (desired_out -  out)} * in3) / LEARNING_RATE_MULT_INV);
            end
        end
    end

    // Summation logic
    assign weighted = in1 * we1 + in2 * we2 + in3 * we3; 

endmodule
