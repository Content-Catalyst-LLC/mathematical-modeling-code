#include <iomanip>
#include <iostream>
#include <vector>

std::vector<int> neighbors(int i, int n) {
    return {
        (i - 2 + n) % n,
        (i - 1 + n) % n,
        (i + 1) % n,
        (i + 2) % n
    };
}

int main() {
    const int n = 20;
    const int steps = 10;
    const double threshold = 0.35;
    std::vector<bool> adopted(n, false);

    adopted[0] = true;
    adopted[1] = true;
    adopted[2] = true;

    std::cout << "step,adopted_count,adoption_share\n";

    for (int t = 0; t <= steps; ++t) {
        int count = 0;
        for (bool state : adopted) {
            if (state) ++count;
        }

        std::cout << t << "," << count << ","
                  << std::fixed << std::setprecision(6)
                  << static_cast<double>(count) / n << "\n";

        std::vector<bool> next = adopted;
        for (int i = 0; i < n; ++i) {
            if (adopted[i]) continue;
            int adopted_neighbors = 0;
            for (int j : neighbors(i, n)) {
                if (adopted[j]) ++adopted_neighbors;
            }
            if (static_cast<double>(adopted_neighbors) / 4.0 >= threshold) {
                next[i] = true;
            }
        }
        adopted = next;
    }

    return 0;
}
