`default_nettype none

module perceptron (
    input wire          clk,
    input wire          reset,
    input wire  [7:0]   in1,
    input wire  [7:0]   in2,
    input wire  [7:0]   in3,
    output reg  [0:0]   out,
    output reg  [0:0]   desired_out
);

    reg    [15:0]   threshold;
    reg    [15:0]   we1;
    reg    [15:0]   we2;
    reg    [15:0]   we3;
    wire   [15:0]   weighted;
    parameter ONE_OVER_LEARNING_RATE = 8'd10;

    always @(posedge clk or negedge reset) begin
        if (!reset) begin
            out <= 0;
            threshold <= 200; 
            we1 <= 16'd10;       
            we2 <= 16'd20;       
            we3 <= 16'd30; 
        end
        else begin
            out <= (weighted >= threshold);

            if (out != desired_out) begin
                we1 <= we1 + ((desired_out - out) * in1) / ONE_OVER_LEARNING_RATE;
                we2 <= we2 + ((desired_out - out) * in2) / ONE_OVER_LEARNING_RATE; 
                we3 <= we3 + ((desired_out - out) * in3) / ONE_OVER_LEARNING_RATE;
            end
        end
    end

    // summation logic
    assign weighted = in1 * we1 + in2 * we2 + in3 * we3; 

endmodule