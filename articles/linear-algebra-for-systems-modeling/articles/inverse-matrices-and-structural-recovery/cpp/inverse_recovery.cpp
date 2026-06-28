#include <iostream>
using namespace std;

int main() {
    double a = 3, b = 1, c = 2, d = 4;
    double y1 = 7, y2 = 8;
    double det = a * d - b * c;

    if (det == 0) {
        cout << "Matrix is singular; recovery is not unique." << endl;
        return 1;
    }

    double x1 = (d * y1 - b * y2) / det;
    double x2 = (-c * y1 + a * y2) / det;

    cout << "Recovered state: x1 = " << x1 << ", x2 = " << x2 << endl;
    return 0;
}
