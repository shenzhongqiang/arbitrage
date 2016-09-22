#include <stdio.h>

struct Contract {
    float strike;
    float price;
    char code[18];
};

float get_slope(Contract contracts[], int i1, int i2) {
    float slope = (contracts[i1].price - contracts[i2].price) / (i1-i2);
    return slope;
}

float find_max_profit(Contract contracts[], int n, int mid) {
    int right_i = mid + 1;
    int left_i = mid - 1;
}

int main() {

}
