def pytest_addoption(parser):
    parser.addoption("--files", action="store")
    parser.addoption("--report", action="store")