#include "mini_robotics/vec2.h"
#include <iostream>
#include <cassert>

void test_construction() {
    mr::Vec2 a;
    assert(a.x == 0.0 && a.y == 0.0);

    mr::Vec2 b(3.0, 4.0);
    assert(b.x == 3.0 && b.y == 4.0);
    std::cout << "[PASS] construction\n";
}

void test_addition() {
    mr::Vec2 a(1.0, 2.0);
    mr::Vec2 b(3.0, 4.0);
    mr::Vec2 c = a + b;
    assert(c.x == 4.0 && c.y == 6.0);
    std::cout << "[PASS] addition\n";
}

void test_subtraction() {
    mr::Vec2 a(5.0, 7.0);
    mr::Vec2 b(1.0, 3.0);
    mr::Vec2 c = a - b;
    assert(c.x == 4.0 && c.y == 4.0);
    std::cout << "[PASS] subtraction\n";
}

void test_scalar_multiplication() {
    mr::Vec2 v(2.0, 3.0);
    mr::Vec2 r1 = v * 3.0;
    assert(r1.x == 6.0 && r1.y == 9.0);

    mr::Vec2 r2 = 3.0 * v;
    assert(r2.x == 6.0 && r2.y == 9.0);
    std::cout << "[PASS] scalar multiplication\n";
}

void test_negation() {
    mr::Vec2 v(2.0, -3.0);
    mr::Vec2 r = -v;
    assert(r.x == -2.0 && r.y == 3.0);
    std::cout << "[PASS] negation\n";
}

void test_dot_product() {
    mr::Vec2 a(1.0, 2.0);
    mr::Vec2 b(3.0, 4.0);
    double d = a.dot(b);
    assert(d == 11.0); // 1*3 + 2*4 = 11
    std::cout << "[PASS] dot product\n";
}

void test_cross_product() {
    mr::Vec2 a(1.0, 0.0);
    mr::Vec2 b(0.0, 1.0);
    double c = a.cross(b);
    assert(c == 1.0); // |a||b|sin(90°) = 1
    std::cout << "[PASS] cross product (2D)\n";
}

void test_norm() {
    mr::Vec2 v(3.0, 4.0);
    double n = v.norm();
    assert(n == 5.0); // 3-4-5 triangle
    assert(v.norm_sq() == 25.0);
    std::cout << "[PASS] norm\n";
}

void test_normalize() {
    mr::Vec2 v(3.0, 4.0);
    mr::Vec2 u = v.normalized();
    assert(std::abs(u.norm() - 1.0) < 1e-9);
    assert(std::abs(u.x - 0.6) < 1e-9);
    assert(std::abs(u.y - 0.8) < 1e-9);
    std::cout << "[PASS] normalize\n";
}

void test_compound_assignment() {
    mr::Vec2 v(1.0, 2.0);
    v += mr::Vec2(3.0, 4.0);
    assert(v.x == 4.0 && v.y == 6.0);

    v *= 2.0;
    assert(v.x == 8.0 && v.y == 12.0);
    std::cout << "[PASS] compound assignment\n";
}

void test_equality() {
    mr::Vec2 a(1.0, 2.0);
    mr::Vec2 b(1.0, 2.0);
    mr::Vec2 c(1.0, 3.0);
    assert(a == b);
    assert(a != c);
    std::cout << "[PASS] equality\n";
}

void test_output() {
    mr::Vec2 v(1.5, 2.5);
    std::cout << "  Vec2 output: " << v << "\n";
    std::cout << "[PASS] output\n";
}

int main() {
    test_construction();
    test_addition();
    test_subtraction();
    test_scalar_multiplication();
    test_negation();
    test_dot_product();
    test_cross_product();
    test_norm();
    test_normalize();
    test_compound_assignment();
    test_equality();
    test_output();
    std::cout << "\nAll Vec2 tests passed!\n";
    return 0;
}
