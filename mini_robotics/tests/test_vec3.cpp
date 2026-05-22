#include "mini_robotics/vec3.h"
#include <iostream>
#include <cassert>

void test_construction() {
    mr::Vec3 a;
    assert(a.x == 0.0 && a.y == 0.0 && a.z == 0.0);

    mr::Vec3 b(1.0, 2.0, 3.0);
    assert(b.x == 1.0 && b.y == 2.0 && b.z == 3.0);
    std::cout << "[PASS] construction\n";
}

void test_dot_product() {
    mr::Vec3 a(1.0, 2.0, 3.0);
    mr::Vec3 b(4.0, 5.0, 6.0);
    double d = a.dot(b);
    assert(d == 32.0); // 1*4 + 2*5 + 3*6 = 4+10+18 = 32
    std::cout << "[PASS] dot product\n";
}

void test_cross_product() {
    mr::Vec3 a(1.0, 0.0, 0.0);
    mr::Vec3 b(0.0, 1.0, 0.0);
    mr::Vec3 c = a.cross(b);
    assert(c.x == 0.0 && c.y == 0.0 && c.z == 1.0);
    // i x j = k
    std::cout << "[PASS] cross product\n";
}

void test_cross_anticommutative() {
    mr::Vec3 a(1.0, 2.0, 3.0);
    mr::Vec3 b(4.0, 5.0, 6.0);
    mr::Vec3 ab = a.cross(b);
    mr::Vec3 ba = b.cross(a);
    assert(ab.x == -ba.x && ab.y == -ba.y && ab.z == -ba.z);
    std::cout << "[PASS] cross product anticommutative\n";
}

void test_norm_and_normalize() {
    mr::Vec3 v(2.0, 3.0, 6.0);
    double n = v.norm();
    assert(n == 7.0); // sqrt(4+9+36) = sqrt(49) = 7

    mr::Vec3 u = v.normalized();
    assert(std::abs(u.norm() - 1.0) < 1e-9);
    std::cout << "[PASS] norm and normalize\n";
}

void test_arithmetic() {
    mr::Vec3 a(1.0, 2.0, 3.0);
    mr::Vec3 b(4.0, 5.0, 6.0);

    mr::Vec3 sum = a + b;
    assert(sum.x == 5.0 && sum.y == 7.0 && sum.z == 9.0);

    mr::Vec3 diff = a - b;
    assert(diff.x == -3.0 && diff.y == -3.0 && diff.z == -3.0);

    mr::Vec3 scaled = a * 2.0;
    assert(scaled.x == 2.0 && scaled.y == 4.0 && scaled.z == 6.0);

    mr::Vec3 scaled2 = 2.0 * a;
    assert(scaled2.x == 2.0 && scaled2.y == 4.0 && scaled2.z == 6.0);
    std::cout << "[PASS] arithmetic\n";
}

void test_negation() {
    mr::Vec3 v(1.0, -2.0, 3.0);
    mr::Vec3 r = -v;
    assert(r.x == -1.0 && r.y == 2.0 && r.z == -3.0);
    std::cout << "[PASS] negation\n";
}

void test_output() {
    mr::Vec3 v(1.5, 2.5, 3.5);
    std::cout << "  Vec3 output: " << v << "\n";
    std::cout << "[PASS] output\n";
}

int main() {
    test_construction();
    test_dot_product();
    test_cross_product();
    test_cross_anticommutative();
    test_norm_and_normalize();
    test_arithmetic();
    test_negation();
    test_output();
    std::cout << "\nAll Vec3 tests passed!\n";
    return 0;
}
