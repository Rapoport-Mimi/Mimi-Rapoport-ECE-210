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
    reg    [3:0]   we1_mult_inv;
    reg    [3:0]   we2_mult_inv;
    reg    [6:0]   we3_mult_inv;
    wire   [15:0]   weighted;
    parameter LEARNING_RATE_MULT_INV = 16'd10;

    always @(posedge clk or negedge reset) begin
        if (!reset) begin
            out <= 0;
            threshold <= 16'd200; 
            we1_mult_inv <= 4'd10;       
            we2_mult_inv <= 4'd20;       
            we3_mult_inv <= 6'd30; 
        end
        else begin
            out <= (weighted >= threshold);

            if (out != desired_out) begin
                we1_mult_inv <= 1 / ( (1 / we1_mult_inv) + (desired_out - out) * in1 / LEARNING_RATE_MULT_INV );
                we2_mult_inv <= 1 / ( (1 / we2_mult_inv) + (desired_out - out) * in2 / LEARNING_RATE_MULT_INV ); 
                we3_mult_inv <= 1 / ( (1 / we3_mult_inv) + (desired_out - out) * in3 / LEARNING_RATE_MULT_INV );
            end
        end
    end

    // summation logic
    assign weighted = in1 / we1_mult_inv + in2 / we2_mult_inv + in3 / we3_mult_inv; 

endmodule