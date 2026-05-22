# 狩猎式学习计划 — 自动化保研/考研复习

> 狩猎法则：以项目为猎物，缺什么学什么，学到什么记什么。笔记 = 战利品清单。

## 猎物（Project）

**用 C++ 写一个 Mini-Robotics 工具库**，逐步增加功能：

| 阶段 | 项目模块 | 练什么 |
|------|---------|--------|
| 1 | `Vec2`, `Vec3`, `Mat2`, `Mat3` 基础类 | **线代** + **C++ 类和运算符重载** |
| 2 | `Matrix` 泛型类 + `vector` 容器 | **STL vector** + **模板** + **线代（矩阵运算）** |
| 3 | 读取 CSV 文件、命令行参数解析 | **Linux 文件 I/O** + **STL string/algorithm** |
| 4 | 2D 正运动学 + 逆运动学求解 | **线代（旋转矩阵、雅可比）** + **C++ 数值计算** |
| 5 | Makefile / CMake 构建 | **Linux 编译工具链** |
| 6 | Git 分支管理、tag、rebase | **Git 全流程** |
| 7 | 单元测试（GoogleTest） | **C++ 测试** + **Linux 库链接** |
| 8 | 控制循环 + 可视化为点集 | **控制理论验证** + **STL 数据流** |

---

## 1. 线性代数 — 以代码视角重学

自动化人的线代重点**不是证明是计算**。

| 目标 | 要点 | 对应项目阶段 |
|------|------|------------|
| 向量点积/叉积/模长 | 用 `std::array` 手写，不用 Eigen | 阶段1 |
| 矩阵乘法 | 三重循环 → 理解 O(n³) | 阶段1-2 |
| 旋转矩阵 (SO2/SO3) | cos/sin 构造 → 2D 机器人旋转 | 阶段4 |
| 齐次坐标 + 平移 | 3×3 齐次变换矩阵 | 阶段4 |
| 矩阵求逆 (Gauss-Jordan) | 手写消元 → 理解数值稳定性 | 阶段2 |
| Jacobian 矩阵 | 2 连杆速度 → 角速度映射 | 阶段4 |
| SVD/PCA (调 Eigen) | 面试要能说原理 | 阶段8 |
| 特征值在控制里的意义 | 极点、稳定性 | 阶段8 |

---

## 2. C++ / STL — 以写库的方式重学

| 目标 | 要点 | 笔记提示 |
|------|------|---------|
| class/struct, 构造/析构, RAII | `Vec3` 类设计 | 记：为什么用 `double` 不用 `float`？ |
| 运算符重载 | `v1 + v2`, `mat * vec` | 记：const 引用 vs 返回值优化 |
| 模板 | `Matrix<N, M>` | 记：编译期 vs 运行期 |
| `std::vector`, `std::array` | 动态 vs 静态大小 | 记：`vector` 扩容机制 |
| `std::algorithm` | `std::sort`, `std::transform` | 记：谓词、lambda |
| `std::map` / `std::unordered_map` | 参数配置字典 | 记：哈希 vs 红黑树 |
| 智能指针 | `unique_ptr`, `shared_ptr` | 记：所有权语义 |
| `const` 正确性 | 哪些函数加 const | 死也要记住 |

---

## 3. Linux — 以开发环境为载体

| 目标 | 要点 |
|------|------|
| 目录结构 (`/`, `/usr`, `/home`) | 脑图记下来 |
| 文件权限 `chmod`/`chown` | 记：`rwx` = 421 |
| `grep` / `find` / `awk` / `sed` | 文本处理四剑客 |
| 管道 `|` 和重定向 `>` | 组合即武器 |
| 编译：`g++ -O2 -g -Wall` | 每个 flag 什么含义 |
| Makefile / CMake | 分别写一个 |
| `gdb` 调试 | 至少会 `break`, `run`, `bt`, `print` |
| `top`/`htop`/`ps` | 看进程和内存 |
| Shell 脚本 | 写一个自动化测试脚本 |

---

## 4. Git — 以项目管理方式练

| 目标 | 要点 |
|------|------|
| `init`, `add`, `commit`, `log` | 基本功 |
| `branch`, `checkout`, `merge` | Git Flow 模型 |
| `rebase -i` (squash/fixup) | 清理提交历史 |
| `reset --soft/hard` | 理解 HEAD/Index/Working |
| `.gitignore` | 哪些不该提交 |
| `remote`, `push`, `pull`, `fetch` | 远程协作 |
| `tag` | 发版标记 |
| `stash` | 临时保存现场 |
| `cherry-pick` | 挑选提交 |

---

## 狩猎笔记模板

每学完一个知识点，按这个模板记一条：

```markdown
## [日期] 猎物: 标题

### 遇到的问题
- 问题1
- 问题2

### 狩猎结果
```cpp
// 代码
```

### 关联
- 关联其他知识点
- 追猎: 下一步要学什么
```

---

## 建议的学习节奏

| 周 | 打下的猎物 |
|----|-----------|
| 1 | 搭环境（WSL/Linux VM）+ Git 初始化 + Vec2/Vec3 |
| 2 | Matrix 模板类 + STL vector + 矩阵乘法 |
| 3 | 高斯消元求逆 + Makefile/CMake |
| 4 | 2D 旋转矩阵 + 正运动学（2 连杆） |
| 5 | 逆运动学 + Jacobian + Git 分支管理 |
| 6 | 单元测试 + Shell 脚本 + 整理笔记查漏补缺 |
