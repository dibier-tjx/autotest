import sys
import pytest

def main():
    # 配置命令行参数
    parser = pytest.Parser()
    
    # 添加自定义参数
    parser.addoption(
        "-m", "--mark", 
        action="store", 
        default="", 
        help="" #只运行指定标记的测试 (如 'slow' 或 'not slow')
    )
    parser.addoption(
        "-k", "--keyword", 
        action="store", 
        default="", 
        help="" #只运行名称包含关键字的测试
    )
    parser.addoption(
        "--test-dir", 
        action="store", 
        default="tests", 
        help="" #指定测试目录 (默认: tests)
    )
    
    # 解析命令行参数
    args, pytest_args = parser.parse_known_args(sys.argv[1:])
    
    # 构建pytest命令行参数
    pytest_options = [
        args.test_dir,  # 测试目录
        "-v",           # 详细输出
        "--color=yes"   # 彩色输出
    ]
    
    # 添加过滤选项
    if args.mark:
        pytest_options.append(f"-m {args.mark}")
    if args.keyword:
        pytest_options.append(f"-k {args.keyword}")
    
    # 添加其他pytest参数
    pytest_options.extend(pytest_args)
    
    # 运行pytest
    exit_code = pytest.main(pytest_options)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()